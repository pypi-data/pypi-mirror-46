# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from builtins import input

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
# pylint: disable=E0611
from iothub_service_client import IoTHubDeviceMethod, IoTHubError

# The service connection string to authenticate with your IoT hub.
# Using the Azure CLI:
# az iot hub show-connection-string --hub-name {your iot hub name}
CONNECTION_STRING = "HostName=Homevee-Cloud.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=8k64yd8mLPj4rCwQP6XnNPiKhbr4tStwSImct2hDXaM="
DEVICE_ID = "9QYWLEVU"

# Details of the direct method to call.
METHOD_NAME = "SetTelemetryInterval"
METHOD_PAYLOAD = "10"
TIMEOUT = 60

def iothub_devicemethod_sample_run():
    try:
        # Connect to your hub.
        iothub_device_method = IoTHubDeviceMethod(CONNECTION_STRING)

        # Call the direct method.
        response = iothub_device_method.invoke(DEVICE_ID, METHOD_NAME, METHOD_PAYLOAD, TIMEOUT)

        print ( "" )
        print ( "Device Method called" )
        print ( "Device Method name       : {0}".format(METHOD_NAME) )
        print ( "Device Method payload    : {0}".format(METHOD_PAYLOAD) )
        print ( "" )
        print ( "Response status          : {0}".format(response.status) )
        print ( "Response payload         : {0}".format(response.payload) )

        input("Press Enter to continue...\n")

    except IoTHubError as iothub_error:
        print ( "" )
        print ( "Unexpected error {0}".format(iothub_error) )
        return
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Python quickstart #2..." )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )
    print ( "    Device ID         = {0}".format(DEVICE_ID) )

    iothub_devicemethod_sample_run()