#!/usr/bin/python
# -*- coding: utf-8 -*-

from Homevee.VoiceAssistant.Modules import VoiceModule


class VoiceGetTvScheduleModule(VoiceModule):
    def get_pattern(self, db):
        return [
            ['was',['kommt','ist','gibt','läuft'],['tv','fernsehen','fernseher']]
        ]

    def get_label(self):
        return "gettvschedule"

    def run_command(self, username, text, context, db):
        return self.get_tv(username, text, context, db)

    def get_tv(self, username, text, context, db):
        return {'msg_speech':'TV-Programm', 'msg_text':'TV-Programm'}