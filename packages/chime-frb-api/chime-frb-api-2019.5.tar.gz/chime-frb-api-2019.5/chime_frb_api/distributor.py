#!/usr/bin/env pythonAAOA
# -*- coding: utf-8 -*-

import requests
from chime_frb_api.api import API

class Distributor(API):
    def __init__(self, base_url: str = "http://frb-vsop.chime:8002"):
        API.__init__(self, base_url=base_url)

    def create_distributor(self, distributor_name: str):
        payload = {"distributor": distributor_name}
        return self._post("/distributor/", payload)

    def delete_distributor(self, distributor_name: str):
        return self._delete("/distributor/{}".format(distributor_name))

    def create_directory_scanning_distributor(
        self, distributor_name: str, directory: str, interval: int, retries: int
    ):
        payload = {
            "distributor": distributor_name,
            "directory": directory,
            "interval": interval,
            "retries": retries,
        }
        return self._post("/distributor/directory-scanner", payload)

    def deposit_work(self, distributor_name:str, work):
        payload = {"work": [work]}
        return self._post("/distributor/work/{}".format(distributor_name), payload)

    def get_work(self, distributor_name:str):
        return self._get("/distributor/work/{}".format(distributor_name))

    def conclude_work(self, distributor_name, work_name:str, work_status: bool):
        payload = {"work": work_name, "status": work_status}
        return self._post("/distributor/conclude-work/{}".format(distributor_name), payload)

    def get_status(self, distributor_name:str = None):
        if distributor_name is None:
            response = self._get("/distributor/status")
        else:
            response = self._get("/distributor/status/{}".format(distributor_name))
        return response






