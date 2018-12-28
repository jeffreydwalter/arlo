from Arlo import Arlo
from datetime import timedelta, date
import datetime
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
import json
import os
import logging


class ArloGooglePhotos:

    def __init__(self, arlo):
        """ (Arlo, str, str) -> None
        Start an Arlo Google Photos session
        """
        self.arlo = arlo
        # Get auth from file or log user in via browser
        self.googlePhotos = GooglePhotos()
        self.last_update = (date.today() - timedelta(days=30)).strftime("%Y%m%d")
        self.videos_to_upload = []
        self.photos_uploaded = self._load_uploaded_files()

        # create folder "temp"
        if not os.path.exists("temp"):
            os.mkdir("temp")

    def run(self):
        """ Downloads arlo footage and uploads them to google photos"""
        print("Checking for new footage... This may take a minute")
        while True:
            self._get_videos()
            self.last_update = date.today().strftime("%Y%m%d");
            self._upload()
            time.sleep(60)  # re-check every minute
            print("Upload complete. Snoozing for 1 minute... zzzzzzzzz")

    def _get_videos(self):
        # Downloads videos from Arlo and uploads every 10 videos
        try:
            today = (date.today() - timedelta(days=0)).strftime("%Y%m%d")
            library = self.arlo.GetLibrary(self.last_update, today)
            counter = 0  # count number of videos
            for recording in library:

                # Grab the recording name
                videofilename = datetime.datetime.fromtimestamp(int(recording['name']) // 1000).strftime(
                    '%Y-%m-%d %H-%M-%S') + ' ' + recording['uniqueId'] + '.mp4'

                # skip files that have been uploaded
                if videofilename in self.photos_uploaded:
                    continue
                counter += 1

                # Download video recording from Arlo
                stream = self.arlo.StreamRecording(recording['presignedContentUrl'])
                with open('temp/' + videofilename, 'wb') as f:
                    for chunk in stream:
                        f.write(chunk)
                    f.close()
                print('Downloaded footage: ' + videofilename)
                self.videos_to_upload.append('temp/' + videofilename)

                # upload to g photos every 10 downloads
                if counter % 10 == 0:
                    self._upload(10)

        except Exception as e:
            print(e)

    def _upload(self, num=None):
        upload_list = self.videos_to_upload
        if num:
            upload_list = self.videos_to_upload[:num]

        self.googlePhotos.upload_photos(upload_list,
                                        'Arlo')

        # Delete uploaded recordings
        for file in upload_list:
            self.photos_uploaded.append(file[5:])  # remove "temp/" from filename
            if os.path.exists(file):
                os.remove(file)
                self.videos_to_upload.remove(file)

        self._save_uploaded_files()  # save progress

    def _save_uploaded_files(self):
        f = open('uploaded.json', 'w+')
        f.write(json.dumps(self.photos_uploaded))
        f.close()

    def _load_uploaded_files(self):
        if os.path.exists('uploaded.json'):
            f = open('uploaded.json', 'r')
            list = json.loads(f.read())
            return list
        else:
            return []

class GooglePhotos:
    """ Thanks to eshmu/gphotos-upload """

    def __init__(self):
        self.session = self.get_authorized_session('google_auth.json')

    def auth(self, scopes):
        flow = InstalledAppFlow.from_client_secrets_file(
            'g_client.json',
            scopes=scopes)

        print('Opening OAuth')
        credentials = flow.run_local_server(host='localhost',
                                            port=8080,
                                            authorization_prompt_message="",
                                            success_message='Done. You may close this window.',
                                            open_browser=True)

        print('Logged into Google Photos')
        return credentials

    def get_authorized_session(self, auth_token_file):

        scopes=['https://www.googleapis.com/auth/photoslibrary',
                'https://www.googleapis.com/auth/photoslibrary.sharing']

        cred = None

        if auth_token_file:
            try:
                cred = Credentials.from_authorized_user_file(auth_token_file, scopes)
            except OSError as err:
                logging.debug("Error opening auth token file - {0}".format(err))
            except ValueError:
                logging.debug("Error loading auth tokens - Incorrect format")

        if not cred:
            cred = self.auth(scopes)

        try:
            self.save_cred(cred, auth_token_file)
        except OSError as err:
            logging.debug("Could not save auth tokens - {0}".format(err))

        session = AuthorizedSession(cred)
        return session

    def save_cred(self, cred, auth_file):

        cred_dict = {
            'token': cred.token,
            'refresh_token': cred.refresh_token,
            'id_token': cred.id_token,
            'scopes': cred.scopes,
            'token_uri': cred.token_uri,
            'client_id': cred.client_id,
            'client_secret': cred.client_secret
        }

        with open(auth_file, 'w') as f:
            print(json.dumps(cred_dict), file=f)

    # Generator to loop through all albums
    def getAlbums(self, session, appCreatedOnly=False):

        params = {
                'excludeNonAppCreatedData': appCreatedOnly
        }

        while True:

            albums = session.get('https://photoslibrary.googleapis.com/v1/albums', params=params).json()
            logging.debug("Server response: {}".format(albums))

            if 'albums' in albums:

                for a in albums["albums"]:
                    yield a

                if 'nextPageToken' in albums:
                    params["pageToken"] = albums["nextPageToken"]
                else:
                    return

            else:
                return

    def create_or_retrieve_album(self, session, album_title):
        # Find albums created by this app to see if one matches album_title
        for a in self.getAlbums(session, True):
            if a["title"].lower() == album_title.lower():
                album_id = a["id"]
                logging.info("Uploading into EXISTING photo album -- \'{0}\'".format(album_title))
                return album_id

    # No matches, create new album

        create_album_body = json.dumps({"album":{"title": album_title}})
        resp = session.post('https://photoslibrary.googleapis.com/v1/albums', create_album_body).json()

        logging.debug("Server response: {}".format(resp))

        if "id" in resp:
            logging.info("Uploading into NEW photo album -- \'{0}\'".format(album_title))
            return resp['id']
        else:
            logging.error("Could not find or create photo album '\{0}\'. Server Response: {1}".format(album_title, resp))
            return None

    def upload_photos(self, photo_file_list, album_name):
        album_id = self.create_or_retrieve_album(self.session, album_name) if album_name else None

        # interrupt upload if an upload was requested but could not be created
        if album_name and not album_id:
            return

        self.session.headers["Content-type"] = "application/octet-stream"
        self.session.headers["X-Goog-Upload-Protocol"] = "raw"

        for photo_file_name in photo_file_list:

            try:
                photo_file = open(photo_file_name, mode='rb')
                photo_bytes = photo_file.read()
            except OSError as err:
                logging.error("Could not read file \'{0}\' -- {1}".format(photo_file_name, err))
                continue

            self.session.headers["X-Goog-Upload-File-Name"] = os.path.basename(photo_file_name)

            logging.info("Uploading photo -- \'{}\'".format(photo_file_name))

            upload_token = self.session.post('https://photoslibrary.googleapis.com/v1/uploads', photo_bytes)

            if (upload_token.status_code == 200) and (upload_token.content):

                create_body = json.dumps({"albumId":album_id, "newMediaItems":[{"description":"","simpleMediaItem":{"uploadToken":upload_token.content.decode()}}]}, indent=4)

                resp = self.session.post('https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate', create_body).json()

                logging.debug("Server response: {}".format(resp))

                if "newMediaItemResults" in resp:
                    status = resp["newMediaItemResults"][0]["status"]
                    if status.get("code") and (status.get("code") > 0):
                        logging.error("Could not add \'{0}\' to library -- {1}".format(os.path.basename(photo_file_name), status["message"]))
                    else:
                        logging.info("Added \'{}\' to library and album \'{}\' ".format(os.path.basename(photo_file_name), album_name))
                else:
                    logging.error("Could not add \'{0}\' to library. Server Response -- {1}".format(os.path.basename(photo_file_name), resp))

            else:
                logging.error("Could not upload \'{0}\'. Server Response - {1}".format(os.path.basename(photo_file_name), upload_token))

            print('Uploaded: ' + photo_file_name)

        try:
            del(self.session.headers["Content-type"])
            del(self.session.headers["X-Goog-Upload-Protocol"])
            del(self.session.headers["X-Goog-Upload-File-Name"])
        except KeyError:
            pass
