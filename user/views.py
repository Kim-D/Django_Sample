from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, RegisterForm

# Create your views here.

User = get_user_model()

def index(request):
    username = 'world'
    if request.user.is_authenticated:
        username = request.user.username
    
    return render(request, "index.html", {'welcom_msg': f"Hello, {username}"})

def login_view(request):
    if request.method == "POST":
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요
        form = LoginForm(request.POST)
        username = form['username'].value()
        password = form['password'].value()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요	
    logout(request)					
    return HttpResponseRedirect("/")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
def user_list_view(request):
    # TODO: 7. /users 에 user 목록을 출력해주세요
    # TODO: 9. user 목록은 pagination이 되게 해주세요
    #users
    if request.user.is_authenticated is False:
        return HttpResponseRedirect("/login")

    user_list = User.objects.all().order_by("register_date")
    page = int(request.GET.get('page', 1))

    paginator = Paginator(user_list, 5)
   
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.gage(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, "users.html", {"users": users})

