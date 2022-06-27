import requests
import json

base = "http://127.0.0.1:5000/"




response = requests.get(base + "rstat" )
print (response.json())