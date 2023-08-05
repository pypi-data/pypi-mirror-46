from django.urls import path

from django_model_builder_service import views

app_name = 'service'

urlpatterns = [
    path('getmodel/<str:identifier>/', views.show_model, name='show_model'),
    path('getmodel/', views.get_model, name='get_model'),
]
