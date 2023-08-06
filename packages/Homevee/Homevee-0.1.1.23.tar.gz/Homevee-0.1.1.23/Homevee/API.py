#!/usr/bin/python
# -*- coding: utf-8 -*-
import traceback

from Homevee import Helper, Updater
from Homevee.DeviceAPI.set_modes import set_modes
from Homevee.Functions import ar_control, people_classifier
from Homevee.Helper import translations
from .DeviceAPI import dimmer, energy_data
from .DeviceAPI.blind_control import set_blinds, get_all_blinds, set_room_blinds
from .DeviceAPI.get_modes import *
from .DeviceAPI.heating import get_thermostats, control_room_heating, heating_control
from .DeviceAPI.rfid_control import get_rfid_tags, add_edit_rfid_tag, run_rfid_action
from .DeviceAPI.rgb_control import rgb_control
from .DeviceAPI.wake_on_lan import *
# from Functions import people_classifier, ar_control
# from Functions.people_classifier import *
from .Functions import room_data, weather, events, chat, shopping_list, media_center, gps_data, nutrition_data
from .Functions.calendar import *
from .Functions.condition_actions.actions import run_scene
from .Functions.graph_data import *
from .Functions.home_budget import get_home_budget_data, add_edit_home_budget_data, delete_home_budget_data, \
    get_home_budget_data_day_items, get_home_budget_data_graph
from .Functions.sensor_data import *
from .Functions.system_info import *
from .Functions.tv_data import *
from .Helper.helper_functions import load_remote_data, save_remote_data, set_remote_control_enabled, \
    connect_remote_id_with_account
from .Manager import dashboard, mqtt_connector, places
from .Manager.api_key import *
from .Manager.automation import *
from .Manager.custom_voice_commands import get_voice_commands, add_edit_voice_command, delete_voice_command
from .Manager.device import *
from .Manager.gateway import *
from .Manager.heating_scheme import *
from .Manager.persons import get_persons, add_edit_person
from .Manager.room import *
from .Manager.scenes import add_edit_scene, delete_scene, get_all_scenes
from .Manager.smart_speaker import get_smart_speakers
from .Manager.user import *
from .VoiceAssistant import *
from .VoiceAssistant.VoiceReplaceManager import *


class API:
    def __init__(self):
        return

    def process_data(self, data, db):
        try:
            username = data['username']
            password = data['password']

            user = User.load_username_from_db(username, db)
            verified = user.verify(password)

            if 'language' in data and data['language'] is not None:
                language = data['language']
            else:
                language = translations.LANGUAGE

            if not verified:
                return json.dumps({'result': 'wrongdata'})

            try:
                return self.handle_request(user, data, db)
            except Exception as e:
                if(Logger.IS_DEBUG):
                    traceback.print_exc()
                return
        except Exception as e:
            if(Logger.IS_DEBUG):
                    traceback.print_exc()
            if 'status' in data:
                if data['status'] == 'connectionok':
                    Logger.log('connectionok')


    def handle_request(self, user, request, db):
        response = None

        #print(user, request)

        action = request['action']
        username = request['username']

        if 'language' in request:
            language = request['language']
        else:
            language = translations.LANGUAGE

        if ('user_last_location' in request and request['user_last_location'] is not None):
            user_last_location = json.loads(request['user_last_location'])
        else:
            user_last_location = None

        # Roomdata
        if action == "login":
            rooms = room_data.get_rooms(user, db)

            remote_id = Database.get_server_data("REMOTE_ID", db)

            response = {'remote_id': remote_id, 'rooms': rooms['rooms']}

        # Roomdata
        elif action == "getrooms":
            response = room_data.get_rooms(user, db)
        elif action == "getroomdata":
            response = room_data.get_room_data(user, request['room'], db)

        # Remote-ID
        elif action == "setremotedata":
            response = save_remote_data(user, request['remote_id'], request['linked_account'], db)
        elif action == "getremotedata":
            response = load_remote_data(user, db)
        elif action == "setremotecontrolenabled":
            response = set_remote_control_enabled(user, request['enabled'], db)
        elif action == "connectremoteidwithaccount":
            response = connect_remote_id_with_account(user, request['accountname'], request['accountsecret'], db)

        # Kalender
        elif action == "getcalendaritemdates":
            response = get_calendar_item_dates(user, request['year'], db)
        elif action == "getcalendardayitems":
            response = get_calendar_day_items(user, request['date'], db)
        elif action == "addeditcalendarentry":
            response = add_edit_entry(user, request['id'], request['name'], request['date'], request['start'],
                                      request['end'], request['note'], request['address'], db)
        elif action == "deletecalendarentry":
            response = delete_entry(user, request['id'], db)

        # Personen
        elif action == "getpersons":
            response = get_persons(db)
        elif action == "addeditperson":
            response = add_edit_person(user, request['id'], request['name'], request['nickname'], request['address'],
                                       request['latitude'], request['longitude'], request['phonenumber'],
                                       request['birthdate'], db)

        # RGB Lampen
        elif action == "setrgb":
            response = rgb_control(user, request['type'], request['id'], request['mode'], request['brightness'],
                                   request['color'], db)

        # RFID
        elif action == "getrfidtags":
            response = get_rfid_tags(user, db)
        elif action == "addeditrfidtag":
            response = add_edit_rfid_tag(user, request['name'], request['uuid'], request['type'], request['id'], db)
        elif action == "deleterfidtag":
            response = add_edit_rfid_tag(user, request['uuid'], db)
        elif action == "runrfidaction":
            response = run_rfid_action(user, request['uuid'], db)

        # Events
        elif action == "getevents":
            type = None
            if "type" in request:
                type = request['type']
            response = events.get_events(user, type, request['limit'], request['offset'], db)
        elif action == "geteventtypes":
            response = events.get_event_types(db)
        elif action == "addevent":
            response = events.add_event(request['type'], request['text'], db)
        elif action == "getunseenevents":
            response = events.get_unseen_events(user, db)

        # Permissions
        elif action == "getpermissions":
            response = Helper.permissions.get_permissions(request['user'], db)
        elif action == "setpermissions":
            response = Helper.permissions.set_permissions(user, request['user'], request['permissions'], db)

        # MQTT Anlernen => generate_device_data()
        elif action == "generatedevicedata":
            response = mqtt_connector.generate_device_data(user, request['location'], db)
        elif action == "savemqttdevice":
            response = mqtt_connector.save_mqtt_device(user, request['type'], request['location'], request['id'],
                                                       request['devicedata'], db)

        # Jalousie-Steuerung
        elif action == "setblinds":
            response = set_blinds(user, request['type'], request['id'], request['value'], db)
        elif action == "setroomblinds":
            response = set_room_blinds(user, request['location'], request['value'], db)
        elif action == "getallblinds":
            response = get_all_blinds(user, db)

        # Weather
        elif action == "getweather":
            response = weather.get_weather(int(request['daycount']), db)
        elif action == "getweathercitylist":
            response = weather.get_weather_city_list(db)
        elif action == "setweathercityid":
            response = weather.set_weather_city_id(user, request['id'])

        # Get graph data
        elif action == "getgraphdata":
            response = get_graph_data(user, request['room'], request['type'], request['id'], request['von'], request['bis'],
                                      db)

        # Get modes, set modes
        elif action == "getmodes":
            response = get_modes(user, request['room'], request['type'], request['device'], db)
        elif action == "setmodes":
            response = set_modes(user, request['type'], request['device'], request['zustand'], db)

        # Dimmer
        elif action == "setdimmer":
            response = dimmer.set_dimmer(user, request['type'], request['id'], request['value'], db)

        # Wake on Lan
        elif action == "wakeonlan":
            response = wake_on_lan(user, request['id'], db)
        elif action == "startxboxone":
            response = wake_xbox_on_lan(user, request['id'], db)

        # Systeminfo
        elif action == "getsysteminfo":
            response = get_system_info()

        # Chat
        elif action == "getchatmessages":
            response = chat.get_chat_messages(user, request['time'], request['limit'], db)
        elif action == "getchatimage":
            response = chat.get_chat_image(user, request['imageid'], db)
        elif action == "sendchatmessage":
            response = chat.send_chat_message(user, request['data'], db)

        # Dashboard
        elif action == "getuserdashboarditems":
            response = dashboard.get_user_dashboard_items(user, db)
        elif action == "getuserfavouritedevices":
            response = dashboard.get_user_favourite_devices(user, db)
        elif action == "edituserdashboard":
            response = dashboard.edit_user_dashboard(user, request['dashboarddata'], db)
        elif action == "getuserdashboard":
            response = dashboard.get_user_dashboard(user, db)

        # Energie-Daten
        elif action == "getenergydata":
            response = energy_data.get_energy_data(user, request['room'], request['devicetype'], request['deviceid'],
                                                   request['von'], request['bis'], db)
        elif action == "getdeviceenergydata":
            response = energy_data.get_device_energy_data(user, request['room'], request['devicetype'], request['deviceid'],
                                                          request['von'], request['bis'], db)
        elif action == "getenergycourse":
            response = energy_data.get_energy_course(user, request['room'], request['von'], request['bis'], db)
        elif action == "setpowercost":
            response = energy_data.set_power_cost(user, request['cost'], db)
        elif action == "getpowercost":
            response = energy_data.get_power_cost(user, db)

        # Sensor-Daten
        elif action == "getsensordata":
            response = get_sensor_data(user, request['room'], db)
        # User-Manager
        elif action == "getusers":
            response = get_users(user, db)
        elif action == "deleteuser":
            response = delete_user(user, request['name'], db)
        elif action == "addedituser":
            response = add_edit_user(user, request['name'], request['psw'], request['ip'],
                                     request['permissions'], db)

        # Gateway-Manager
        elif action == "getgateways":
            response = get_gateways(user, db)
        elif action == "addeditgateway":
            response = add_edit_gateway(user, request['type'], request['usr'], request['psw'], request['changepw'],
                                        request['ip'], request['port'], request['gateway_type'], db)
        elif action == "deletegateway":
            response = delete_gateway(user, request['type'], db)
        elif action == "getgatewaydevices":
            response = get_gateway_devices(user, request['type'], db)
        elif action == "connectgateway":
            response = connect_gateway(user, request['type'], request['ip'], db)

        # TV-Programm
        elif action == "settvchannels":
            response = set_tv_channels(user, request['channels'], db)
        elif action == "gettvplan":
            response = get_tv_plan(user, request['time'], db)
        elif action == "getalltvchannels":
            response = get_all_tv_channels(user, db)

        # Einkaufsliste
        elif action == "getshoppinglist":
            response = shopping_list.get_shopping_list(user, db)
        elif action == "addeditshoppinglistitem":
            response = shopping_list.add_edit_shopping_list_item(user, request['id'],
                                                                 request['amount'], request['name'], db)
        elif action == "deleteshoppinglistitem":
            response = shopping_list.delete_shopping_list_item(user, request['id'], db)

        # Sprachassistent
        elif action == "voicecommand":
            response = VoiceAssistant().do_voice_command(user, request['text'], user_last_location, None, db, language)
            # response = do_voice_command(user, request['text'], user_last_location, None, db, language)
        elif action == "getvoicereplaceitems":
            response = get_voice_replace_items(user, db)
        elif action == "addeditvoicereplaceitem":
            response = add_edit_voice_replace_item(user, request['replacewith'], request['itemstoreplace'], db)
        elif action == "deletevoicereplaceitem":
            response = delete_voice_replace_item(user, request['replacewith'], db)

        # Smart Speakers
        elif action == "getsmartspeakers":
            response = get_smart_speakers(user, db)

        # Heizpläne
        elif action == "addeditheatingschemeitem":
            response = add_edit_heating_scheme_item(user, request['id'], request['time'], request['value'],
                                                    request['active'], request['days'], request['data'], db)
        elif action == "deleteheatingschemeitem":
            response = delete_heating_scheme_item(user, request['id'], db)
        elif action == "getheatingschemeitems":
            response = get_heating_scheme_items(user, request['day'], request['rooms'], db)
        elif action == "setheatingschemeitemactive":
            response = set_heating_scheme_item_active(user, request['id'], request['active'], db)
        elif action == "getheatingschemeitemdata":
            response = get_heating_scheme_item_data(user, request['id'], db)
        elif action == "setheatingschemeactive":
            response = set_heating_scheme_active(user, request['active'], db)
        elif action == "isheatingschemeactive":
            response = is_heating_scheme_active(user, db)

        # API-Keys
        elif action == "getapikeydata":
            response = get_all_api_key_data(user, db)
        elif action == "setapikey":
            response = set_api_key(user, request['service'], request['apikey'], db)

        # Media Center
        elif action == "getmediacenters":
            response = media_center.get_media_centers(user, db)
        elif action == "mediacentercontrol":
            response = media_center.media_remote_action(request['type'], request['id'], request['remoteaction'], db)
        elif action == "mediacentersendtext":
            response = media_center.media_center_send_text(request['type'], request['id'], request['text'], db)
        elif action == "mediacentermusic":
            response = media_center.get_media_center_music(request['type'], request['id'],
                                                           request['limit'], request['offset'], db)
        elif action == "mediacenterartists":
            response = media_center.get_media_center_artists(request['type'], request['id'],
                                                             request['limit'], request['offset'], db)
        elif action == "mediacenteralbums":
            response = media_center.get_media_center_albums(request['type'], request['id'],
                                                            request['limit'], request['offset'], db)
        elif action == "mediacentermusicgenres":
            response = media_center.get_media_center_music_genres(request['type'], request['id'],
                                                                  request['limit'], request['offset'], db)
        elif action == "mediacentertvshows":
            response = media_center.get_media_center_shows(request['type'], request['id'],
                                                           request['limit'], request['offset'], db)
        elif action == "mediacentertvshowseasons":
            response = media_center.get_media_center_show_seasons(request['type'], request['id'], request['limit'],
                                                                  request['offset'], request['showid'], db)
        elif action == "mediacentertvshowepisodes":
            response = media_center.get_media_center_show_episodes(request['type'], request['id'], request['limit'],
                                                                   request['offset'], request['showid'],
                                                                   request['seasonid'], db)
        elif action == "mediacentermovies":
            response = media_center.get_media_center_movies(request['type'], request['id'],
                                                            request['limit'], request['offset'], db)
        elif action == "mediacentermoviegenres":
            response = media_center.get_media_center_movie_genres(request['type'], request['id'],
                                                                  request['limit'], request['offset'], db)
        elif action == "mediacenterplaying":
            response = media_center.get_media_menter_playing(request['type'], request['id'], db)

        # Firebase-Token aktualisieren
        elif action == "updatefcmtoken":
            response = set_user_fcm_token(user, request['token'], db)

        # Heizung
        elif action == "heatingcontrol":
            response = heating_control(user, request['type'], request['id'], request['value'], db)
        elif action == "controlroomheating":
            response = control_room_heating(user, request['location'], request['value'], db)
        elif action == "getthermostats":
            response = get_thermostats(user, request['room'], db)

        # Räume
        elif action == "addeditroom":
            response = add_edit_room(user, request['roomname'], request['location'], request['icon'], db)
        elif action == "moveitemsanddeleteoldroom":
            response = move_items_and_delete_old_room(user, request['oldroom'], request['newroom'], db)
        elif action == "deleteroomwithitems":
            response = delete_room_with_items(user, request['location'], db)
        elif action == "deleteroom":
            response = delete_room(user, request['location'], db)

        # Geräte-Manager
        elif action == "addeditdevice":
            response = add_edit_device(user, request['id'], request['type'], request['data'], db)
        elif action == "deletedevice":
            response = delete_device(user, request['type'], request['id'], db)
        elif action == "getdevicedata":
            response = get_device_data(user, request['type'], request['id'], db)

        # AR-Control
        elif action == "arcontrol":
            response = ar_control.ar_control(user, request['imagedata'], db)
        elif action == "getarcontrolclasses":
            response = ar_control.get_ar_control_classes(db)
        elif action == "savearcontrolclass":
            response = ar_control.save_ar_control_class(user, request['id'], request['data'], request['classname'], db)
        elif action == "getarcontrolclassimages":
            response = ar_control.get_ar_control_class_images(request['class'], request['show'], request['offset'], db)
        elif action == "startarcontroltraining":
            response = ar_control.start_ar_training(user, db)
        elif action == "changearcontrolimageclass":
            response = ar_control.change_ar_image_class(request['ids'], request['newclass'], db)
        elif action == "getarcontrolimages":
            response = ar_control.get_ar_control_image(request['id'], db)
        elif action == "getarimageclassifierperformancesettings":
            response = ar_control.get_performance_settings(user, db)
        elif action == "setarimageclassifierperformancesettings":
            response = ar_control.set_performance_settings(user, request['data'], db)
        elif action == "uploadarcontrolimages":
            response = ar_control.upload_images(user, request['data'], request['class'], db)
        elif action == "deletearcontrolimages":
            response = ar_control.delete_ar_control_images(request['ids'], db)

        # Gesichtserkennung
        elif action == "getpeopleclasses":
            response = people_classifier.get_people_classes(db)
        elif action == "savepeopleclass":
            response = people_classifier.save_people_class(user, request['id'], request['data'], request['classname'], db)
        elif action == "startpeopletraining":
            response = people_classifier.start_people_training(user, db)
        elif action == "getpeopleimageclassifierperformancesettings":
            response = people_classifier.get_performance_settings(user, db)
        elif action == "setpeopleimageclassifierperformancesettings":
            response = people_classifier.set_performance_settings(user, request['data'], db)
        elif action == "changepeopleclassifierimageclass":
            response = people_classifier.change_people_image_class(request['ids'], request['newclass'], db)
        elif action == "getpeopleclassifierimage":
            response = people_classifier.get_people_image(request['id'], db)
        elif action == "getpeopleclassifierimages":
            response = people_classifier.get_people_images(request['class'], request['show'], request['offset'], db)
        elif action == "uploadpeopleimages":
            response = people_classifier.upload_images(user, request['data'], request['class'], db)
        elif action == "classifyperson":
            response = people_classifier.classify_person(request['imagedata'], db)
        elif action == "deletepeopleimages":
            response = people_classifier.delete_people_images(request['ids'], db)

        # Automation
        elif action == "getautomationrules":
            response = get_automations(user, request['location'], db)
        elif action == "addeditautomationrule":
            response = add_edit_automation_rule(user, request['location'], request['id'], request['name'],
                                                request['triggerdata'], request['conditiondata'], request['actiondata'],
                                                request['isactive'], db)
        elif action == "deleteautomationrule":
            response = delete_automation_rule(user, request['id'], db)
        # Eigene Sprachbefehle
        elif action == "getvoicecommands":
            response = get_voice_commands(db)
        elif action == "addeditvoicecommand":
            response = add_edit_voice_command(user, request['id'], request['name'], request['command_data'],
                                              request['response_data'], request['action_data'], db)
        elif action == "deletevoicecommand":
            response = delete_voice_command(user, request['id'], db)
        # Szenen
        elif action == "getallscenes":
            response = get_all_scenes(user, db)
        elif action == "getscenes":
            response = get_scenes(user, request['location'], db)
        elif action == "addeditscene":
            response = add_edit_scene(user, request['id'], request['name'], request['location'], request['action_data'], db)
        elif action == "deletescene":
            response = delete_scene(user, request['id'], db)
        elif action == "runscene":
            response = run_scene(user, request['id'], db)
        # Haushaltskasse
        elif action == "gethomebudgetdata":
            response = get_home_budget_data(user, request['startdate'], db)
        elif action == "gethomebudgetdatadayitems":
            response = get_home_budget_data_day_items(user, request['date'], db)
        elif action == "gethomebudgetdatagraph":
            response = get_home_budget_data_graph(user, request['startdate'], request['enddate'], db)
        elif action == "addedithomebudgetdata":
            response = add_edit_home_budget_data(user, request['id'], request['date'], request['info'], request['amount'],
                                                 db)
        elif action == "deletehomebudgetdata":
            response = delete_home_budget_data(user, request['id'], db)
        # GPS data
        elif action == "updategps":
            response = gps_data.update_gps(user, request['time'], request['lat'], request['lng'], db)
        elif action == "getgpslocations":
            response = gps_data.get_gps_locations(user, db)
        # Places
        elif action == "addeditplace":
            response = places.add_edit_place(user, request['id'], request['name'], request['address'], request['latitude'],
                                             request['longitude'], db)
        elif action == "getmyplaces":
            response = places.get_my_places(user, db)
        elif action == "deleteplace":
            response = places.delete_place(user, request['id'], db)
        # Ernährungsmanager
        elif action == "submitfood":
            response = nutrition_data.submit_food(user, request['name'], request['calories'], request['portionsize'],
                                                  request['portionunit'], request['protein'], request['fat'],
                                                  request['saturated'], request['unsaturated'], request['carbs'],
                                                  request['sugar'], request['ean'], db)
        elif action == "getusernutritionoverview":
            response = nutrition_data.get_user_nutrition_overview(user, db)
        elif action == "getuserdaynutritionitems":
            response = nutrition_data.get_user_day_nutrition_items(user, request['date'], db)
        elif action == "addedituserdaynutritionitem":
            response = nutrition_data.add_edit_user_day_nutrition_item(user, request['id'], request['date'],
                                                                       request['daytime'], request['name'],
                                                                       request['eatenportionsize'], request['portionsize'],
                                                                       request['portionunit'],
                                                                       request['calories'], request['fat'],
                                                                       request['saturated'], request['unsaturated'],
                                                                       request['carbs'], request['sugar'],
                                                                       request['protein'], db)
        elif action == "loadnutritionmanagersettings":
            response = nutrition_data.load_user_settings(user, db)
        elif action == "deletefooditem":
            response = nutrition_data.delete_food_item(user, request['id'], db)
        elif action == "savenutritionmanagersettings":
            response = nutrition_data.save_user_settings(user, request['height'], request['weight'], request['birthdate'],
                                                         request['mode'], request['activity'], db)
        elif action == "movenutritionitem":
            response = nutrition_data.move_item(user, request['id'], request['date'], request['daytime'],
                                                request['deleteold'], db)
        # Updates
        elif action == "checkforupdates":
            response = Updater.check_for_updates()
        elif action == "updatesystem":
            response = Updater.do_homevee_update(user, db)
        else:
            return {'result': 'nosuchaction'}

        # Ausgeben
        return json.dumps(response)

        '''
        //Kalender
            case "getcalendaritems":
                $result = getCalendarItems($_POST['cal_user'], $db);
                break;
            case "getcalendaritemsforday":
                $result = getCalendarItemsForDay($_POST['USERNAME'], $_POST['date'], $db);
                break;
            case "getcalendardataformonth":
                $result = getCalendarDataForMonth($_POST['USERNAME'], $_POST['month'], $db);
                break;
            case "getcalendariteminfo":
                $result = getCalendarItemInfo($_POST['id'], $db);
                break;
            case "addeditcalendaritem":
                $result = addEditCalendarItem($_POST['id'], $_POST['name'],
                $_POST['start'], $_POST['end'], $_POST['note'], $_POST['repeat'], $_POST['participants'], $db);
                break;
            case "deletecalendaritem":
                $result = deleteCalendarItem($_POST['id'], $db);
                break;
        '''

        '''
            case "runscene":
                $result = runScene($_POST['room'], $_POST['name'], $db);
                break;
            case "createscene":
                $result = createScene($_POST['devices'], $_POST['rooms'], $_POST['types'], $_POST['values'],
                    $_POST['conditions'], $_POST['room'], $_POST['name'], $db);
                break;
            case "getscenes":
                $result = getScenes($_POST['room'], $db);
                break;
    
            //Noch nicht im Tutorial
            case "shouldshowmorninginfo":
                //$result = iotDeviceControl($_POST['device'], $_POST['room'], 'getinfo', "", $db);
                break;
            case "getmorninginfo":
                //$result = iotDeviceControl($_POST['device'], $_POST['room'], 'getinfo', "", $db);
                break;
            case "getmorninginfosettings":
                //$result = iotDeviceControl($_POST['device'], $_POST['room'], 'getinfo', "", $db);
                break;
            case "setmorninginfosettings":
                //$result = iotDeviceControl($_POST['device'], $_POST['room'], 'getinfo', "", $db);
                break;
            case "rfidvalidation":
                $result = rfidValidation($_POST['uid'], $db);
                break;
            case "rfidtrigger":
                $result = rfidTrigger($_POST['uid'], $_POST['triggerid'], $db);
                break;
            case "heatingcontrol":
                $result = heatingControl($_POST['room'], $_POST['type'], $_POST['id'], $_POST['value'], $db);
                break;
            case "getheatingdata":
                $result = getHeatingData($_POST['room'], $_POST['type'], $_POST['id'], $_POST['all_data'], $db);
                break;
            case "controldiydevice":
                $result = diyDeviceControl($_POST['device'], $_POST['room'], $_POST['diyaction'], $_POST['value'], $db);
                break;
            case "getdiyinfo":
                $result = diyDeviceControl($_POST['device'], $_POST['room'], 'getinfo', "", $db);
                break;
            case "getreeddata":
                $result = getReedData($_POST['room'], $_POST['type'], $_POST['id'], $db);
                break;
            case "addedittargetid":
                $result = addEditTargetID($_POST['user'], $_POST['deviceid'], $_POST['targetid'], $db);
                break;
            case "getpowermeterdata":
                $result = getSensorData($_POST['room'], $_POST['type'], $_POST['id'], $_POST['hide_einheit'], $db);
                break;
            case "getdimmer":
                $result = getDimmer($_POST['room'], $_POST['type'], $_POST['id'], $db);
                break;
            case "setdimmer":
                $result = setDimmer($_POST['room'], $_POST['type'], $_POST['id'], $_POST['value'], $db);
                break;
    
            //Stromverbrauch
            case "getenergydata":
                $result = getEnergyData($_POST['room'], $_POST['devicetype'], $_POST['deviceid'], $_POST['von'], $_POST['bis'], $db);
                break;
            case "getdeviceenergydata":
                $result = getDeviceEnergyData($_POST['type'], $_POST['device'], $_POST['von'], $_POST['bis'], $db);
                break;
            case "setpowercost":
                $result = setPowerCost($_POST['cost'], $db);
                break;
            case "getpowercost":
                $result = getPowerCost($db);
                break;
    
            //Überwachungskamera
            case "getsurveillancefootage":
                $result = getSurveillanceFootage($_POST['id'], $_POST['filterdata'], $_POST['offset'], $_POST['limit'], $db);
                break;
            case "getsurveillancethumbnail":
                $result = getSurveillanceThumbnail($_POST['id'], $db);
                break;
            case "getsurveillancefootagevideo":
                $result = getSurveillanceFootageVideo($_POST['id'], $db);
                break;
            case "getipcameradata":
                $result = getIpCameraData($_POST['room'], $_POST['id'], $db);
                break;
    
            //Türspion
            case "addpeepholeimages":
                $result = addPeepholeImages($_POST['imagedata'], $db);
                break;
            case "getpeepholeclassimages":
                $result = getPeepholeClassImages($_POST['class'], $_POST['show'], $_POST['offset'], $db);
                break;
            case "changepeepholeimageclass":
                $result = changePeepholeClass($_POST['ids'], $_POST['newclass'], $db);
                break;
            case "getpeepholeimage":
                $result = getPeepholeImage($_POST['id'], $db);
                break;
            case "addeditpeepholeclass":
                $result = addEditPeepHoleClass($_POST['id'], $_POST['name'], $db);
                break;
            case "deletepeepholeclass":
                $result = deletePeepHoleClass($_POST['id'], $db);
                break;
    
            //Bild-Klassifizierer Einstellungen
            case "getimageclassifierperformancesettings":
                $result = getImageClassifierPerformanceSettings($db);
                break;
            case "setimageclassifierperformancesettings":
                $result = setImageClassifierPerformanceSettings($_POST['data'], $db);
                break;
    
            //Manager
            case "getdevicedata":
                $result = getDeviceData($_POST['type'], $_POST['id'], $db);
                break;
            case "deletedevice":
                $result = deleteDevice($_POST['type'], $_POST['id'], $db);
                break;
            case "addeditdevice":
                $result = addEditDevice($_POST['id'], $_POST['type'], $_POST['data'], $db);
                break;
    
            //Kalender
            case "getcalendaritems":
                $result = getCalendarItems($_POST['cal_user'], $db);
                break;
            case "getcalendaritemsforday":
                $result = getCalendarItemsForDay($_POST['USERNAME'], $_POST['date'], $db);
                break;
            case "getcalendardataformonth":
                $result = getCalendarDataForMonth($_POST['USERNAME'], $_POST['month'], $db);
                break;
            case "getcalendariteminfo":
                $result = getCalendarItemInfo($_POST['id'], $db);
                break;
            case "addeditcalendaritem":
                $result = addEditCalendarItem($_POST['id'], $_POST['name'],
                $_POST['start'], $_POST['end'], $_POST['note'], $_POST['repeat'], $_POST['participants'], $db);
                break;
            case "deletecalendaritem":
                $result = deleteCalendarItem($_POST['id'], $db);
                break;
    
            //MediaCenter
            case "getmediacenters":
                $result = getMediaCenters($db);
                break;
            case "mediacentercontrol":
                $result = remoteAction($_POST['type'], $_POST['id'], $_POST['remoteaction'], $db);
                break;
            case "mediacentersendtext":
                $result = mediaCenterSendText($_POST['type'], $_POST['id'], $_POST['text'], $db);
                break;
            case "mediacentermusic":
                $result = getMediaCenterMusic($_POST['type'], $_POST['id'], $_POST['limit'], $_POST['offset'], $db);
                break;
            case "mediacenterartists":
                $result = getMediaCenterArtists($_POST['type'], $_POST['id'], $_POST['limit'], $_POST['offset'], $db);
                break;
            case "mediacenteralbums":
                $result = getMediaCenterAlbums($_POST['type'], $_POST['id'], $_POST['limit'], $_POST['offset'], $db);
                break;
            case "mediacentermusicgenres":
                $result = getMediaCenterMusicGenres($_POST['type'], $_POST['id'], $_POST['limit'], $_POST['offset'], $db);
                break;
            case "mediacentertvshows":
                $result = getMediaCenterShows($_POST['type'], $_POST['id'], $_POST['limit'], $_POST['offset'], $db);
                break;
            case "mediacentertvshowseasons":
                $result = getMediaCenterShowSeasons($_POST['type'], $_POST['id'], $_POST['limit'], $_POST['offset'], $_POST['showid'], $db);
                break;
            case "mediacentertvshowepisodes":
                $result = getMediaCenterShowEpisodes($_POST['type'], $_POST['id'], $_POST['limit'], $_POST['offset'], $_POST['showid'], $_POST['seasonid'], $db);
                break;
            case "mediacentermovies":
                $result = getMediaCenterMovies($_POST['type'], $_POST['id'], $_POST['limit'], $_POST['offset'], $db);
                break;
            case "mediacentermoviegenres":
                $result = getMediaCenterMovieGenres($_POST['type'], $_POST['id'], $_POST['limit'], $_POST['offset'], $db);
                break;
            case "mediacenterplaying":
                $result = getMediaCenterPlaying($_POST['type'], $_POST['id'], $db);
                break;
    
            //Update
            case "checkforupdates":
                $result = checkForUpdates($db);
                break;
            case "updatesystem":
                $result = updateSystem($db);
                break;
            '''