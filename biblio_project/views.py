from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Book, Category, Favorite, Purchase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from.models import InfoUser, Address

# Create your views here.

@login_required(redirect_field_name="login/")
def home(request):
    if request.user.is_authenticated:
        user = request.user
        is_staff = user.is_staff
        books = Book.objects.all()

        return render(request, 'biblio_project/home.html', {'user': user, 'books':books, 'is_staff': is_staff})
    else:
        return HttpResponse('Você precisa estar logado')

def sign_in(request):

    if request.method == 'GET':
        return render(request, 'biblio_project/sign_in.html')
    
    else:
        try:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            first_name = request.POST.get("first_name") or ''
            last_name = request.POST.get("last_name") or ''
            photo = request.FILES.get("photo")
            cpf = request.POST.get("cpf")
            address = request.POST.get("address")
            city = request.POST.get("city")
            state = request.POST.get("state")
            country = request.POST.get("country")
            zip_code = request.POST.get("zip_code")

            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            new_info_user = InfoUser.objects.create(user=user, photo=photo, cpf=cpf)
            new_address = Address.objects.create(user=user, address=address, city=city, state=state, country=country,zip_code=zip_code)


            return redirect('http://127.0.0.1:8000/cadastro/sucesso')
    
        except Exception:
            return render(request, 'biblio_project/sign_in.html')

@login_required(redirect_field_name="login/")
def sign_in_success(request):
    return render(request, 'biblio_project/sucess.html')

def login_user(request):
    if request.method == 'GET':
        answer = False
        return render(request, 'biblio_project/login.html', {'answer':answer})
    
    else:
        answer = False
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)


        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
    
        else:
            answer = 'Login e senha inválidos!'
            return render(request, 'biblio_project/login.html', {'answer':answer})

@staff_member_required(login_url='http://127.0.0.1:8000/sem_acesso/')
@login_required(redirect_field_name="login/")   
def sign_in_books(request):
    if request.method == 'GET':
        correct_sign_in = 'Error'
        return render(request, 'biblio_project/sign_in_books.html')
    
    else:
        try:
            title = request.POST.get("title")
            author = request.POST.get("author")
            pages = request.POST.get("pages")
            buy_price = request.POST.get("buy_price") 
            available = request.POST.get('available') == 'on'
            description = request.POST.get("description")
            category_name = request.POST.get("name")
            image = request.FILES.get("image")

            new_book = Book.objects.create(title=title, author=author, pages=pages, buy_price=buy_price, available=available,
            description=description, image=image)

            category, created = Category.objects.get_or_create(name=category_name)

            new_book.categories.add(category)
            
            correct_sign_in = 'Correct'

            return render(request, 'biblio_project/sign_in_books.html', {'correct_sign_in': correct_sign_in})
    
        except Exception:
            correct_sign_in = 'Error'
            return render(request, 'biblio_project/sign_in_books.html', {'correct_sign_in': correct_sign_in})

@login_required(redirect_field_name="login/")
def profile(request):
    try:
        correct_sign_in = 'None' 
        user = request.user
        info_user, _ = InfoUser.objects.get_or_create(user=user)
        address, _ = Address.objects.get_or_create(user=user)

        if request.method == 'POST':
            user.first_name = request.POST.get('first_name') 
            user.last_name = request.POST.get('last_name') 
            user.email = request.POST.get('email') 
            user.username = request.POST.get('username')

            user.save(update_fields=['first_name', 'last_name', 'email', 'username'])

            info_user.cpf = request.POST.get('cpf') 
            info_user.photo = request.FILES.get('photo') 

            info_user.save(update_fields=['cpf', 'photo'])

            address.address = request.POST.get('address') 
            address.city = request.POST.get('city') 
            address.state = request.POST.get('state') 
            address.zip_code = request.POST.get('zip_code') 

            address.save(update_fields=['address', 'city', 'state', 'zip_code'])

            correct_sign_in = 'Correct' 

        return render(request, 'biblio_project/profile.html', {
            'user': user,
            'info_user': info_user,
            'address': address,
            'correct_sign_in': correct_sign_in,
        })
    
    except IntegrityError:
        correct_sign_in = 'UniqueCPF'
        return render(request, 'biblio_project/profile.html', {
            'user': user,
            'info_user': info_user,
            'address': address,
            'correct_sign_in': correct_sign_in,
        })
    
    except ValueError:
        correct_sign_in = 'Sem foto'
        return render(request, 'biblio_project/profile.html', {
            'user': user,
            'info_user': info_user,
            'address': address,
            'correct_sign_in': correct_sign_in,
        })
    
    except Exception as e:
        correct_sign_in = 'Error' 
        return render(request, 'biblio_project/profile.html', {
            'user': user,
            'info_user': info_user,
            'address': address,
            'correct_sign_in': correct_sign_in,
        })
    
def detail(request, id):
    item = get_object_or_404(Book, id=id)
    return render(request, 'biblio_project/detail.html', {'item': item})

@staff_member_required(login_url='http://127.0.0.1:8000/sem_acesso/')
@login_required(redirect_field_name="login/")
def edit_book(request, id):
    item = get_object_or_404(Book, pk=id)
    category = get_object_or_404(Category, book=item)
    correct_sign_in = 'None'

    if request.method == 'POST':
        try:
            title = request.POST.get("title")
            author = request.POST.get("author")
            pages = request.POST.get("pages")
            buy_price = request.POST.get("buy_price") 
            available = request.POST.get('available') == 'on'
            description = request.POST.get("description")
            name = request.POST.get("name")
            image = request.FILES.get("image")

            item.title = title
            item.author = author
            item.pages = pages
            item.buy_price = buy_price
            item.available = available
            item.description = description
            item.image = image
            category.name = name

            item.save()
            category.save()

            correct_sign_in = 'Correct'

            return render(request, 'biblio_project/edit_book.html', {'item':item, 'category': category, 'correct_sign_in': correct_sign_in})
        
        except Exception as e:
            print('Erro:', e)
            correct_sign_in = 'Error'

            return render(request, 'biblio_project/edit_book.html', {'item':item, 'category': category, 'correct_sign_in': correct_sign_in})
    
    else:
        return render(request, 'biblio_project/edit_book.html', {'item':item, 'category': category, 'correct_sign_in': correct_sign_in})

@staff_member_required(login_url='http://127.0.0.1:8000/sem_acesso/')
@login_required(redirect_field_name="login/")
def delete(request, id):
    if not request.user.is_staff:
        return HttpResponse("Você Não tem permissão para isso.")
    
    else:
        item = get_object_or_404(Book, pk=id)
        item.delete()
        return redirect('http://127.0.0.1:8000/')
    
@login_required(redirect_field_name="login/")
def noaccess(request):
    return render(request, 'biblio_project/no_access.html')

@login_required(redirect_field_name="login/")
def logout_view(request):
    logout(request)
    return render(request, 'biblio_project/logout.html')

def category(request):
    categories = Category.objects.prefetch_related('book').all()
    return render(request, 'biblio_project/category.html', {'categories': categories})

@login_required(redirect_field_name="login/")
def favorited(request, id):
    book = get_object_or_404(Book, id=id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)

    if not created:
        favorite.delete()

    return redirect('http://127.0.0.1:8000/')

@login_required(redirect_field_name="login/")
def books_favorited(request):
    favorited_books_ids = Favorite.objects.all().values_list('book_id', flat=True)

    favorited_books = Book.objects.filter(id__in=favorited_books_ids).distinct()

    return render(request, 'biblio_project/favorited.html', {'favorited_books': favorited_books})

@login_required(redirect_field_name="login/")
def purchased(request, id):
    book = get_object_or_404(Book, id=id)
    purchase, created = Purchase.objects.get_or_create(user=request.user, book=book)

    if not created:
        purchase.delete()

    return redirect('http://127.0.0.1:8000/')

@login_required(redirect_field_name="login/")
def books_purchased(request):
    purchased_books_ids = Purchase.objects.all().values_list('book_id', flat=True)

    purchased_books = Book.objects.filter(id__in=purchased_books_ids).distinct()

    return render(request, 'biblio_project/purchased.html', {'purchased_books': purchased_books})