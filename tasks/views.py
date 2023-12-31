from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def home(request):
    return render(request,'tasks/home.html')

def index(request):
    # import ipdb;ipdb.set_trace()
    tasks = Task.objects.all()
    
    form=TaskForm()
    
    if request.method == 'POST':
        try:
            form = TaskForm(request.POST)
            user=request.user

            if form.is_valid():
                mytodo = form.save()
                mytodo.user=request.user
                mytodo.save()
            return redirect('/list')
        except ValueError:
            return render(request,'tasks/list.html',{'form':TaskForm(), 'error':'Bad data passed in. Try again.'})
   
    else:
        user=request.user
        print(user)   
        context={'tasks':tasks,'user':user,'form':TaskForm()}
        
        return render(request,'tasks/list.html',context)
    
    # context = {'tasks':tasks, 'form':form}
    # return render(request,'tasks/list.html', context)

def update_task(request, pk):
    task= Task.objects.get(id=pk)
    
    print(pk)
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        print("fgvhgvfcghjuhgbvgh")
        if form.is_valid():
            form.save()
            return redirect('/list')
    
    context = {'form':form}
 
    return render(request, 'tasks/update_task.html',context)


def deleteTask(request, pk):
    item=Task.objects.get(id=pk)
    
    if request.method == 'POST':
        item.delete()
        return redirect('/list')
        
    
    context ={'item':item}
    return render(request,'tasks/delete.html',context)

# def login(request):

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic.detail import DetailView

from .forms import SignUpForm


class UserView(DetailView):
    template_name = 'tasks/profile.html'

    def get_object(self):
        return self.request.user


def assign_domain_admin(user):
    if not User.objects.filter(domain=user.domain, is_admin=True).exists():
        user.is_admin = True
        user.save()

def signup(request):
    # import ipdb;ipdb.set_trace()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            
            dom=form.cleaned_data.get('email')
            res = str(dom[dom.index('@') + 1 : ])
            user.domain=res
            user.save()
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                login(request, user)
            else:
                print("user is not authenticated")
                
            assign_domain_admin(user)
            print(user.domain)
            print(user.is_admin)
            if user.is_admin == False:
                user.is_active = False
            user.save()
            return redirect('tasks:profile')
    else:
        form = SignUpForm()
    return render(request, 'tasks/signup.html', {'form': form})
    
    
def logoutView(request):
    logout(request)
    return redirect("login")

def loginView(request):
    tasks = Task.objects.all()
    form = TaskForm()
    user= request.user
    # print(user)
    # context = {"tasks":tasks, "form":form}
    context = {"tasks":tasks, "form":form,"user":request.user}
    
    if user.is_authenticated:
        context2 = {"tasks":tasks, "form":form,"user":user}
        return render(request,'tasks/profile.html',context2)
    
    if request.POST:
        form= AccountAuthenticationForm(request.POST)
        if form.is_valid():
            
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                
                mcontext = {"tasks":tasks, "form":TaskForm(),"user":user}
                
                login(request,user)
                destination= get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                
                print(user)
                return render(request,"tasks/list.html",mcontext)
        else:
            context['login_form']=form
    return render(request,'tasks/login.html',context)


def get_redirect_if_exists(request):
    redirect=None
    if request.GET:
        if request.GET.get("next"):
            redirect=str(request.GET.get("next"))
    return redirect

def admindashboard(request):
    form=TaskForm()
    context={"form":form}
    return render(request,'tasks/admindash.html',context)