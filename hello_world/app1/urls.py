from django.urls import path
from . import views

urlpatterns = [
    path('hello_world/', views.hello_world),
    path('a/', views.a),
    path('b/', views.b)
]
