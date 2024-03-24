import http.client, urllib.parse
params = urllib.parse.urlencode({'@direction': 'forward', '@step_count': '600' })
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "type/plain"}
conn = http.client.HTTPConnection("192.168.1.55:8000")
conn.request("POST", "", params, headers)
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
data
conn.close()
