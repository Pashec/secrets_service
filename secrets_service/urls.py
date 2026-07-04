from django.urls import path
from . import views


urlpatterns = [
    path('', views.create_secret, name='create_secret'),
    path('created/<uuid:secret_id>/', views.secret_created, name='secret_crated'),
    path('secret/<uuid:secret_id>/', views.view_secret, name='view_secret')
]