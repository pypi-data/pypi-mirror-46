from socketTransfering import Receiver


toPATH = '/Users/vt/Desktop/copyto'

rx = Receiver()

while True:
    rx.save_files_to(toPATH)

