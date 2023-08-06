import json
from time import sleep

from iothub_client.iothub_client import IoTHubTransportProvider, IoTHubModuleClient, DeviceMethodReturnValue

from Homevee import API
from Homevee.Utils.Database import Database

METHOD_PROCESS_DATA = "ProcessData"

class CloudConnection():
    def __init__(self):
        self.protocol = IoTHubTransportProvider.MQTT

        self.msg_timeout = 1000
        self.timeout = 1000

        cloud_host_name = "Homevee-Cloud.azure-devices.net"
        device_id = Database.get_server_data("REMOTE_ID")
        shared_access_key = Database.get_server_data("CLOUD_ACCESS_KEY")

        self.connection_string = "HostName="+cloud_host_name+";DeviceId="+device_id+\
                                 ";SharedAccessKey="+shared_access_key

        self.client = self.init_client()

        return

    # This function will be called every time a method request is received
    def method_callback(self, method_name, payload, user_context):
        retval = DeviceMethodReturnValue()

        if method_name == METHOD_PROCESS_DATA:
            try:
                data = json.loads(payload)
                msg = API().process_data(data, Database.get_database_con())

                retval.response = msg
                retval.status = 200
            except:
                retval.status = 500
                retval.response = "{ \"Response\": \"Could not call method %s\" }" % METHOD_PROCESS_DATA
        else:
            retval.status = 404
            retval.response = "{ \"Response\": \"Method %s not found\" }" % method_name

        return retval

    def init_client(self):
        print(self.connection_string)
        client = IoTHubModuleClient(self.connection_string, self.protocol)
        #client.create_from_environment(IoTHubTransportProvider.MQTT)
        #client.set_module_method_callback(self.method_callback, 0)
        client.set_module_method_callback(self.method_callback, 0)
        return client

    @staticmethod
    def cloud_connection_loop():
        cloud_connection = CloudConnection()
        while(True):
            sleep(15)

    def device_method_callback(self, method_name, payload, user_context):
        global INTERVAL
        print("\nMethod callback called with:\nmethodName = %s\npayload = %s" % (method_name, payload))
        device_method_return_value = DeviceMethodReturnValue()
        if method_name == "SetTelemetryInterval":
            try:
                INTERVAL = int(payload)
                # Build and send the acknowledgment.
                device_method_return_value.response = "{ \"Response\": \"Executed direct method %s\" }" % method_name
                device_method_return_value.status = 200
            except ValueError:
                # Build and send an error response.
                device_method_return_value.response = "{ \"Response\": \"Invalid parameter\" }"
                device_method_return_value.status = 400
        else:
            # Build and send an error response.
            device_method_return_value.response = "{ \"Response\": \"Direct method not defined: %s\" }" % method_name
            device_method_return_value.status = 404
        return device_method_return_value

