#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import platform
if 'java' in platform.system().lower():
    import java.io as io
    from com.thoughtworks.xstream import XStream

class Module:
    def __init__(self):
        self.is_jython = 'java' in platform.system().lower()
        self.name = 'java_deserializer'
        self.description = 'Deserialization of Java objects' if self.is_jython else \
                           'Deserialization of Java objects (needs jython)'

    def execute(self, data):
        if not self.is_jython:
            print '[!] This module can only be used in jython!'
            return data

        # turn data into a Java object
        bis = io.ByteArrayInputStream(data)
        ois = io.ObjectInputStream(bis)
        obj = ois.readObject()

        # converting Java object to XML structure
        xs = XStream()
        xml = xs.toXML(obj)
        return xml

if __name__ == '__main__':
    print 'This module is not supposed to be executed alone!'
