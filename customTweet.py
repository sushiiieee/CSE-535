
import json
from urllib import parse


class customTweet :
    
    _id = '0'               #id of the tweet
    lang = 'en'             #language of the tweeet
    created_at = ''         #UTC time when the tweet was posted
    coordinates = [-1,-1]   #[longitude,latitude]
    text = ''               #text of tweeet
    retweet_status = False
    quote_status = False
    user_lang = 'en'
    
    place_id = ''           #place.id
    place_type = ''         #place.place_type
    place_full_name = ''    #place.place_full_name
    place_country_code = '' #plce.country_code
    place_country = ''      #place.country
    
    hashtags = []           #entities.hashtags[].text
    trends = []             #entities.trends[].text
    urls = []               #entities.urls[].url
    expanded_urls = []      #entities.urls[].expanded_url
    symbols = []            #entites.symbols[].text
    
    timestamp = 0           #timestamp_ms
    
    json_text = {}
    lang_set_en = ['en','en-us','en-gb','en-au','en-ca','en-nz','en-ie','en-za','en-jm','en-bz','en-tt','en-in']
    lang_set_de = ['de','de-ch','de-at','de-li','de-lu']
    lang_set_ru = ['ru','ru-mo']
    
    term_set = ['health','Gesundheit','здоровье', 'самочувствие','здравие','cancer','disease', \
                'blood','AIDS','Krebs','Krebsgeschwür', 'Krankheit', 'Erkrankung', \
                'болезнь','заболевание','недуг','карцинома','Gesundheitszustand','Volksgesundheit','krank','Übelkeit','	Erkrankung',\
                'Erbrechen']

    
    def __init__(self, text):
    
        try:
            json_text = json.loads(text, encoding="utf-8")
            self._id = json_text['id_str']
        except KeyError:
            pass
        
        try:
            self.lang = json_text['lang']
        except KeyError:
            pass
        
        try:
            self.user_lang = json_text['user']['lang']
        except KeyError:
            pass
        
        try:
            self.created_at = json_text['created_at']
        except KeyError:
            pass
        
        try:
            if (json_text['coordinates']) and ((json_text['coordinates']['coordinates'])) :
                self.coordinates = json_text['coordinates']['coordinates']
            else:
                self.coordinates = [-1,-1]
        except KeyError:
            self.coordinates = [-1,-1]
        except TypeError:
            self.coordinates = [-1,-1]
        
        try:
            self.text = json_text['text']
        except KeyError:
            pass
        
        try:
            if not json_text['retweeted_status']:
                self.retweet_status = False
            else :
                self.retweet_status = True
        except KeyError:
            pass
        
        try:
            if not json_text['quoted_status']:
                self.quote_status = False
            else :
                self.quote_status = True
        except KeyError:
            pass
        
        
        try:
            if not json_text['place']:
                self.place_id = ''
                self.place_type = ''
                self.place_full_name = ''
                self.place_country = ''
                self.place_country_code = ''
            else:
                try:
                    self.place_id = json_text['place']['id']
                    self.place_type = json_text['place']['place_type']
                    self.place_full_name = json_text['place']['full_name']
                    self.place_country_code = json_text['place']['country_code']
                    self.place_country = json_text['place']['country']
                    #print(json_text['place'])
                except KeyError:
                    pass
        except KeyError:
            self.place_id = ''
            self.place_type = ''
            self.place_full_name = ''
            self.place_country = ''
            self.place_country_code = ''
        
        try:
            self.hashtags = []
            self.trends = []
            self.symbols = []
            self.urls = []
            self.expanded_urls = []
            if json_text['entities'] :
                try:
                    if not json_text['entities']['hashtags'] :
                        self.hashtags = []
                    else:
                        for h in json_text['entities']['hashtags']:
                            self.hashtags.append(h['text'])
                except KeyError:
                    self.hashtags = []
                    
                try:
                    if not json_text['entities']['trends'] :
                        self.trends = []
                    else:
                        for t in json_text['entities']['trends']:
                            self.trends.append(t['text'])
                except KeyError:
                    self.trends = []
                    
                try:
                    if not json_text['entities']['symbols'] :
                        self.symbols = []
                    else:
                        for s in json_text['entities']['symbols']:
                            self.symbols.append(s['text'])
                except KeyError:
                    self.symbols = []
                    
                try:
                    if not json_text['entities']['urls'] :
                        self.urls = []
                        self.expanded_urls = []
                    else:
                        for u in json_text['entities']['urls']:
                            self.urls.append(parse.quote_plus(u['url']))
                            self.expanded_urls.append(parse.quote_plus(u['expanded_url']))
                except KeyError:
                        self.urls = []
                        self.expanded_urls = []
        except KeyError:
            self.hashtags = []
            self.trends = []
            self.symbols = []
            self.urls = []
            self.expanded_urls = []

        try:
            self.timestamp = json_text['timestamp_ms']
        except KeyError:
            self.timestamp = 0
        

    def sanitize_str(self,string):
        string = string.replace('\n','')
        string = string.replace('\r','')
        string = string.replace('\t','')
        return string.replace('"','')
 
    #currently not in use. Add other variables to complete and use
    def set_vals(self, _id='0',lang='en',created_at='',coordinates=[-1,-1],text='',retweet_status=False,quote_status=False, user_lang='en'):
        self._id = _id
        self.lang = lang
        self.created_at = created_at
        self.coordinates = coordinates
        self.text = text
        self.retweet_status = retweet_status
        self.quote_status = quote_status
        self.user_lang = user_lang

    def is_lang_english (self):
        #global lang_set_en
        #return self.lang in self.lang_set_en
        return False
        
    def is_lang_german (self):
        #global lang_set_de
        return ((self.lang in self.lang_set_de) and (self.user_lang in self.lang_set_de))
  
    def is_lang_russian (self):
        #global lang_set_ru
        return ((self.lang in self.lang_set_ru) and (self.user_lang in self.lang_set_ru))
    
    def is_lang_interesting (self):
        return self.is_lang_english() or self.is_lang_german() or self.is_lang_russian()
    
    
    def is_term_interesting (self):
        for term in self.term_set:
            for word in self.text.split():
                if word.lower() == term.lower():     #direct comparision works for German, English and Russian. Problems only seem to be with Greek and Turkish
                    return True
        return False
    
    def encode_to_json (self):
        str_tweet = '[{'
        str_tweet += ' "id" : "'+ self._id + '",'
        str_tweet += ' "lang" : "'+ self.lang + '",'
        str_tweet += ' "created_at" : "'+ self.created_at + '",'
        str_tweet += ' "coordinates" : { "longitude" : '+ str(self.coordinates[0]) + ', "latitude" :' + str(self.coordinates[1]) + '},'
        str_tweet += ' "text" : "'+ parse.quote_plus(self.text) + '"'
        str_tweet += '}]'
        
        #print(json.loads(str_tweet))
        return str_tweet

    def encode_to_json2 (self):
        str_tweet = '{'
        str_tweet += ' "id" : "'+ self._id + '",'
        str_tweet += ' "lang" : "'+ self.lang + '",'
        str_tweet += ' "created_at" : "'+ self.created_at + '",'
        str_tweet += ' "coordinates" : ['+ str(self.coordinates[0]) + ', ' + str(self.coordinates[1]) + '],'
        #str_tweet += ' "text" : "'+ urllib.parse.quote_plus(self.text) + '",'
        str_tweet += ' "place_id" : "'+ self.place_id + '",'
        str_tweet += ' "place_type" : "'+ self.place_type + '",'
        str_tweet += ' "place_full_name" : "'+ self.place_full_name + '",'
        str_tweet += ' "place_country_code" : "'+ self.place_country_code + '",'
        str_tweet += ' "place_country" : "'+ self.place_country + '",'
        str_tweet += ' "tweet_hashtags" : "'+ str(self.hashtags) + '",'
        str_tweet += ' "trends" : "'+ str(self.trends) + '",'
        str_tweet += ' "symbols" : "'+ str(self.symbols) + '",'
        str_tweet += ' "tweet_urls" : "'+ str(self.urls) + '",'
        str_tweet += ' "expanded_urls" : "'+ str(self.expanded_urls) + '",'
        str_tweet += ' "timestamp" : "'+ str(self.timestamp) + '",'
        str_tweet += ' "text" : "'+ self.sanitize_str(self.text) + '"'
        
        if self.is_lang_english():
            str_tweet += ', "text_en" : "'+ self.sanitize_str(self.text) + '"'
        elif self.is_lang_russian():
            str_tweet += ', "text_ru" : "'+ self.sanitize_str(self.text) + '"'
        elif self.is_lang_german():
            str_tweet += ', "text_de" : "'+ self.sanitize_str(self.text) + '"'

        str_tweet += '}'
        
        #print(json.loads(str_tweet))
        return str_tweet

    def is_original(self) :
        return ((not self.retweet_status) and (not self.quote_status))
        
    def encode_to_json2_bin(self):
        return self.encode_to_json2.encode("utf-8")
