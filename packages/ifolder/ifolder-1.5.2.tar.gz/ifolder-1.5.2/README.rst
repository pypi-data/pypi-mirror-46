# ifolder
ifolder is a python package for transferring files and folders with tcp socket.


receiver

.. code-block:: python

    from ifolder import Receiver
    # replace this path to a valid one on this machine
    toPATH = '/Users/xxxx/Desktop/copyto'

    rx = Receiver()
    while True:
        rx.save_files_to(toPATH)



sender


.. code-block:: python
    
    from ifolder import Sender
    ip = ('127.0.0.1',10086)

    # files or folders to be sent. should be a list
    files = [
    '/Users/xxx/Desktop/TEST.pdf',
    ]
    tx = Sender(ip)
    tx.send(files)