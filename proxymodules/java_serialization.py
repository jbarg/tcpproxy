#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import platform
if 'java' in platform.system().lower():
    import java.io as io
    from com.thoughtworks.xstream import XStream
    from java.lang import Exception


class Module:
    def __init__(self, incoming=False, options=None):
        self.is_jython = 'java' in platform.system().lower()
        # extract the file name from __file__. __file__ is proxymodules/name.py
        self.name = __file__.rsplit('/', 1)[1].split('.')[0]
        self.description = 'Deserialization of Java objects' if self.is_jython else \
                           'Deserialization of Java objects (needs jython)'
        self.incoming = incoming  # incoming means module is on -im chain
        self.execute = self.error

        if options is not None:
            if 'mode' in options.keys():
                print options['mode'] 
                if 'deserial' in options['mode']:
                    self.execute = self.deserial
                elif 'serial' in options['mode']:
                    self.execute = self.serial

    def deserial(self, data):
        if not self.is_jython:
            print '[!] This module can only be used in jython!'
            return data

        try:
        # turn data into a Java object
            bis = io.ByteArrayInputStream(data)
            ois = io.ObjectInputStream(bis)
            obj = ois.readObject()

            # converting Java object to XML structure
            xs = XStream()
            xml = xs.toXML(obj)
            return xml
        except  Exception, e:
            print '[!] Caught Exception. Could not convert.\n'
            return data

    def serial(self, data):
        if not self.is_jython:
            print '[!] This module can only be used in jython!'
            return data
        try:
            # Creating XStream object and creating Java object from XML structure
            xs = XStream()
            serial = xs.fromXML(data)

            # writing created Java object to and serializing it with ObjectOutputStream
            bos = io.ByteArrayOutputStream()
            oos = io.ObjectOutputStream(bos)
            oos.writeObject(serial)

            # I had a problem with signed vs. unsigned bytes, hence the & 0xff
            return "".join([chr(x & 0xff) for x in bos.toByteArray().tolist()])
        except  Exception, e:
            print '[!] Caught Exception. Could not convert.\n'
            return data

    def error(self, data):
        print '[!] Unknown mode'
        return data

if __name__ == '__main__':
    print 'This module is not supposed to be executed alone!'
