# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 17:47:48 2015

@author: ruhansa
"""
import json
# if you are using python 3, you should 
# import urllib.request 
import urllib2


# change the url according to your own koding username and query
inurl = 'http://susmitha.koding.io:8983/solr/vsm/select?q=US+air+dropped+50+tons+of+Ammo+on+Syria&fl=id%2C+score&wt=json&indent=true&defType=dismax&qf=text_ru^0.5+text_en^2+text_de^0.5&pf=text_en&wt=json&indent=true&rows=1000'
outfn = 'test/res_trec_2.txt'


# change query id and IRModel name accordingly
qid = '002'
IRModel='default'
outf = open(outfn, 'w+')
data = urllib2.urlopen(inurl)
# if you're using python 3, you should use
# data = urllib.request.urlopen(inurl)

docs = json.load(data)['response']['docs']
# the ranking should start from 1 and increase
rank = 1
for doc in docs:
    outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
    rank += 1
outf.close()
