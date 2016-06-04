#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

import json
import requests
import sys
import logger
import subprocess

from customTweet import customTweet
from fileWriter import fileWriter

ckey = 'ZiS77nnXgwbPIVZ5AsvxERCnK'
csecret = 'VKcf7Sfd5mwmpcjSuGOWVCkiLMfpoMOZ5i4LLidCZtwhMUBv8Q'
atoken = '3526839621-Poj6uaa1CNn5WPXK3GFD91NMs0Do1WON3yxkUpE'
asecret = 'Fo0YlmTqMnLbeH3GsgNn1VyEmCIW3IGWuDKDrQ6cWWXD3'

count = 1
interesting_count=0
int_german=0
int_russian=0
init_by = 'user'

_TOTAL_LIMIT = 500
_INTERESTING_LIMIT = 100
_STRICT_INTERESTING_LIMIT_LOWER = 10

tw_writer = fileWriter()

update_url = ['http://localhost:8983/solr/gettingstarted/update/json/docs','http://localhost:7574/solr/gettingstarted/update/json/docs']
update_url_args = ['?split=/'+ \
                  '&f=id:/id' + \
                  '&f=lang:/lang' + \
                  '&f=created_at:/created_at' + \
                  '&f=longitude:/coordinates/longitude' + \
                  '&f=latitude:/coordinates/latitude' + \
                  '&f=text:/text'+ \
                  '&commit=true'+ \
                  '&data=' , \
                  \
                  '?split=/'+ \
                  '&f=id:/id' + \
                  '&f=lang:/lang' + \
                  '&f=created_at:/created_at' + \
                  '&f=longitude:/coordinates/longitude' + \
                  '&f=latitude:/coordinates/latitude' + \
                  '&f=text:/text'+ \
                  '&data='
                  ]

headers = {'Content-type':'application/json'}
term_set = ['health','Gesundheit','здоровье', 'самочувствие','здравие','cancer','disease', \
            'blood','AIDS','Krebs','Krebsgeschwür', 'Krankheit', 'Erkrankung', \
            'болезнь','заболевание','недуг','карцинома','Gesundheitszustand','Volksgesundheit','krank','Übelkeit','	Erkrankung',\
            'Erbrechen']


class twitterListener(StreamListener) :
    global count
    global interesting_count
    global int_german
    global int_russian
    global tw_writer
    global init_by
    
    def __init__(self):
        super().__init__()
        #tw_writer = fileWriter()

    def on_data(self, data) :
        global count
        global interesting_count
        global int_german
        global int_russian
        global tw_writer
        global _TOTAL_LIMIT
        global _INTERESTING_LIMIT
        global _STRICT_INTERESTING_LIMIT_LOWER
        global init_by
        
        tweet = customTweet(data)
        
        
        if tweet.is_lang_interesting() and tweet.is_term_interesting() and tweet.is_original():
            if tweet.is_lang_german():
                int_german = int_german + 1
            if tweet.is_lang_russian():
                int_russian = int_russian + 1
                
            interesting_count+=1
            print("Got a new tweet :: Total # : "+ str(int_german)+"-"+str(int_russian)+"|"+str(interesting_count-int_german-int_russian)+"/"+str(count))
            
            if tweet.is_lang_german() :
                tw_writer.dump_tweet(data,'de')
            elif tweet.is_lang_russian() :
                tw_writer.dump_tweet(data,'ru')
            elif tweet.is_lang_english() :
                tw_writer.dump_tweet(data,'en')
            
            
            if (interesting_count <= _INTERESTING_LIMIT and count <= _TOTAL_LIMIT) or interesting_count <= _STRICT_INTERESTING_LIMIT_LOWER :
                '''try:
                    #req = requests.post(update_url[count%2]+update_url_args[0 if count%25==0 else 1], data = tweet.encode_to_json(), headers=headers)
                    pass
                except Exception:
                        logger.log("Solr offline. Attempting wake")
                        p = subprocess.Popen(str("/home/cse535/solr/solr-5.3.0/bin/solr start -e cloud -noprompt"), stdout=subprocess.PIPE, shell=True)
                        (output, err) = p.communicate()
                        if err :
                            logger.log("Couldn't wake solr. Terminating.")
                            sys.exit(0)
                        else :
                            logger.log("solr wake successful. Continuing..")
                '''
                pass
                #print(req.text)
                #print("Pushing to SOLR : return# "+str(req.status_code))
            else:
                '''
                    commit both cores. One duplicate tweet will be added to one of the core, but shouldn't matter over the other count
                '''
                #req = requests.post(update_url[1]+update_url_args[0], data = tweet.encode_to_json(), headers=headers)
                #req = requests.post(update_url[0]+update_url_args[0], data = tweet.encode_to_json(), headers=headers)
                msg = "["+init_by+"] Successfully completed dump :: Total # : G["+ str(int_german)+"]-R["+str(int_russian)+"] | E["+str(interesting_count-int_german-int_russian)+"] / T["+str(count)+"]"
                print(msg)
                logger.end(msg)
                sys.exit(0)
        elif not tweet.is_original():
            print("retweet/quoted tweet. Scanned["+str(count)+"]")
        else:
            print("Unkown or uninteresting language/term, skipping. Scanned["+str(count)+"]")
        #print("Got a new tweet :: "+parsed_text['text'].encode('ascii', 'ignore').decode('ascii')+"\nTotal # : "+ str(count))
        count = count + 1
        
        #terminate after limit
        if count > _TOTAL_LIMIT and interesting_count > _STRICT_INTERESTING_LIMIT_LOWER :
            msg = "["+init_by+"] Successfully completed dump :: Total # : G["+ str(int_german)+"]-R["+str(int_russian)+"] | E["+str(interesting_count-int_german-int_russian)+"] / T["+str(count)+"]"
            logger.end(msg)
            print(msg)
            sys.exit(0)
        
        return True
        
    def on_error(self, status) :
        print(status)
        

auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

try:
    twitterStream = Stream(auth,twitterListener())
    msg = " initiated run"
    
    try:
        if sys.argv[1] == "cron":
            msg = "cron" + msg
            init_by = 'cron'
        else:
            msg = "user" + msg
            init_by = 'user'
    except Exception:
         msg = "user" + msg
         init_by = 'user'
    print(msg)
    logger.start(msg)
    twitterStream.filter(track=term_set)
    
except KeyboardInterrupt:
    print("["+init_by+"] Caught KeyboardInterrupt :: Total # : G["+ str(int_german)+"]-R["+str(int_russian)+"] | E["+str(interesting_count-1-int_german-int_russian)+"] / T["+str(count))+"]"
    logger.end("["+init_by+"] Caught KeyboardInterrupt :: Total # : G["+ str(int_german)+"]-R["+str(int_russian)+"] | E["+str(interesting_count-1-int_german-int_russian)+"] / T["+str(count))+"]"
    sys.exit(0) 

