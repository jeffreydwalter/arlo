Help on module Arlo:

NAME
    Arlo

FILE
    /Users/jeff_walter/Code/github/jeffreydwalter/arlo/Arlo.py

DESCRIPTION
    ##
    # Copyright 2016 Jeffrey D. Walter
    #
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at
    #
    #    http://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.
    ##

CLASSES
    __builtin__.object
        Arlo
    
    class Arlo(__builtin__.object)
     |  Methods defined here:
     |  
     |  AddFriend(self, firstname, lastname, email, devices={}, admin=False)
     |  
     |  AdjustBrightness(self, basestation, camera, brightness=0)
     |  
     |  AlertNotificationMethods(self, basestation, action='disabled', email=False, push=False)
     |  
     |  Arm(self, device)
     |  
     |  BatchDeleteRecordings(self, recording_metadata)
     |  
     |  Calendar(self, basestation, active=True)
     |  
     |  CustomMode(self, device, mode, schedules=[])
     |  
     |  DeleteMode(self, device, mode)
     |  
     |  DeleteRecording(self, camera, created_date, utc_created_date)
     |  
     |  Disarm(self, device)
     |  
     |  DownloadRecording(self, url, to)
     |  
     |  DownloadSnapshot(self, url, to, chunk_size=4096)
     |  
     |  Geofencing(self, location_id, active=True)
     |  
     |  GetAudioPlayback(self, basestation)
     |  
     |  GetAutomationActivityZones(self, camera)
     |  
     |  GetAutomationDefinitions(self)
     |  
     |  GetBaseStationState(self, basestation)
     |  
     |  GetCalendar(self, basestation)
     |  
     |  GetCameraState(self, basestation)
     |  
     |  GetCameraTempReading(self, basestation)
     |  
     |  GetCvrPlaylist(self, camera, fromDate, toDate)
     |  
     |  GetDeviceCapabilities(self, device)
     |  
     |  GetDeviceSupport(self)
     |  
     |  GetDeviceSupportV3(self)
     |  
     |  GetDeviceSupportv2(self)
     |  
     |  GetDevices(self, device_type=None)
     |  
     |  GetEmergencyLocations(self)
     |  
     |  GetFriends(self)
     |  
     |  GetLibrary(self, from_date, to_date)
     |  
     |  GetLibraryMetaData(self, from_date, to_date)
     |  
     |  GetLocations(self)
     |  
     |  GetModes(self, basestation)
     |  
     |  GetModesV2(self)
     |  
     |  GetOCProfile(self)
     |  
     |  GetPaymentBilling(self)
     |  
     |  GetPaymentOffers(self)
     |  
     |  GetPaymentOffersV2(self)
     |  
     |  GetPaymentOffersV3(self)
     |  
     |  GetPaymentOffersV4(self)
     |  
     |  GetProfile(self)
     |  
     |  GetRecording(self, url, chunk_size=4096)
     |  
     |  GetRules(self, basestation)
     |  
     |  GetSensorConfig(self, basestation)
     |  
     |  GetServiceLevel(self)
     |  
     |  GetServiceLevelSettings(self)
     |  
     |  GetServiceLevelV2(self)
     |  
     |  GetServiceLevelV3(self)
     |  
     |  GetServiceLevelV4(self)
     |  
     |  GetSession(self)
     |  
     |  GetSmartAlerts(self, camera)
     |  
     |  GetSmartFeatures(self)
     |  
     |  GetUpdateFeatures(self)
     |  
     |  HandleEvents(self, basestation, callback, timeout=120)
     |  
     |  Login(self, username, password)
     |  
     |  Logout(self)
     |  
     |  Notify(self, basestation, body)
     |  
     |  NotifyAndGetResponse(self, basestation, body, timeout=120)
     |  
     |  PauseTrack(self, basestation)
     |  
     |  Ping(self, basestation)
     |  
     |  PlayTrack(self, basestation, track_id='2391d620-e491-4412-99f6-e9a40d6046ed', position=0)
     |  
     |  PushToTalk(self, camera)
     |  
     |  RemoveFriend(self, email)
     |  
     |  ResendFriendInvite(self, friend)
     |  
     |  Reset(self)
     |  
     |  RestartBasestation(self, basestation)
     |  
     |  SetAirQualityAlertOff(self, basestation)
     |  
     |  SetAirQualityAlertOn(self, basestation)
     |  
     |  SetAirQualityAlertThresholdMax(self, basestation, number=700)
     |  
     |  SetAirQualityAlertThresholdMin(self, basestation, number=400)
     |  
     |  SetAirQualityRecordingOff(self, basestation)
     |  
     |  SetAirQualityRecordingOn(self, basestation)
     |  
     |  SetAudioAlertsOff(self, basestation, sensitivity=3)
     |  
     |  SetAudioAlertsOn(self, basestation, sensitivity=3)
     |  
     |  SetAutomationActivityZones(self, camera, zone, coords, color)
     |  
     |  SetHumidityAlertOff(self, basestation)
     |  
     |  SetHumidityAlertOn(self, basestation)
     |  
     |  SetHumidityAlertThresholdMax(self, basestation, number=800)
     |  
     |  SetHumidityAlertThresholdMin(self, basestation, number=400)
     |  
     |  SetHumidityRecordingOff(self, basestation)
     |  
     |  SetHumidityRecordingOn(self, basestation)
     |  
     |  SetLoopBackModeContinuous(self, basestation)
     |  
     |  SetLoopBackModeSingleTrack(self, basestation)
     |  
     |  SetMotionAlertsOff(self, basestation, sensitivity=5)
     |  
     |  SetMotionAlertsOn(self, basestation, sensitivity=5)
     |  
     |  SetNightLightBrightness(self, basestation, level=200)
     |  
     |  SetNightLightColor(self, basestation, red=255, green=255, blue=255)
     |  
     |  SetNightLightMode(self, basestation, mode='rainbow')
     |  
     |  SetNightLightOff(self, basestation)
     |  
     |  SetNightLightOn(self, basestation)
     |  
     |  SetNightLightTimerOff(self, basestation, time=0, timediff=300)
     |  
     |  SetNightLightTimerOn(self, basestation, time=1548482956, timediff=0)
     |  
     |  SetOCProfile(self, firstName, lastName, country='United States', language='en', spam_me=0)
     |  
     |  SetSchedule(self, basestation, schedule)
     |  
     |  SetShuffleOff(self, basestation)
     |  
     |  SetShuffleOn(self, basestation)
     |  
     |  SetSleepTimerOff(self, basestation, time=0, timediff=300)
     |  
     |  SetSleepTimerOn(self, basestation, time=1548482956, timediff=0)
     |  
     |  SetTempAlertOff(self, basestation)
     |  
     |  SetTempAlertOn(self, basestation)
     |  
     |  SetTempAlertThresholdMax(self, basestation, number=240)
     |  
     |  SetTempAlertThresholdMin(self, basestation, number=200)
     |  
     |  SetTempRecordingOff(self, basestation)
     |  
     |  SetTempRecordingOn(self, basestation)
     |  
     |  SetTempUnit(self, uniqueId, unit='C')
     |  
     |  SetVolume(self, basestation, mute=False, volume=50)
     |  
     |  SirenOff(self, basestation)
     |  
     |  SirenOn(self, basestation)
     |  
     |  SkipTrack(self, basestation)
     |  
     |  StartRecording(self, basestation, camera)
     |  
     |  StartStream(self, basestation, camera)
     |  
     |  StopRecording(self, camera)
     |  
     |  StopStream(self, basestation, camera)
     |  
     |  StreamRecording(self, url, chunk_size=4096)
     |  
     |  Subscribe(self, basestation)
     |  
     |  SubscribeToMotionEvents(self, basestation, callback, timeout=120)
     |  
     |  ToggleCamera(self, basestation, camera, active=True)
     |  
     |  TriggerAndHandleEvent(self, basestation, trigger, callback, timeout=120)
     |  
     |  TriggerFullFrameSnapshot(self, basestation, camera)
     |  
     |  TriggerStreamSnapshot(self, basestation, camera)
     |  
     |  Unsubscribe(self, basestation)
     |  
     |  UpdateDeviceName(self, device, name)
     |  
     |  UpdateDisplayOrder(self, body)
     |  
     |  UpdateFriend(self, body)
     |  
     |  UpdatePassword(self, password)
     |  
     |  UpdateProfile(self, first_name, last_name)
     |  
     |  __init__(self, username, password)
     |  
     |  genTransId(self, trans_type='web')
     |  
     |  interrupt_handler(self, signum, frame)
     |  
     |  to_timestamp(self, dt)
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  TRANSID_PREFIX = 'web'

DATA
    string_types = (<type 'basestring'>,)


