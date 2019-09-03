"""Dyson Pure Cool Link library."""

import Domoticz
import requests
from requests.auth import HTTPBasicAuth

DYSON_API_URL = "api.cp.dyson.com"

class DysonAccount:
    """Dyson account."""

    def __init__(self, email, password, country):
        """Create a new Dyson account.

        :param email: User email
        :param password: User password
        :param country: 2 characters language code
        """
        self._email = email
        self._password = password
        self._country = country
        self._logged = False
        self._auth = None

    def login(self):
        """Login to dyson web services."""
        request_body = {
            "Email": self._email,
            "Password": self._password
        }
        login = requests.post(
            "https://{0}/v1/userregistration/authenticate?country={1}".format(
                DYSON_API_URL, self._country), request_body, verify=False)
        if login.status_code == requests.codes.ok:
            json_response = login.json()
            self._auth = HTTPBasicAuth(json_response["Account"],
                                       json_response["Password"])
            self._logged = True
        else:
            self._logged = False
        return self._logged

    def devices(self):
        """Return all devices linked to the account."""
        if self._logged:
            device_response = requests.get(
                "https://{0}/v1/provisioningservice/manifest".format(
                    DYSON_API_URL), verify=False, auth=self._auth)
            devices = []
            for device in device_response.json():
                Domoticz.Debug("Device returned from Dyson: "+device+"'")
            return devices
        else:
            Domoticz.Log("Not logged to Dyson Web Services.")
            #raise DysonNotLoggedException()

    @property
    def logged(self):
        """Return True if user is logged, else False."""
        return self._logged