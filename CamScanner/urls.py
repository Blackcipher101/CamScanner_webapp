from django.urls import path
from . import views

urlpatterns = [
    path('', views.stream, name='stream'),
    path('home/',views.html_render, name='html_render'),
    path('capture/',views.capture, name='capture'),
    path('points/', views.points, name='points'),
    path('display_points/',views.display_points, name='display_points'),
    path('final/',views.display_last, name='per_blur'),
    path('download/',views.download, name='download')
]
