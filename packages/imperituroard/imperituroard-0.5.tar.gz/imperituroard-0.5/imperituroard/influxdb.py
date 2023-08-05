import requests


def push_unbound_metrics(mass, url, database):
    data11 = ''
    for i in mass:
        if i != '':
            d1 = i.split("=")
            name = d1[0]
            val = d1[1]
            data11 = data11 + 'dns,host='+database+',name=' + name + ' value=' + val + '\n'
    requests.post(url, data11)
