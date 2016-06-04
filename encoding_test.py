#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sys

#print((json.loads('{"text":"абвТ"}')).encode('utf-8'))
j=json.loads('{"text":"\u0205"}')
text = j['text'].encode('utf-8')
print(bytes(text,'utf-8'))
#sys.stdout.write(text)
