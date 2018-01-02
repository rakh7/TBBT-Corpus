import urllib3

http = urllib3.PoolManager()

response = http.request('GET','http://python.org/')
print(response.read())
