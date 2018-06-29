from django.urls import path

from . import views

app_name = 'torrents'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('search/', views.search, name='search'),
    path('download/', views.download, name='download'),
]
