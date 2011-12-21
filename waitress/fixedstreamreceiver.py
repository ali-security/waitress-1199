##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Fixed Stream Receiver
"""

from waitress.interfaces import IStreamConsumer
from zope.interface import implements


class FixedStreamReceiver(object):

    implements(IStreamConsumer)

    # See IStreamConsumer
    completed = False

    def __init__(self, cl, buf):
        self.remain = cl
        self.buf = buf

    def received(self, data):
        'See IStreamConsumer'
        rm = self.remain
        if rm < 1:
            self.completed = True  # Avoid any chance of spinning
            return 0
        datalen = len(data)
        if rm <= datalen:
            self.buf.append(data[:rm])
            self.remain = 0
            self.completed = True
            return rm
        else:
            self.buf.append(data)
            self.remain -= datalen
            return datalen

    def getfile(self):
        return self.buf.getfile()