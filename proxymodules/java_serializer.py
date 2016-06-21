#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import platform
if 'java' in platform.system().lower():
    import java.io as io
    from com.thoughtworks.xstream import XStream


class Module:
    def __init__(self, incoming=False, options=None):
        self.is_jython = 'java' in platform.system().lower()
        # extract the file name from __file__. __file__ is proxymodules/name.py
        self.name = __file__.rsplit('/', 1)[1].split('.')[0]
        self.description = 'Serialization of XStream XML data' if self.is_jython else \
                           'serialization of XStream XML data (needs jython)'
        self.incoming = incoming  # incoming means module is on -im chain

    def execute(self, data):
        if not self.is_jython:
            print '[!] This module can only be used in jython!'
            return data

        # Creating XStream object and creating Java object from XML structure
        xs = XStream()
        serial = xs.fromXML(data)

        # writing created Java object to and serializing it with ObjectOutputStream
        bos = io.ByteArrayOutputStream()
        oos = io.ObjectOutputStream(bos)
        oos.writeObject(serial)

        # I had a problem with signed vs. unsigned bytes, hence the & 0xff
        return "".join([chr(x & 0xff) for x in bos.toByteArray().tolist()])


if __name__ == '__main__':
    print 'This module is not supposed to be executed alone!'
