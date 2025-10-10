
from django.urls import path
from . import views

app_name = 'biblio_project'

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.sign_in, name='sign_in'),
    path('login/', views.login_user, name='login')
]