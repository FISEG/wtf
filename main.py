from flask import Flask
from flask import request
from flask import jsonify
import requests
import json
from flask_sslify import SSLify
from bs4 import BeautifulSoup
import urllib.request


app=Flask(__name__)
sslify=SSLify(app)
# token 490951147:AAEmwCG3MBydNpRQTNps1C2-M5-bouOZKw0
URL='https://api.telegram.org/bot490951147:AAEmwCG3MBydNpRQTNps1C2-M5-bouOZKw0/'


def write_json(data, filename='answer.json'):
    with  open(filename,'w') as f:
        json.dump(data,f, indent=2, ensure_ascii=False)


def get_Updates():
    url=URL+'getUpdates'
    r=requests.get(url)

    return r.json()

def send_message(chat_id, text='something go wrong'):
    url=URL+'sendMessage'
    answer={'chat_id':chat_id, 'text':text}
    r=requests.post(url, json=answer)
    return r.json()





def get_html(url):
    response=urllib.request.urlopen(url)
    return response.read()

def parse(html):
    soup=BeautifulSoup(html)

    shedules=[]

    table=soup.find('div',class_='panel-group', id='accordion')

    for rows in table.find_all('div', class_='panel panel-default'):
           date=rows.find_all('div', class_='panel-heading')

           blocks=rows.find_all('span',class_='moreinfo')
           place=rows.find_all('span', class_='hoverable link')
           educator=rows.find_all('span',class_='link')
           shedules.append({'date':date[0].h4.text.strip(),
                         'time':blocks[0].text.strip(),
                         'project':blocks[1].text.strip(),
                         'place':place[0].text.strip(),

                         })


    str1=''
    for shedule in shedules:
        str1=str1+shedule['date']+'\n '+shedule['time']+' '+shedule['project']+' '+shedule['place']+'\n'+'\n'+' '


    return(str1)




@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
       r=request.get_json()
       chat_id=r['message']['chat']['id']
       message=r['message']['text']

       if '/shedule' in message:
           s=parse(get_html('https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/14930/'))
           send_message(chat_id,  s )
      # write_json(r)
           return jsonify(r)
    return '<h1>Bot welcomes you</h1>'
  #https://api.telegram.org/bot490951147:AAEmwCG3MBydNpRQTNps1C2-M5-bouOZKw0/setWebhook?url=https://8731c5b1.ngrok.io
    #    r=requests.get(URL+ 'getMe')
    #    write_json(r.json())
        # r=get_Updates()
        # chat_id=r['result'][-1]['message']['chat']['id']
        # send_message(chat_id)

#    parse(get_html('https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/14930'))

if __name__ == '__main__':

     app.run()
