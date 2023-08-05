#!/usr/bin/python


import functions
import influxdb

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

    def ping_check(self):
        resp = functions.check_ping()
        return resp


class ArdUnbound:
    def __init__(self, telegram_token, telegram_chat_id):
        self.test = "test"
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

    def processes_check(self):
        stat = functions.get_modules_status()
        hostn = functions.get_hostname()
        if stat["unbound"] < 50:
            mess1 = "DNS " + hostn + " ERROR. Some Unbound processes are failed"
            functions.send_telegr(mess1, self.telegram_chat_id, self.telegram_token)

        if stat["bfd_c"] < 6:
            mess2 = "DNS " + hostn + " ERROR. Some BFD processes are failed"
            functions.send_telegr(mess2, self.telegram_chat_id, self.telegram_token)

        if stat["bird"] < 1:
            mess3 = "DNS " + hostn + " ERROR. BGP IPv4 process failed"
            functions.send_telegr(mess3, self.telegram_chat_id, self.telegram_token)

        if stat["zabbix"] < 1:
            mess4 = "DNS " + hostn + " ERROR. Zabbix Agent IPv4 process failed"
            functions.send_telegr(mess4, self.telegram_chat_id, self.telegram_token)

        if stat["bird6"] < 1:
            mess5 = "DNS " + hostn + " ERROR. BGP IPv6 process failed"
            functions.send_telegr(mess5, self.telegram_chat_id, self.telegram_token)


class ArdInflux:
    def __init__(self, influxurl):
        self.influxurl = influxurl

    def unbound_stat_to_influx(self):
        hostname = functions.get_hostname()
        data = functions.get_data_from_unbound_stat()
        influxdb.push_unbound_metrics(data, self.influxurl, hostname)

