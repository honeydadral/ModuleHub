from django.urls import path
from . import views

app_name = 'modules'

urlpatterns = [
    path('', views.module_list, name='module_list'),
    path('<int:module_id>/', views.module_detail, name='module_detail'),
    path('<int:module_id>/register/', views.register, name='register'),
    path('<int:module_id>/unregister/', views.unregister, name='unregister'),
    path('api/<int:module_id>/register/', views.RegisterModuleAPIView.as_view(), name='api_register'),
]