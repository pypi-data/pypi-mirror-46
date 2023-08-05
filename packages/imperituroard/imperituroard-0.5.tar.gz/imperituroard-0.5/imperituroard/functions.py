#!/usr/bin/python


import re
import requests
import subprocess
import os


def send_telegr(message, chatid, token):
    r = requests.post(token, data={'chat_id': chatid, 'text': message})
    #print str(r.status_code)
    answr= {'status_code': str(r.status_code), 'reason': str(r.reason)}
    return answr


def get_path_to(app):
    p1 = subprocess.Popen(["which", app], stdout=subprocess.PIPE)
    output1 = p1.communicate()[0]
    return output1.split(".")[0].replace('\n', '')


def get_hostname():
    netst = get_path_to("cat")
    p1 = subprocess.Popen([netst, "/proc/sys/kernel/hostname"], stdout=subprocess.PIPE)
    output1 = p1.communicate()[0]
    return output1.split(".")[0]


def get_modules_status():
    netst = get_path_to("netstat")
    p = subprocess.Popen([netst, "-ntulp"], stdout=subprocess.PIPE)
    output = p.communicate()[0]
    a2 = re.findall(r'\s+\d+/(\S+)\s+', output)
    val2 = a2
    #print val2

    unbound = 0
    bfd_c = 0
    bird = 0
    zabbix = 0
    bird6 = 0

    cnt = 0
    while cnt < len(a2):
        i = a2[cnt]
        if i == 'unbound':
            unbound = unbound + 1
        elif i == 'bird':
            bird = bird + 1
        elif i == 'bfdd-beacon':
            bfd_c = bfd_c + 1
        elif i == 'zabbix_agentd':
            zabbix = zabbix + 1
        elif i == 'bird6':
            bird6 = bird6 + 1
        cnt = cnt + 1
    answer = {"unbound": unbound, "bfd_c": bfd_c, "bird": bird, "zabbix": zabbix, "bird6": bird6}
    return answer


def mac_parse(mac):
    a = mac.upper()
    pos = a[0] + a[1]
    if pos == "01":
        subscribers_mac = a[2] + a[3] + ":" + a[5] + a[6] + ":" + a[7] + a[8] + ":" + a[10] + a[11] + ":" + a[12] + a[13] + ":" + a[15] + a[16]
    else:
        subscribers_mac = a[0] + a[1] + ":" + a[2] + a[3] + ":" + a[5] + a[6] + ":" + a[7] + a[8] + ":" + a[10] + a[11] + ":" + a[12] + a[13]
    return subscribers_mac


def check_ping():
    hostname = "google.com"
    response = os.system("ping -c 7 " + hostname)
    # and then check the response...
    #print response
    if response == 0:
        pingstatus = "OK"
    else:
        pingstatus = "ERROR"
        #os.system("ifdown ens161;ifdown ens256")
    return pingstatus


def get_data_from_unbound_stat():
    netst = get_path_to("unbound-control")
    p = subprocess.Popen([netst, "stats"], stdout=subprocess.PIPE)
    output = p.communicate()[0]
    mass = str(output).split("\n")
    return mass

#[root@min26dns1 python]# which crontab
#/usr/bin/crontab
#[root@min26dns1 python]# which netstat
#/usr/bin/netstat
#[root@min26dns1 python]# which unbound-control