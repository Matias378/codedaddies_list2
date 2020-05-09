from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'), #si pongo solo la pagina, sin nada, me va a views.home
    path('new_search', views.new_search, name="new_search"),
]