#!/usr/bin/env python
import httplib
import socket
from cStringIO import StringIO

host = "localhost"
fileSize = 52428800

conn = httplib.HTTPConnection(host)
conn.request("POST", "/", headers={"Content-Type": "application/x-tar", "Transfer-Encoding": "chunked"})

fileForReading = StringIO()
fileForReading.seek(fileSize - 1)
fileForReading.write("\x00")
fileForReading.seek(0)

while True:
    data = fileForReading.read(1024)
    if not data:
        break
    conn.send("%x\r\n%s\r\n" % (len(data), data))
conn.send('0\r\n\r\n')

fileForReading.close()

conn.sock.shutdown(socket.SHUT_WR)
resp = conn.getresponse()

print "Status: %s" % resp.status
if resp.status == 200:
    if len(resp.read()) == fileSize:
        print "Success"
    else:
        print "Fail"
else:
    print resp.read()
conn.close()
