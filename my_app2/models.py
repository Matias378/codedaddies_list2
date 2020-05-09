from django.db import models

class Search(models.Model): #creamos la base de datos, ESTAS SON TABLAS

    objects = models.Manager() #hay que agregar esto a cada modelo
    search = models.CharField(max_length=500) #ESTAS SON COLUMNAS DE LA BASE DE DATOS
    created = models.DateTimeField(auto_now=True)

    def __str__(self):

        return '{}'.format(self.search)

    class Meta:

        verbose_name_plural = 'Searches' #esto es para que lo escriba bien asi en admin y no searchs


