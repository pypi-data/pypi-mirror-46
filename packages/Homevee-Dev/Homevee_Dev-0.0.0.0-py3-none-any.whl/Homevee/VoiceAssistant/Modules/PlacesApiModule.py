#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.VoiceAssistant.Modules import VoiceModule

class VoicePlacesApiModule(VoiceModule):
    def get_pattern(self, db):
        return [
            [['wo', 'was'], 'ist', ['der', 'die', 'das'], ['nähste', 'nächste']]
        ]

    def get_label(self):
        return "placesapi"

    def run_command(self, username, text, context, db):
        return self.get_places(username, text, context, db)

    def get_places(self, username, text, context, db):
        return {'msg_speech': 'Places', 'msg_text': 'Places'}