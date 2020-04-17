from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json
import xmltodict
#from pornhub_api import api
import random

#api = api.PornhubApi()
app = Flask(__name__)

movieUrl='https://api.reelgood.com/v3.0/content/roulette/netflix?availability=onAnySource&content_kind=both&nocache=true&region=us'

imageMovieUrl='https://img.reelgood.com/content/movie/'
imageMovieUrlSuffix='/poster-92.jpg'
genreSuffix='&genre='
rating='&minimum_imdb='

coronaUrl='https://api.coronatracker.com/v3/stats/worldometer/country?countryCode='

genres={'accion':5,'animacion':6,'anime':39,'biograficas':7,'infantiles':8,'comedia':9,'crimen':10,'culto':41,'documental':11,'drama':3,'familiar':12,'fantasia':13,'comida':15,'game show':16,'historia':17,'hogar y jardin':18, 'horror':19, 'independientes':43,'LGBTQ':37,'musical':22,'misterio':23,'reality':25,'romance':4,'sci-fi':26,'deportes':29,'stand-up':45,'suspenso':32,'viajes':33}

countries={"colombia":"CO","usa":"US","españa":"ES","china":"CN","italia":"IT","francia":"FR","alemania":"DE"}

@app.route('/bot', methods=['POST'])
def bot():
    #print( request.values)
    parsedata=json.loads(request.data)['Body']
    print(parsedata)
    incoming_msg= parsedata['msg'].lower()
    incoming_media = ""
    if('media' in parsedata.keys()):
        incoming_media= parsedata['media']
    
    resp = MessagingResponse()
    msg = resp.message()
    # try:
    #     requests.post('https://magnolia-goldfinch-3225.twil.io/receive-owl',request)
    # except:
    #     print('fallo')
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if 'doggo' in incoming_msg:
        r = requests.get('https://dog.ceo/api/breeds/image/random')
        if r.status_code == 200:
            data = r.json()
            print(data)
            msg.media(data['message'])
        responded = True
    if 'netflix' in incoming_msg:
        if 'genero' in incoming_msg:
            for g in genres.keys():
                if g in incoming_msg:
                    print(movieUrl+genreSuffix+g)
                    r= requests.get(movieUrl+genreSuffix+str(genres[g]))
                    print(r)
                    if r.status_code == 200:
                        data = r.json()
                        #print(data)
                        movieId=data['id']
                        title=data['title']
                        overview=data['overview']
                        has_poster=data['has_poster']
                        msgBody='Titulo: '+title+'\n'+'Descripcion: '+overview+'\n'
                        if has_poster:
                            re=requests.get(imageMovieUrl+str(movieId)+imageMovieUrlSuffix)
                            print(re)
                            msg.media(imageMovieUrl+str(movieId)+imageMovieUrlSuffix)
                        msg.body(msgBody)
                        print(movieId,title,overview,has_poster)
                    responded=True
                    break
            if not responded:
                msgBody='los generos disponibles son: \n'
                for g in genres.keys():
                    msgBody+=('\n'+g)
                msg.body(msgBody)
                responded=True 
        else:       
            #if 'rating' in incoming_msg:         
            r = requests.get(movieUrl)
            if r.status_code == 200:
                data = r.json()
                #print(data)
                movieId=data['id']
                title=data['title']
                overview=data['overview']
                has_poster=data['has_poster']
                msgBody='Titulo: '+title+'\n'+'Descripcion: '+overview+'\n'
                if has_poster:
                    re=requests.get(imageMovieUrl+str(movieId)+imageMovieUrlSuffix)
                    print(re)
                    msg.media(imageMovieUrl+str(movieId)+imageMovieUrlSuffix)
                msg.body(msgBody)
                print(movieId,title,overview,has_poster)
            responded=True
                #quote = f'{data["content"]} ({data["author"]})' 
    if 'bicho' in incoming_msg:
        msg.body('siuuuuuuuuu')
        responded = True
    if 'luisa' in incoming_msg:
        msg.body('Hello, eres divina, bye')
        responded=True
    #if 'paula' in incoming_msg:
    #    all_tags=api.video.tags("f").tags
    #    all_categories = api.video.categories().categories
    #    tags = random.sample(all_tags, 5)
    #    category = random.choice(all_categories)
    #    result = api.search.search(ordering="mostrelevant", tags=tags, category=category)
    #    vid = result.videos[random.choice([0,1,2,3,4])]
    #    msg.body(vid.title +'\n'+vid.url)
    #    responded=True
    if 'kanye' in incoming_msg:
        # return a quote
        r = requests.get('https://api.kanye.rest')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["quote"]} '
        else:
            quote = 'I could not retrieve a kanye quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'dare' in incoming_msg:
        r=requests.get('https://truthordare-game.com/api/dare/9',headers={'Cache-Control': 'no-cache'})
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["text"]} '
        else:
            quote = 'I could not retrieve a dare at this time, sorry.'
        msg.body(quote)
        responded=True
    if 'truth' in incoming_msg:
        r=requests.get('https://truthordare-game.com/api/truth/9',headers={'Cache-Control': 'no-cache'})
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["text"]} '
        else:
            quote = 'I could not retrieve a dare at this time, sorry.'
        msg.body(quote)
        responded=True
    if 'covid' in incoming_msg:
        for country in countries.keys():
            if country in incoming_msg:
                msg.body(obtenerCovidStats(countries[country]))
                responded=True
        if not responded:
            countriesStr=''
            for country in  countries.keys():
                countriesStr+=('\n'+country)
            msg.body(obtenerCovidStats('')+'\n puedes ver las estadisitcas de los siguientes paises'+ countriesStr)
            responded=True
    if 'ayuda' in incoming_msg:
        msg.body('quote: te puedo ofrecer una cita en ingles\ncat: puedo mostrarte fotos de gatos\ndoggo: tambien de perros\n Netflix: te puedo ofrecer una pelicula aleatoria en netflix\n Neflix genero: puedo filtrar por generos y con esto puedes saber que generos hay\n Netflix genero "genero elegido" te recomiendo una pelicula con ese genero\n kanye: que diria Kanye West?\nel bicho: siuuuuuuuuuuuu\n covid: te doy estadisticas respecto al covid-19\n dare: reto hot\n truth: hot truth')
        responded=True
    if not responded:
        msg.body('escribe ayuda para saber que puedo hacer por ti')
    jsonResp=json.dumps(xmltodict.parse(str(resp)))
    return str(jsonResp)

def obtenerCovidStats(pais):
    if pais!='':    
        r= requests.get(coronaUrl+pais)
        data=r.json()
        print(data)
        data=data[0]
        totalConfirmed=data['totalConfirmed']
        totalDeaths=data['totalDeaths']
        totalRecovered=data['totalRecovered']
        totalActiveCases=data['activeCases']
        string='Total Confirmados: '+str(totalConfirmed)+'\n'+'Total Muertes: '+str(totalDeaths)+'\n'+'Total Recuperados: '+str(totalRecovered)+'\n'+'Total casos activos: '+str(totalActiveCases)+'\n'
        return string
    else:
        r= requests.get('https://api.coronatracker.com/v3/stats/worldometer/global')
        data=r.json()
        totalConfirmed=data['totalConfirmed']
        totalDeaths=data['totalDeaths']
        totalRecovered=data['totalRecovered']
        totalNewCases=data['totalNewCases']
        totalNewDeaths=data['totalNewDeaths']
        totalActiveCases=data['totalActiveCases']
        string='Total Confirmados: '+str(totalConfirmed)+'\n'+'Total Muertes: '+str(totalDeaths)+'\n'+'Total Recuperados: '+str(totalRecovered)+'\n'+'Total casos nuevos: '+str(totalNewCases)+'\n'+'Total nuevas muertes: '+str(totalNewDeaths)+'\n'+'Total casos activos: '+str(totalActiveCases)+'\n'
        return string

if __name__ == '__main__':
    app.run(debug=True)
