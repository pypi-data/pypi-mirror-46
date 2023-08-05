from iosxe import IosClient
import json

ddd = IosClient("soapgw2", "eb5Swd8Yhq2Snd3eD", "172.24.223.149", 22)

print ddd.get_cpu_load()

jjj = ddd.get_binding_by_ip("100.70.2.1")
print json.dumps(jjj, indent=4, sort_keys=True)

print jjj["mac"] + "  " + jjj["iwaginterface"] + "  " + jjj["aphostname"] + "  " + jjj["SSID"]
