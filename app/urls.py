from django.contrib import admin
from django.urls import path
from .views import get_recipe
urlpatterns = [
        path('get-recipe/', get_recipe, name='get_recipe'),

]
