import praw
import config
import time
import os
import random
import openpyxl
import datetime
GonderilenPostIdleri = []
Satirsublar = []
Postlinks = []
Hata = "community"

import socket

        
def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

def randomTime():
    randomText1 = random.randint(60,120)
    return  randomText1
def randomLine():
    textim = random.choice(list(open('readme.txt')))
    return textim
def randomLink():
    textlink = random.choice(list(open('justetext.txt')))
    return textlink

def bot_login():
	print ("Logging in...")
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "replay bot by u/4234we")
	print ("Logged in!")

	return r



def run_bot(subreddit1, GonderilenPostIdleri,r,username_Used):    
    for submission in subreddit1.new(limit=100):
        if submission.id not in GonderilenPostIdleri :
            print ("Yeni Post bulundu. Post id : " + submission.id)
     
            with open('subreddits.txt') as file:
                for line in file:
                    print("Subreddit sıraya alındı : " + line.rstrip())
                    with open("Paylasilansublar.txt") as file1:  #Paylasilansublar.txt elle oluştur.
                        Satirsublar = [line.strip() for line in file1]
                    if line.rstrip() not in Satirsublar :
                        submission1 = r.submission(id=submission.id)


                        r.validate_on_submit = True

                        try:

                            submission1.crosspost (subreddit=line.rstrip(), send_replies=True) # .reply(body=yorum)
                                            
                        except Exception as e:
                            print(str(e))
                            
                            if ("community" in str(e)  or  "frlair"  in str(e)):
                                with open("subreddits.txt", "r") as f:
                                    lines = f.readlines()
                                with open("subreddits.txt", "w") as f:
                                    for line1 in lines:
                                        if (line1.strip("\n") != line.rstrip()):
                                            f.write(line1)
                                    pass 
                               
                                    
                            else:
                                 try:
                                    submission1.crosspost (subreddit=line.rstrip(), send_replies=True) #.reply(body=yorum)
                                 except:
                                    with open("subreddits.txt", "r") as f:
                                        lines = f.readlines()
                                    with open("subreddits.txt", "w") as f:
                                        for line1 in lines:
                                            if (line1.strip("\n") != line.rstrip()):
                                                f.write(line1)
                                        pass
      
                        with open ("Paylasilansublar.txt", "a") as f:
                            f.write(line.rstrip() + "\n")
                        print ("Post Göderimi "+line.rstrip()+" subredditine yapıldı :  " + submission.id+"\n")
                        print ("Crosspost için yeni subreddit bekleniyor (random) ", time.sleep(randomTime()))
            
            GonderilenPostIdleri.append(submission.id)
          
            with open ("GonderilenPostIdleri.txt", "a") as f:
                f.write(submission.id + "\n")
                print ("GonderilenPostIdleri.txt'nin içine crosspost yapılan id kaydedildi.")
            print ("Crosspost işlemiş Bitti. " + submission.id)
            with open("Paylasilansublar.txt", "r+") as file2:
                file2.truncate()
                print ("Paylasilansublar.txt'in içi temizlendi.\n")
                print ("Yeni içerik için crosspostu  1 saat beklet. ",time.sleep(3600),"\n")
    print ("Corsspost Yapılan Post idleri : ",GonderilenPostIdleri)

    
                
  
def get_saved_comments():

	if not os.path.isfile("GonderilenPostIdleri.txt"):
		GonderilenPostIdleri = []
	else:
		with open("GonderilenPostIdleri.txt", "r") as f:
			GonderilenPostIdleri = f.read()
			GonderilenPostIdleri = GonderilenPostIdleri.split("\n")
			GonderilenPostIdleri = list(filter(None, GonderilenPostIdleri))

	return GonderilenPostIdleri




r = bot_login()
username_Used = ""
subreddit1 = r.subreddit('') #kendi subreddit sayfanın urlsi gelecek
GonderilenPostIdleri = get_saved_comments()







while True:
    try:
        run_bot(subreddit1, GonderilenPostIdleri,r,username_Used)
    except Exception as e:
        if (internet()):
            run_bot(subreddit1, GonderilenPostIdleri,r,username_Used)
        else:
            print("INTERNET YOK")
            time.sleep(500)
    
        
