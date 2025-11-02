
from django.urls import path
from . import views

app_name = 'biblio_project'

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.sign_in, name='sign_in'),
    path('cadastro/sucesso', views.sign_in_success, name='sign_in_success'),
    path('sem_acesso/', views.noaccess, name='noaccess'),
    path('logout/', views.logout_view, name='logout'),
    path('categorias/', views.category, name='category'),
    path('accounts/login/', views.login_user, name='login'),
    path('cadastro_livros/', views.sign_in_books, name='sign_in_books'),
    path('alterar_livros/<int:id>/', views.edit_book, name='edit_book'),
    path('minha_conta/', views.profile, name='profile'),
    path('detalhes/<int:id>/', views.detail, name='detail'),
    path('deletar/<int:id>', views.delete, name='delete'),
    path('favoritar/<int:id>', views.favorited, name='favorited'),
    path('favoritos', views.books_favorited, name='books_favorited'),
    path('comprar/<int:id>', views.purchased, name='purchased'),
    path('comprados', views.books_purchased, name='books_purchased'),
]