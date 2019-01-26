<p><tt>##<br>
#&nbsp;Copyright&nbsp;2016&nbsp;Jeffrey&nbsp;D.&nbsp;Walter<br>
#<br>
#&nbsp;Licensed&nbsp;under&nbsp;the&nbsp;Apache&nbsp;License,&nbsp;Version&nbsp;2.0&nbsp;(the&nbsp;"License");<br>
#&nbsp;you&nbsp;may&nbsp;not&nbsp;use&nbsp;this&nbsp;file&nbsp;except&nbsp;in&nbsp;compliance&nbsp;with&nbsp;the&nbsp;License.<br>
#&nbsp;You&nbsp;may&nbsp;obtain&nbsp;a&nbsp;copy&nbsp;of&nbsp;the&nbsp;License&nbsp;at<br>
#<br>
#&nbsp;&nbsp;&nbsp;&nbsp;<a href="http://www.apache.org/licenses/LICENSE-2.0">http://www.apache.org/licenses/LICENSE-2.0</a><br>
#<br>
#&nbsp;Unless&nbsp;required&nbsp;by&nbsp;applicable&nbsp;law&nbsp;or&nbsp;agreed&nbsp;to&nbsp;in&nbsp;writing,&nbsp;software<br>
#&nbsp;distributed&nbsp;under&nbsp;the&nbsp;License&nbsp;is&nbsp;distributed&nbsp;on&nbsp;an&nbsp;"AS&nbsp;IS"&nbsp;BASIS,<br>
#&nbsp;WITHOUT&nbsp;WARRANTIES&nbsp;OR&nbsp;CONDITIONS&nbsp;OF&nbsp;ANY&nbsp;KIND,&nbsp;either&nbsp;express&nbsp;or&nbsp;implied.<br>
#&nbsp;See&nbsp;the&nbsp;License&nbsp;for&nbsp;the&nbsp;specific&nbsp;language&nbsp;governing&nbsp;permissions&nbsp;and<br>
#&nbsp;limitations&nbsp;under&nbsp;the&nbsp;License.<br>
##</tt></p>
<p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#aa55cc">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Modules</strong></big></font></td></tr>
    
<tr><td bgcolor="#aa55cc"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><table width="100%" summary="list"><tr><td width="25%" valign=top><a href="calendar.html">calendar</a><br>
<a href="json.html">json</a><br>
<a href="math.html">math</a><br>
</td><td width="25%" valign=top><a href="os.html">os</a><br>
<a href="Queue.html">Queue</a><br>
<a href="random.html">random</a><br>
</td><td width="25%" valign=top><a href="signal.html">signal</a><br>
<a href="sys.html">sys</a><br>
<a href="time.html">time</a><br>
</td><td width="25%" valign=top></td></tr></table></td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ee77aa">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Classes</strong></big></font></td></tr>
    
<tr><td bgcolor="#ee77aa"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><dl>
<dt><font face="helvetica, arial"><a href="__builtin__.html#object">__builtin__.object</a>
</font></dt><dd>
<dl>
<dt><font face="helvetica, arial"><a href="arlo.html#Arlo">Arlo</a>
</font></dt></dl>
</dd>
</dl>
 <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="Arlo">class <strong>Arlo</strong></a>(<a href="__builtin__.html#object">__builtin__.object</a>)</font></td></tr>
    
<tr><td bgcolor="#ffc8d8"><tt>&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%">Methods defined here:<br>
<dl><dt><a name="Arlo-AddFriend"><strong>AddFriend</strong></a>(self, firstname, lastname, email, devices<font color="#909090">={}</font>, admin<font color="#909090">=False</font>)</dt></dl>

<dl><dt><a name="Arlo-AdjustBrightness"><strong>AdjustBrightness</strong></a>(self, basestation, camera, brightness<font color="#909090">=0</font>)</dt></dl>

<dl><dt><a name="Arlo-AlertNotificationMethods"><strong>AlertNotificationMethods</strong></a>(self, basestation, action<font color="#909090">='disabled'</font>, email<font color="#909090">=False</font>, push<font color="#909090">=False</font>)</dt></dl>

<dl><dt><a name="Arlo-Arm"><strong>Arm</strong></a>(self, device)</dt></dl>

<dl><dt><a name="Arlo-BatchDeleteRecordings"><strong>BatchDeleteRecordings</strong></a>(self, recording_metadata)</dt></dl>

<dl><dt><a name="Arlo-Calendar"><strong>Calendar</strong></a>(self, basestation, active<font color="#909090">=True</font>)</dt></dl>

<dl><dt><a name="Arlo-CustomMode"><strong>CustomMode</strong></a>(self, device, mode, schedules<font color="#909090">=[]</font>)</dt></dl>

<dl><dt><a name="Arlo-DeleteMode"><strong>DeleteMode</strong></a>(self, device, mode)</dt></dl>

<dl><dt><a name="Arlo-DeleteRecording"><strong>DeleteRecording</strong></a>(self, camera, created_date, utc_created_date)</dt></dl>

<dl><dt><a name="Arlo-Disarm"><strong>Disarm</strong></a>(self, device)</dt></dl>

<dl><dt><a name="Arlo-DownloadRecording"><strong>DownloadRecording</strong></a>(self, url, to)</dt></dl>

<dl><dt><a name="Arlo-DownloadSnapshot"><strong>DownloadSnapshot</strong></a>(self, url, to, chunk_size<font color="#909090">=4096</font>)</dt></dl>

<dl><dt><a name="Arlo-Geofencing"><strong>Geofencing</strong></a>(self, location_id, active<font color="#909090">=True</font>)</dt></dl>

<dl><dt><a name="Arlo-GetAudioPlayback"><strong>GetAudioPlayback</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-GetAutomationActivityZones"><strong>GetAutomationActivityZones</strong></a>(self, camera)</dt></dl>

<dl><dt><a name="Arlo-GetAutomationDefinitions"><strong>GetAutomationDefinitions</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetBaseStationState"><strong>GetBaseStationState</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-GetCalendar"><strong>GetCalendar</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-GetCameraState"><strong>GetCameraState</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-GetCameraTempReading"><strong>GetCameraTempReading</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-GetCvrPlaylist"><strong>GetCvrPlaylist</strong></a>(self, camera, fromDate, toDate)</dt></dl>

<dl><dt><a name="Arlo-GetDeviceCapabilities"><strong>GetDeviceCapabilities</strong></a>(self, device)</dt></dl>

<dl><dt><a name="Arlo-GetDeviceSupport"><strong>GetDeviceSupport</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetDeviceSupportV3"><strong>GetDeviceSupportV3</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetDeviceSupportv2"><strong>GetDeviceSupportv2</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetDevices"><strong>GetDevices</strong></a>(self, device_type<font color="#909090">=None</font>)</dt></dl>

<dl><dt><a name="Arlo-GetEmergencyLocations"><strong>GetEmergencyLocations</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetFriends"><strong>GetFriends</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetLibrary"><strong>GetLibrary</strong></a>(self, from_date, to_date)</dt></dl>

<dl><dt><a name="Arlo-GetLibraryMetaData"><strong>GetLibraryMetaData</strong></a>(self, from_date, to_date)</dt></dl>

<dl><dt><a name="Arlo-GetLocations"><strong>GetLocations</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetModes"><strong>GetModes</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-GetModesV2"><strong>GetModesV2</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetOCProfile"><strong>GetOCProfile</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetPaymentBilling"><strong>GetPaymentBilling</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetPaymentOffers"><strong>GetPaymentOffers</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetPaymentOffersV2"><strong>GetPaymentOffersV2</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetPaymentOffersV3"><strong>GetPaymentOffersV3</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetPaymentOffersV4"><strong>GetPaymentOffersV4</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetProfile"><strong>GetProfile</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetRecording"><strong>GetRecording</strong></a>(self, url, chunk_size<font color="#909090">=4096</font>)</dt></dl>

<dl><dt><a name="Arlo-GetRules"><strong>GetRules</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-GetSensorConfig"><strong>GetSensorConfig</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-GetServiceLevel"><strong>GetServiceLevel</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetServiceLevelSettings"><strong>GetServiceLevelSettings</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetServiceLevelV2"><strong>GetServiceLevelV2</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetServiceLevelV3"><strong>GetServiceLevelV3</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetServiceLevelV4"><strong>GetServiceLevelV4</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetSession"><strong>GetSession</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetSmartAlerts"><strong>GetSmartAlerts</strong></a>(self, camera)</dt></dl>

<dl><dt><a name="Arlo-GetSmartFeatures"><strong>GetSmartFeatures</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-GetUpdateFeatures"><strong>GetUpdateFeatures</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-HandleEvents"><strong>HandleEvents</strong></a>(self, basestation, callback, timeout<font color="#909090">=120</font>)</dt></dl>

<dl><dt><a name="Arlo-Login"><strong>Login</strong></a>(self, username, password)</dt></dl>

<dl><dt><a name="Arlo-Logout"><strong>Logout</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-Notify"><strong>Notify</strong></a>(self, basestation, body)</dt></dl>

<dl><dt><a name="Arlo-NotifyAndGetResponse"><strong>NotifyAndGetResponse</strong></a>(self, basestation, body, timeout<font color="#909090">=120</font>)</dt></dl>

<dl><dt><a name="Arlo-PauseTrack"><strong>PauseTrack</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-Ping"><strong>Ping</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-PlayTrack"><strong>PlayTrack</strong></a>(self, basestation, track_id<font color="#909090">='2391d620-e491-4412-99f6-e9a40d6046ed'</font>, position<font color="#909090">=0</font>)</dt></dl>

<dl><dt><a name="Arlo-PushToTalk"><strong>PushToTalk</strong></a>(self, camera)</dt></dl>

<dl><dt><a name="Arlo-RemoveFriend"><strong>RemoveFriend</strong></a>(self, email)</dt></dl>

<dl><dt><a name="Arlo-ResendFriendInvite"><strong>ResendFriendInvite</strong></a>(self, friend)</dt></dl>

<dl><dt><a name="Arlo-Reset"><strong>Reset</strong></a>(self)</dt></dl>

<dl><dt><a name="Arlo-RestartBasestation"><strong>RestartBasestation</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetAirQualityAlertOff"><strong>SetAirQualityAlertOff</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetAirQualityAlertOn"><strong>SetAirQualityAlertOn</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetAirQualityAlertThresholdMax"><strong>SetAirQualityAlertThresholdMax</strong></a>(self, basestation, number<font color="#909090">=700</font>)</dt></dl>

<dl><dt><a name="Arlo-SetAirQualityAlertThresholdMin"><strong>SetAirQualityAlertThresholdMin</strong></a>(self, basestation, number<font color="#909090">=400</font>)</dt></dl>

<dl><dt><a name="Arlo-SetAirQualityRecordingOff"><strong>SetAirQualityRecordingOff</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetAirQualityRecordingOn"><strong>SetAirQualityRecordingOn</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetAudioAlertsOff"><strong>SetAudioAlertsOff</strong></a>(self, basestation, sensitivity<font color="#909090">=3</font>)</dt></dl>

<dl><dt><a name="Arlo-SetAudioAlertsOn"><strong>SetAudioAlertsOn</strong></a>(self, basestation, sensitivity<font color="#909090">=3</font>)</dt></dl>

<dl><dt><a name="Arlo-SetAutomationActivityZones"><strong>SetAutomationActivityZones</strong></a>(self, camera, zone, coords, color)</dt></dl>

<dl><dt><a name="Arlo-SetHumidityAlertOff"><strong>SetHumidityAlertOff</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetHumidityAlertOn"><strong>SetHumidityAlertOn</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetHumidityAlertThresholdMax"><strong>SetHumidityAlertThresholdMax</strong></a>(self, basestation, number<font color="#909090">=800</font>)</dt></dl>

<dl><dt><a name="Arlo-SetHumidityAlertThresholdMin"><strong>SetHumidityAlertThresholdMin</strong></a>(self, basestation, number<font color="#909090">=400</font>)</dt></dl>

<dl><dt><a name="Arlo-SetHumidityRecordingOff"><strong>SetHumidityRecordingOff</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetHumidityRecordingOn"><strong>SetHumidityRecordingOn</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetLoopBackModeContinuous"><strong>SetLoopBackModeContinuous</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetLoopBackModeSingleTrack"><strong>SetLoopBackModeSingleTrack</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetMotionAlertsOff"><strong>SetMotionAlertsOff</strong></a>(self, basestation, sensitivity<font color="#909090">=5</font>)</dt></dl>

<dl><dt><a name="Arlo-SetMotionAlertsOn"><strong>SetMotionAlertsOn</strong></a>(self, basestation, sensitivity<font color="#909090">=5</font>)</dt></dl>

<dl><dt><a name="Arlo-SetNightLightBrightness"><strong>SetNightLightBrightness</strong></a>(self, basestation, level<font color="#909090">=200</font>)</dt></dl>

<dl><dt><a name="Arlo-SetNightLightColor"><strong>SetNightLightColor</strong></a>(self, basestation, red<font color="#909090">=255</font>, green<font color="#909090">=255</font>, blue<font color="#909090">=255</font>)</dt></dl>

<dl><dt><a name="Arlo-SetNightLightMode"><strong>SetNightLightMode</strong></a>(self, basestation, mode<font color="#909090">='rainbow'</font>)</dt></dl>

<dl><dt><a name="Arlo-SetNightLightOff"><strong>SetNightLightOff</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetNightLightOn"><strong>SetNightLightOn</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetNightLightTimerOff"><strong>SetNightLightTimerOff</strong></a>(self, basestation, time<font color="#909090">=0</font>, timediff<font color="#909090">=300</font>)</dt></dl>

<dl><dt><a name="Arlo-SetNightLightTimerOn"><strong>SetNightLightTimerOn</strong></a>(self, basestation, time<font color="#909090">=1548529573</font>, timediff<font color="#909090">=0</font>)</dt></dl>

<dl><dt><a name="Arlo-SetOCProfile"><strong>SetOCProfile</strong></a>(self, firstName, lastName, country<font color="#909090">='United States'</font>, language<font color="#909090">='en'</font>, spam_me<font color="#909090">=0</font>)</dt></dl>

<dl><dt><a name="Arlo-SetSchedule"><strong>SetSchedule</strong></a>(self, basestation, schedule)</dt></dl>

<dl><dt><a name="Arlo-SetShuffleOff"><strong>SetShuffleOff</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetShuffleOn"><strong>SetShuffleOn</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetSleepTimerOff"><strong>SetSleepTimerOff</strong></a>(self, basestation, time<font color="#909090">=0</font>, timediff<font color="#909090">=300</font>)</dt></dl>

<dl><dt><a name="Arlo-SetSleepTimerOn"><strong>SetSleepTimerOn</strong></a>(self, basestation, time<font color="#909090">=1548529573</font>, timediff<font color="#909090">=0</font>)</dt></dl>

<dl><dt><a name="Arlo-SetTempAlertOff"><strong>SetTempAlertOff</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetTempAlertOn"><strong>SetTempAlertOn</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetTempAlertThresholdMax"><strong>SetTempAlertThresholdMax</strong></a>(self, basestation, number<font color="#909090">=240</font>)</dt></dl>

<dl><dt><a name="Arlo-SetTempAlertThresholdMin"><strong>SetTempAlertThresholdMin</strong></a>(self, basestation, number<font color="#909090">=200</font>)</dt></dl>

<dl><dt><a name="Arlo-SetTempRecordingOff"><strong>SetTempRecordingOff</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetTempRecordingOn"><strong>SetTempRecordingOn</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SetTempUnit"><strong>SetTempUnit</strong></a>(self, uniqueId, unit<font color="#909090">='C'</font>)</dt></dl>

<dl><dt><a name="Arlo-SetVolume"><strong>SetVolume</strong></a>(self, basestation, mute<font color="#909090">=False</font>, volume<font color="#909090">=50</font>)</dt></dl>

<dl><dt><a name="Arlo-SirenOff"><strong>SirenOff</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SirenOn"><strong>SirenOn</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SkipTrack"><strong>SkipTrack</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-StartRecording"><strong>StartRecording</strong></a>(self, basestation, camera)</dt></dl>

<dl><dt><a name="Arlo-StartStream"><strong>StartStream</strong></a>(self, basestation, camera)</dt></dl>

<dl><dt><a name="Arlo-StopRecording"><strong>StopRecording</strong></a>(self, camera)</dt></dl>

<dl><dt><a name="Arlo-StopStream"><strong>StopStream</strong></a>(self, basestation, camera)</dt></dl>

<dl><dt><a name="Arlo-StreamRecording"><strong>StreamRecording</strong></a>(self, url, chunk_size<font color="#909090">=4096</font>)</dt></dl>

<dl><dt><a name="Arlo-Subscribe"><strong>Subscribe</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-SubscribeToMotionEvents"><strong>SubscribeToMotionEvents</strong></a>(self, basestation, callback, timeout<font color="#909090">=120</font>)</dt></dl>

<dl><dt><a name="Arlo-ToggleCamera"><strong>ToggleCamera</strong></a>(self, basestation, camera, active<font color="#909090">=True</font>)</dt></dl>

<dl><dt><a name="Arlo-TriggerAndHandleEvent"><strong>TriggerAndHandleEvent</strong></a>(self, basestation, trigger, callback, timeout<font color="#909090">=120</font>)</dt></dl>

<dl><dt><a name="Arlo-TriggerFullFrameSnapshot"><strong>TriggerFullFrameSnapshot</strong></a>(self, basestation, camera)</dt></dl>

<dl><dt><a name="Arlo-TriggerStreamSnapshot"><strong>TriggerStreamSnapshot</strong></a>(self, basestation, camera)</dt></dl>

<dl><dt><a name="Arlo-Unsubscribe"><strong>Unsubscribe</strong></a>(self, basestation)</dt></dl>

<dl><dt><a name="Arlo-UpdateDeviceName"><strong>UpdateDeviceName</strong></a>(self, device, name)</dt></dl>

<dl><dt><a name="Arlo-UpdateDisplayOrder"><strong>UpdateDisplayOrder</strong></a>(self, body)</dt></dl>

<dl><dt><a name="Arlo-UpdateFriend"><strong>UpdateFriend</strong></a>(self, body)</dt></dl>

<dl><dt><a name="Arlo-UpdatePassword"><strong>UpdatePassword</strong></a>(self, password)</dt></dl>

<dl><dt><a name="Arlo-UpdateProfile"><strong>UpdateProfile</strong></a>(self, first_name, last_name)</dt></dl>

<dl><dt><a name="Arlo-__init__"><strong>__init__</strong></a>(self, username, password)</dt></dl>

<dl><dt><a name="Arlo-genTransId"><strong>genTransId</strong></a>(self, trans_type<font color="#909090">='web'</font>)</dt></dl>

<dl><dt><a name="Arlo-interrupt_handler"><strong>interrupt_handler</strong></a>(self, signum, frame)</dt></dl>

<dl><dt><a name="Arlo-to_timestamp"><strong>to_timestamp</strong></a>(self, dt)</dt></dl>

<hr>
Data descriptors defined here:<br>
<dl><dt><strong>__dict__</strong></dt>
<dd><tt>dictionary&nbsp;for&nbsp;instance&nbsp;variables&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
<dl><dt><strong>__weakref__</strong></dt>
<dd><tt>list&nbsp;of&nbsp;weak&nbsp;references&nbsp;to&nbsp;the&nbsp;object&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
<hr>
Data and other attributes defined here:<br>
<dl><dt><strong>TRANSID_PREFIX</strong> = 'web'</dl>

</td></tr></table></td></tr></table><p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#55aa55">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Data</strong></big></font></td></tr>
    
<tr><td bgcolor="#55aa55"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><strong>string_types</strong> = (&lt;type 'basestring'&gt;,)</td></tr></table>
