===========
MKSms Client
===========

MKSms Client is a Python library written to handle/consume the MKSms API. Here is how to use::

    #!/usr/bin/env python

    from mksms.contact import Contact
    from mksms.message import Message, Response
    from mksms.client import Client

    contact = Contact("600000000", "Name")
    message = Message(contact, "Salut molah")
    client = Client("830EA3BB2A", "73249341d85f566b6f2b8cef4563d6c149efe4df2b43f21776a6c9faf7f61af5")
    resp = client.send_message(message)
    self.assertEqual(resp.success, True)

