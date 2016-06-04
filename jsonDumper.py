from fileWriter import fileWriter
from customTweet import customTweet
from urllib import parse
import sys

_static_path = "/home/cse535/code/"
from_file_path = [_static_path+'tweetDump/eng3.txt', _static_path+'tweetDump/ger3.txt', _static_path+'tweetDump/rus3.txt']
to_file_path = [_static_path+'tweetDump/cus_eng_encoded3.json', _static_path+'tweetDump/cus_ger_encoded3.json', _static_path+'tweetDump/cus_rus_encoded3.json']
custom_header = '['
custom_tail = ']'

count = [0,0,0]
illegal = 0

json_writer = fileWriter(to_file_path,custom_header,custom_tail)
t=0
for fr in from_file_path:
    print("Dumping data from : "+fr)
    with open (fr,"r",encoding='utf-8') as f:
        for line in  f:
            if len(line) > 10 :
                try:
                    tweet = customTweet(parse.unquote_plus(str(line)))
                    json_writer.dump_tweet(tweet.encode_to_json2(), tweet.lang)
                    if tweet.is_lang_english():
                        count[0] = count[0]+1
                    elif tweet.is_lang_german():
                        count[1] = count[1]+1
                    elif tweet.is_lang_russian():
                        count[2] = count[2]+1

                except Exception as e:
                    print("failed to dump :: "+line[:10] +" Exception : "+str(e))
                    illegal+=1
                    #print("Found an illegal entry")

t=0
for f in from_file_path:
    print('Dumped :: '+f+' --> '+to_file_path[(t)])
    t=t+1
print('Write :: '+' E['+str(count[0])+']'+' G['+str(count[1])+']'+' R['+str(count[2])+']'+' I['+str(illegal)+']') 