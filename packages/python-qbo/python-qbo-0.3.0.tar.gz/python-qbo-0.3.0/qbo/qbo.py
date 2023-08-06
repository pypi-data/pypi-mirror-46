from typing import List
from urllib.parse import urljoin
from uuid import UUID

import requests
import urllib3
from urllib3 import exceptions

from .utils import parse_int

urllib3.disable_warnings(exceptions.InsecureRequestWarning)


class MachineInfo(object):
    def __init__(self, parsed_json: dict):
        self._serial_number = parsed_json['serialNumber']
        self._mac_address = parsed_json['macAddress']
        self._version = parsed_json['version']

    @property
    def serial_number(self) -> str:
        return self._serial_number

    @property
    def mac_address(self) -> str:
        return self._mac_address

    @property
    def version(self) -> str:
        return self._version


class MaintenanceStatus(object):
    def __init__(self, parsed_json: dict):
        self._maximum_descale_value = parse_int(parsed_json['maximumDescaleValue'])
        self._current_descale_value = parse_int(parsed_json['currentDescaleValue'])
        self._machine_descale_status = parse_int(parsed_json['machineDescaleStatus'])
        self._maximum_clean_value = parse_int(parsed_json['maximumCleanValue'])
        self._current_clean_value = parse_int(parsed_json['currentCleanValue'])
        self._machine_clean_status = parse_int(parsed_json['machineCleanStatus'])
        self._rinsing_status = parse_int(parsed_json['rinsingStatus'])

    @property
    def maximum_descale_value(self) -> int:
        return self._maximum_descale_value

    @property
    def current_descale_value(self) -> int:
        return self._current_descale_value

    @property
    def machine_descale_status(self) -> int:
        return self._machine_descale_status

    @property
    def descale_percent(self) -> float:
        return self.current_descale_value / self.maximum_descale_value

    @property
    def maximum_clean_value(self) -> int:
        """Returns the amount of coffees after which a cleaning should be done."""
        return self._maximum_clean_value

    @property
    def current_clean_value(self) -> int:
        """Return the amount of coffees brewed since the last cleaning."""
        return self._current_clean_value

    @property
    def machine_clean_status(self) -> int:
        return self._machine_clean_status

    @property
    def clean_percent(self) -> float:
        return self.current_clean_value / self.maximum_clean_value

    @property
    def rinsing_status(self):
        return self._rinsing_status


class Recipe(object):
    def __init__(self, parsed_json):
        self._name = parsed_json['name']
        self._uid = UUID(parsed_json['uid'])
        self._uses_hot_milk = parse_int(parsed_json['usesHotMilk']) == 1

    @property
    def name(self) -> str:
        return self._name

    @property
    def uid(self) -> UUID:
        return self._uid

    @property
    def uses_hot_milk(self) -> bool:
        return self._uses_hot_milk


class Qbo(object):
    def __init__(self, qbo_url: str):
        self._qbo_url = qbo_url
        self._headers = {
            "accept": "application/json"
        }

    def machine_info(self) -> MachineInfo:
        req_url = urljoin(self._qbo_url, "machineInfo")
        resp = requests.get(req_url, headers=self._headers, verify=False)
        parsed_json = resp.json()
        return MachineInfo(parsed_json)

    def maintenance_status(self) -> MaintenanceStatus:
        req_url = urljoin(self._qbo_url, "status/maintenance")
        resp = requests.get(req_url, headers=self._headers, verify=False)
        parsed_json = resp.json()
        return MaintenanceStatus(parsed_json)

    def name(self) -> str:
        req_url = urljoin(self._qbo_url, "settings/name")
        resp = requests.get(req_url, headers=self._headers, verify=False)
        parsed_json = resp.json()
        return parsed_json['name']

    def recipes(self) -> List[Recipe]:
        req_url = urljoin(self._qbo_url, "recipes")
        resp = requests.get(req_url, headers=self._headers, verify=False)
        parsed_json = resp.json()
        return [Recipe(parsed_json[index]) for index in parsed_json]
