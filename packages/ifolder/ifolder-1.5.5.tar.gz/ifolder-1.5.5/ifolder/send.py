from socketTransfering import Sender

ip = ('192.168.1.127',10086)
ip = ('127.0.0.1',10087)

# files or folders to be sent. list
files = [
'/Users/vt/Desktop/TEST/TEST.pdf',
'/Users/vt/Desktop/TEST/icon',
'/Users/vt/Desktop/TEST/wonderbits', 
]
tx = Sender(ip)

tx.send(files)

