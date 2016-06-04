from datetime import datetime
import time
import subprocess

_static_path = "/home/anudeep3998/cse535/code/"
file_path = _static_path+'tweetDump/log.txt'
start_time = ''
start_nano = 0
end_time = ''
end_nano = 0
elipsed_nano = 0

def log(msg):
    with open(file_path,"a+") as f:
        f.seek(0,2) #seek file end
        if msg:
            f.write("\n"+msg)
    

def start(cus_msg):
    global start_nano
    start_time = datetime.now().time()
    start_nano = int(round(time.time()))
    msg = "Starting twitterSiphon. \nStart Time : "+str(start_time)
    with open(file_path,"a+") as f:
        f.seek(0,2) #seek file end
        if cus_msg:
            msg = str(cus_msg + "\n"+msg)
        f.write("\n\n"+msg)


def end(msg):
    global start_nano
    global end_nano
    end_time = datetime.now().time()
    end_nano = int(round(time.time()))
    elipsed_nano = end_nano - start_nano
    
    p = subprocess.Popen(str("cat "+_static_path+"tweetDump/ger3.txt | grep '"+'"id"'+"' | wc -l"), stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    ger_count = str(int(output)) #remove byte encoding

    p = subprocess.Popen(str("cat "+_static_path+"tweetDump/rus3.txt | grep '"+'"id"'+"' | wc -l"), stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    rus_count = str(int(output))
    
    p = subprocess.Popen(str("cat "+_static_path+"tweetDump/eng3.txt | grep '"+'"id"'+"' | wc -l"), stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    eng_count = str(int(output))
    
    with open(file_path,"a+") as f:
        f.seek(0,2) #seek file end
        f.write("\n"+msg+"\nFinish Time : "+str(end_time) + " Executed for : "+str(elipsed_nano)+"s")
        f.write("\nCurrent tweets in dump : G["+ger_count+"]-R["+rus_count+"]-E["+eng_count+"]")
    
    
