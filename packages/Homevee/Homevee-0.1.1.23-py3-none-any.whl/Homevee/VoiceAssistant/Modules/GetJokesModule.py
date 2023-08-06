#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import traceback
import urllib.error
import urllib.parse
import urllib.request

from Homevee.Helper import Logger
from Homevee.VoiceAssistant import Helper
from Homevee.VoiceAssistant.Modules import VoiceModule


class VoiceGetJokesModule(VoiceModule):
    def get_pattern(self, db):
        return [
            [['erzähl','sag'],'witz'],
            ['klopf', 'klopf']
        ]

    def get_label(self):
        return "joke"

    def run_command(self, username, text, context, db):
        return self.get_joke(username, text, context, db)

    def get_joke(self, username, text, context, db):
        try:
            url = Helper.SMART_API_PATH + "/?action=joke&text=" + urllib.parse.quote(text.encode('utf8'))
            Logger.log(url)
            data = urllib.request.urlopen(url).read()

            data = data.decode('utf-8')

        except Exception as e:
            if(Logger.IS_DEBUG):
                traceback.print_exc()
            data = None

        if data is not None:
            return {'msg_speech': data, 'msg_text': data}
        else:
            result = self.get_error()
            return {'msg_speech': result, 'msg_text': result}

    def get_error(self):
        return random.choice([
            'Mir fällt gerade kein Witz ein.'
        ])