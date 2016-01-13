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
from xbmcswift2 import Plugin
from resources.lib.api import Api, ApiError


plugin = Plugin()
api = Api(logger=plugin.log)


@plugin.route('/')
def show_root_menu():
    items = [
        {
            'label': station.name,
            'path': plugin.url_for('play', api_id=station.api_id),
        }
        for station in api.get_stations()
    ]
    return plugin.finish(items)


@plugin.route('/play/<api_id>')
def play(api_id):
    station = api.get_station(api_id)
    items = [
        {
            'label': '{station} ({url})'.format(station=station.name, url=source),
            'thumbnail': station.thumbnail,
            'path': source,
            'is_playable': True,
        }
        for source in station.get_sources()
    ]
    return plugin.finish(items)


if __name__ == '__main__':
    try:
        plugin.run()
    except ApiError:
        plugin.notify('Network error')
