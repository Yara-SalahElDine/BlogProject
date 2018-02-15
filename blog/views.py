from django.shortcuts import render
from .models import Categories, Posts ,Tags ,CategoryUser
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UserForm
from django.contrib.auth import authenticate , login , logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import  login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

def homepage(request):

    allPosts = Posts.objects.all().order_by("-created_at")
    paginator = Paginator(allPosts, 5)
    page = request.GET.get('page')
    try:
    	posts= paginator.page(page)
    except PageNotAnInteger:
    	posts= paginator.page(1)
    except EmptyPage:
    	posts= paginator.page(paginator.num_pages)
    	
    	
    context = {'allCategories':Categories.objects.all(), 'allPosts':posts}
    return render(request, 'homepage/homepage.html', context)
    



 


def search(request):
    tag=Tags.objects.get(tag_name__contains=request.POST['term'])
    found_postt=Posts.objects.filter(tag=tag.id)
    found_posts = Posts.objects.filter(title__icontains=request.POST['term']).order_by('-created_at')
    context = {"found": found_posts,"foundd":found_postt}
    return render(request, "search.html", context)

def getCategoryPosts(request, cat_id):
    get_category = Categories.objects.get(id=cat_id)
    context = {'allPosts':Posts.objects.filter(category_id=get_category.id).order_by('-created_at')}
    return render(request, "homepage/homepage.html", context)

def subscribe(request):
    cat_id=request.GET.get('catid',None)
    user_id=request.user.id
    sub=CategoryUser.objects.create(category_id=cat_id ,user_id=user_id)
    sub.save()
    responseData = {
        'json': True
    }
    
    return JsonResponse(responseData,safe=False)


def unsubscribe (request):
    cat_id=request.GET.get('catid',None)
    user_id=request.user.id
    unsub=CategoryUser.objects.get(category_id=cat_id ,user_id=user_id)
    unsub.delete()
    responseData = {
        'json': True
    }
    
    return JsonResponse(responseData,safe=False)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/blog/homepage')


@login_required
def special(request):
    return HttpResponse("you are loggin")


def register(request):
    registered=False
    if request.method=="POST":
        user_form=UserForm(request.POST)
        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            registered=True
            return HttpResponseRedirect('/blog/homepage')

        else:
            #print(user_form.errors)
            pass

    else:
        user_form = UserForm()
        return render(request, "login&&register/registeration.html", {"user_form":user_form , "registered":registered})




def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/blog/homepage')
            else:
                return render(request, 'login&&register/login.html', {'info': 0}) #user Not Active
        else:
            return render(request, 'login&&register/login.html', {'info':1}) #error in username or password

    else:
        return render(request, 'login&&register/login.html', {})


