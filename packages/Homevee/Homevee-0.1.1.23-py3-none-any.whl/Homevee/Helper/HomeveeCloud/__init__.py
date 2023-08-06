import json

from Homevee.Helper.HomeveeCloud.CloudAPI import CloudAPI
from Homevee.Helper.HomeveeCloud.Exception import APINotAuthenticatedException, APIErrorException


class HomeveeCloudWrapper():
    def __init__(self, remote_id=None, access_token=None):
        self.cloud_api = CloudAPI(remote_id, access_token)

        self.remote_id = self.cloud_api.remote_id
        self.access_token = self.cloud_api.access_token

    def is_premium(self):
        response = self.cloud_api.do_get("/ispremium/"+self.remote_id, {})
        data = self.check_response(response)
        return data['is_premium']

    def send_push_notification(self, registration_ids, message_data):
        response = self.cloud_api.do_put("/sendnotification",
                                         {'registration_ids': registration_ids,
                                          'message_data': message_data})
        data = self.check_response(response)
        return data['status']

    def set_ip(self, ip):
        response = self.cloud_api.do_put("/setlocalip/"+self.remote_id, {'ip': ip})
        data = self.check_response(response)
        return data['status']

    def set_cert(self, cert):
        response = self.cloud_api.do_put("/setlocalcert/"+self.remote_id, {'cert': cert})
        data = self.check_response(response)
        return data['status']

    def get_ip(self):
        response = self.cloud_api.do_get("/getlocalip/"+self.remote_id, {})
        data = self.check_response(response)
        return data['local_ip']

    def get_cert(self):
        response = self.cloud_api.do_get("/getlocalcert/"+self.remote_id, {})
        data = self.check_response(response)
        return data['local_cert']

    def get_cloud_cert(self, cloud_ip):
        response = self.cloud_api.do_get("/getcloudcert/"+cloud_ip, {})
        data = self.check_response(response)
        return data['cloud_cert']

    def get_used_cloud(self):
        response = self.cloud_api.do_get("/getusedcloud/"+self.remote_id, {})
        data = self.check_response(response)
        return data['cloud']

    def get_cloud_to_use(self):
        response = self.cloud_api.do_get("/getcloudtouse/"+self.remote_id, {})
        data = self.check_response(response)
        return data['cloud']

    def check_response(self, response):
        if response is None:
            raise APIErrorException("API-Call not successful")

        if response.status_code == 401:
            raise APINotAuthenticatedException("Invalid credentials given")

        if response.status_code != 200:
            raise APIErrorException("API-Call not successful")

        return json.loads(response.response)