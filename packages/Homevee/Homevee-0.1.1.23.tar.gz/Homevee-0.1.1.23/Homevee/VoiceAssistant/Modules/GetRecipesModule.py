#!/usr/bin/python
# -*- coding: utf-8 -*-
from Homevee.Functions.chefkoch_api import search_recipes
from Homevee.VoiceAssistant.Modules import VoiceModule


class VoiceGetRecipesModule(VoiceModule):
    def get_pattern(self, db):
        return [
            ['zeig', 'mir', 'rezepte', ['über', 'für', 'zu', 'von']]
        ]

    def get_label(self):
        return "recipes"

    def run_command(self, username, text, context, db):
        return self.voice_recipes(username, text, context, db)

    def voice_recipes(self, username, text, context, db):
        words = text.split(" ")

        keyword = None
        found = False
        for word in words:
            if found:
                if keyword is None:
                    keyword = word
                else:
                    keyword = keyword + " " + word

            if word in ['über', 'für', 'zu', 'von']:
                found = True

        recipes = search_recipes(keyword, 5)

        recipe_data = []

        for item in recipes:
            recipe = item['recipe']

            recipe_data.append({'name':recipe['title']})

        text = None
        for item in recipe_data:
            if text is None:
                text = item['name']
            else:
                text = text + ", " + item['name']

        return {'msg_speech': 'Rezepte: '+text, 'msg_text': 'Rezepte: '+text}