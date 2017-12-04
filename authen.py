import socket

CLIENT = {
    'USER': "5809610248",
    'PASS': "0248",
    'IP': socket.gethostbyname(socket.gethostname()),
    'PORT':  "12345"
}

AUTHEN = "USER:" + CLIENT['USER'] + "\n" + \
"PASS:" + CLIENT['PASS'] + "\n" + \
"IP:" + CLIENT['IP'] + "\n" + \
"PORT:" + CLIENT['PORT'] + "\n"