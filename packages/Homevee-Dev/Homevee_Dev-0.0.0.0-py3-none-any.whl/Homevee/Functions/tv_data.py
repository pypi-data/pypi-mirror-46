#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as etree

from Homevee.Item.Status import *
from Homevee.Utils.Database import Database


def get_tv_plan(user, type, db):
    try:
        tv_channels = get_tv_channels(user, db)

        if type == "2015":
            type = "heute2015"
        elif type == "2200":
            type = "heute2200"
        elif type == "jetzt":
            type = "jetzt"
        elif type == "tipps":
            type = "tipps"
        else:
            raise AttributeError("TV-Typ '" + type + "' nicht vorhanden")

        tv_shows = []

        link = "http://www.tvspielfilm.de/tv-programm/rss/" + type + ".xml"

        file = urllib.request.urlopen(link)
        data = file.read()
        file.close()

        #XML-Datei laden
        ergebnis = etree.fromstring(data)

        for item in ergebnis.find('channel').findall('item'):
            zeit, channel, name = item.find('title').text.split(" | ")

            description = item.find('description').text

            img = None
            #if item.find('image') is not None:
            img = item.find('enclosure').attrib['url']

            if type == "tipps" or ((tv_channels is None) or (channel in tv_channels)):
                tv_shows.append({'time': zeit, 'channel': channel, 'name': name, 'description': description, 'img': img})

        return tv_shows
    except:
        return None

def get_tv_channels(user, db):
    cur = db.cursor()
    Database.select_all("SELECT * FROM TV_CHANNELS WHERE USERNAME == :username", {'username': user.username})

    channels = []

    for channel in cur.fetchall():
        channels.append(channel['CHANNEL'])

    return channels

def get_all_tv_channels(user, db):
    selected_channels = get_tv_channels(user, db)

    #XML-Datei von Link laden
    link = "http://www.tvspielfilm.de/tv-programm/rss/jetzt.xml"

    file = urllib.request.urlopen(link)
    data = file.read()
    file.close()

    # XML-Datei laden
    ergebnis = etree.fromstring(data)

    channels = []
    for item in ergebnis.find('channel').findall('item'):
        zeit, channel, name = item.find('title').text.split(" | ")

        if (channels is None) or (channel not in channels):
            channels.append({'name': channel, 'selected': (channel in selected_channels)})

    return channels

def set_tv_channels(user, json_data, db):
    cur = db.cursor()
    Database.delete("DELETE FROM TV_CHANNELS WHERE USERNAME == :username", {'username': user.username})

    #Abfrage erfolgreich?
    if False:
        return Status(type=STATUS_ERROR).get_dict()
    else:
        channels = json.loads(json_data)

        for channel in channels:
            Database.insert("INSERT INTO TV_CHANNELS (USERNAME, CHANNEL) VALUES (?,?)",
                [user.username, channel])

        return Status(type=STATUS_OK).get_dict()