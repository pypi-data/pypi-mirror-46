#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.VoiceAssistant.Modules import VoiceModule

class VoiceGetSummaryModule(VoiceModule):
    def get_pattern(self, db):
        #todo declare pattern for summary
        return []

    def get_label(self):
        return "getsummary"

    def run_command(self, username, text, context, db):
        pass

    def get_voice_summary(username, text, context, db):
        return {'msg_speech': 'Get Summary', 'msg_text': 'Get Summary'}