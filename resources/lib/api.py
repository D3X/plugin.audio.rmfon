#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2012 Tristan Fischer (sphere@dersphere.de)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import json
from html import unescape
from urllib.request import Request, urlopen
from xml.etree import ElementTree


class ApiError(Exception):
    pass


class Api(object):
    URL = "http://rmfon.pl/json/stations.txt"

    def __init__(self, logger):
        self.stations = None
        self.logger = logger

    def get_stations(self):
        if self.stations is None:
            try:
                self.logger.info("Fetching stations list")
                stations_json = urlopen(Request(self.URL)).read()
            except Exception:
                raise ApiError()
            stations = json.loads(stations_json)
            self.stations = []
            for station in stations:
                station_obj = Station(logger=self.logger, **station)
                self.stations.append(station_obj)

        return self.stations

    def get_station(self, api_id):
        for station in self.get_stations():
            if station.api_id == api_id:
                return station
        raise ApiError()


class Station(object):
    URL = "http://www.rmfon.pl/stacje/flash_aac_{api_id}.xml.txt"

    def __init__(self, logger, **kwargs):
        self.logger = logger
        self.thumbnail = None
        self.sources = None

    def get_sources(self):
        if self.sources is None:
            url = self.URL.format(api_id=self.api_id)

            try:
                self.logger.info("Fetching sources list")
                sources_xml = urlopen(Request(url)).read()
            except Exception:
                raise ApiError()
            tree = ElementTree.fromstring(sources_xml)

            self.sources = sorted(item.text or "" for item in tree.findall("./item"))

        return self.sources
