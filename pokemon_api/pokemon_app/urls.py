from django.urls import path
from .views import pokemon_list, pokemon_detail

urlpatterns = [
    path('', pokemon_list, name='pokemon_list'),    # página de inicio de la aplicación
    path('<int:pokemon_id>/', pokemon_detail, name='pokemon_detail'),   # página individual de cada pokemon
]
