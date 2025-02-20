from django.urls import path
from .views import home, button_click,weatherdataapi,my_api_view

urlpatterns = [
    path('', home, name='home'),
    path('button-click/', button_click, name='button_click'),
    path('weather-api/',weatherdataapi,name='weatherdataapi'),
    path('my_api_view/',my_api_view,name='my_api_view')
]
