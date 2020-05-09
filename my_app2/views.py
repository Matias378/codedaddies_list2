from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus #es para evitar los espacios en blanco en url, pone un +
from . import models


BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/sss?sort=rel&query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'



def home (request):
    return render(request, 'base.html')



def new_search (request):

    search = request.POST.get('search')

    models.Search.objects.create(search=search) #para crear base de datos, pone el search de arriba en la base

    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))

    response = requests.get(final_url)

    data = response.text

    soup = BeautifulSoup(data, features='html.parser') #es como que toma un elemento html y lo convierte en un objeto

    
    post_listings = soup.find_all('li', {'class':'result-row'}) #result-row tiene toda la info de abajo
    
    
    final_posting = []

    for post in post_listings:

        post_title = post.find(class_='result-title').text#esto lo encontras inspeccionando elemento  por elemento, encontra todos los elementos 'a'(links), cuya clase sea result-title(en la pagina dice: a.result-title.hdrlnk)
        post_url = post.find('a').get('href')
        
        if post.find(class_ ='result-price'): #el _ no es nada, es para usar la palabra class sin que tome la funcion, es un nombre nada mas aca puede ir cualquier palabra

            post_price = post.find(class_ ='result-price').text
        else:
            post_price="N/A"

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1] #data-ids me deveulve un string con todas las imagenes mezcladas, lo que hago con split es separar los strings por comas y asi tener cada elemento por separado y ahi elijo el [i], y desp queda algo como 1:324243fsdfs, por eso el segundo  split y me quedo solo con la foto, obteniendo ahora si una lista de fotos
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'


        final_posting.append((post_title, post_url, post_price, post_image_url))


    
    
    stuff_for_frontend = {
        
        'search': search,
        'final_posting': final_posting,

        
        }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)

