import requests

# api-endpoint 
URL = "http://192.168.0.44" + "/api/"
ZONEMAP = {1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}

#power_status
r = requests.get(url = URL + 'data/0') 
print(r.json()['data']['power'])

#set_power
r = requests.get(url = URL + 'power/1') 
print(r.json()['data']['power'])

#zone_status
r = requests.get(url = URL + 'data/200/z1') 
print(r.json()['data']['zone']['video_input'])

#set_zone_source
print(ZONEMAP.get(1))
r = requests.get(url = URL + 'control/switch/a/2') 
print(r.json()['data']['input_id'])

#set_all_zone_source
zones = {'a','b','c','d'}
for zone in zones:
    r = requests.get(url = URL + 'control/switch/' + zone + '/2') 
    print(r.json()['data']['input_id'])










#data/200/z2