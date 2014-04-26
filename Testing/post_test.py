#import urllib, urllib2, cookielib

# cookie_jar = cookielib.CookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
# urllib2.install_opener(opener)

# #acquire cookie
# # url_1 = "http://yale-hout.appspot.com/api/event/create"
# # req = urllib2.Request(url_1)
# # rsp = urllib2.urlopen(req)

# # do POST
# url_2 = "http://yale-hout.appspot.com/api/event/create"
# values = dict(isbn='9780131185838', schoolStoreId='15828', catalogId='10001')
# data = urllib.urlencode(values)
# req = urllib2.Request(url_2, data)
# rsp = urllib2.urlopen(req)
# content = rsp.read()

# # print result
# import re
# pat = re.compile('Title:.*')
# print pat.search(content).group()

import httplib, urllib
params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
headers = {"Content-type": "application/json;charset=UTF-8", "Accept": "text/plain"}
conn = httplib.HTTPConnection("http://yale-hout.appspot.com/api/event/create:80")
conn.request("POST", "/cgi-bin/query", params, headers)
response = conn.getresponse()
print response.status, response.reason

data = response.read()
print data
conn.close()