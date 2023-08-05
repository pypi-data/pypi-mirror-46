from django.urls import path

from django_model_prediction_service import views

app_name = 'service'

urlpatterns = [
    path('predictJob', views.get_prediction, name='get_prediction'),
]

