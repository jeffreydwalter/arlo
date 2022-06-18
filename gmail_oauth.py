import pickle

# import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow

FILENAME = 'gmail.credentials'
PORT = 7788

flow = InstalledAppFlow.from_client_secrets_file(
    'google_client_credentials.json',
    scopes=['https://www.googleapis.com/auth/gmail.readonly'])

flow.redirect_uri = 'http://localhost:{}/'.format(PORT)

authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true')

credentials = flow.run_local_server(host='localhost',
                                    port=PORT,
                                    authorization_prompt_message='Please visit this URL: {}'.format(authorization_url),
                                    success_message='The auth flow is complete; you may close this window.',
                                    open_browser=True)

pickle.dump(credentials, open(FILENAME, 'wb'))
