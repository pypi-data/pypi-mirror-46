#!/usr/bin/python
# -*- coding: utf-8 -*-

class VoiceModule():
    def __init__(self, priority=1):
        self.priority = priority

    def get_context_key(self):
        return None

    def get_priority(self):
        return self.priority

    def get_pattern(self, db):
        return None

    def get_label(self):
        return None

    def run_command(self, username, text, context, db):
        pass

    #helper functions
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False