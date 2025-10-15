# predictor/urls.py
# predictor/urls.py
from django.urls import path, include
from . import views

app_name = 'predictor'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('survey/', views.stress_predictor_view, name='survey'),
    path('chat/', views.chat_page, name='chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
]