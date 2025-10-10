from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from.models import InfoUser, Address

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request, 'biblio_project/home.html')
    else:
        return HttpResponse('Você precisa estar logado')

def sign_in(request):

    if request.method == 'GET':
        return render(request, 'biblio_project/sign_in.html')
    
    else:
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

        return render(request, 'biblio_project/home.html')

def login_user(request):
    if request.method == 'GET':
        answer = False
        print("entrei no get")
        return render(request, 'biblio_project/login.html', {'answer':answer})
    
    else:
        print("entrei no else")
        answer = False
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)


        if user is not None:
            login(request, user)
            return render(request, 'biblio_project/home.html')
    
        else:
            print("entrei no else do else")
            answer = 'Login e senha inválidos!'
            return render(request, 'biblio_project/login.html', {'answer':answer})