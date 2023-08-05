#!/usr/bin/python


import functions


class Ard:
    def __init__(self):
        self.test = "test"


    def send_telegram_message(self, message, chatid, token):
        functions.send_telegr(message, chatid, token)

    def get_modules_status(self):
        stat = functions.get_modules_status()
        return stat

    def get_hostname(self):
        hn = functions.get_hostname()
        return str(hn)
