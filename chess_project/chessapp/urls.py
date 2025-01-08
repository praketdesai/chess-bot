from django.urls import path
from . import views

urlpatterns = [
    path('', views.chessboard, name='chessboard'),
    path('select-square/', views.select_square, name='select_square'),
]