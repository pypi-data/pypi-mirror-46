from staros import StarClient
import json

ddd = StarClient("starscript", "$rfv3EDC", "172.24.214.17", 22)

hh = [
    '172.24.214.17',
    '172.24.184.9',
    '172.24.221.20',
    '172.25.214.17',
    '172.26.214.17',
    '172.27.214.17',
    '172.28.214.17',
    '172.29.214.17',
    '172.25.184.1',
    '172.26.184.1',
    '172.28.184.1',
    '172.29.184.1',
    '172.28.214.42',
    '172.28.214.43',
    '172.28.214.44',
    '172.28.214.45'
]
jjj = ddd.find_subs_core_list_imsi('257027518529391', hh)
#jjj = ddd.find_subs_core_list('375298766719', hh)

print json.dumps(jjj, indent=4, sort_keys=True)
