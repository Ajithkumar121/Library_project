import os
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from Library.forms import bookform
from Library.models import Books
from Library_project import settings



def index(request):
    books=Books.objects.all()
    context={"book_list":books}
    return render(request,"index.html",context)

def detail(request,book_id):
    books=Books.objects.get(id=book_id)
    return render(request,"detail.html",{"output":books})
def add_book(request):
    if request.method=="POST":
         name=request.POST.get('name')
         desc=request.POST.get('desc')
         year=request.POST.get('year')
         img=request.FILES['img']
         user=Books(name=name,desc=desc,year=year,img=img)
         user.save()
         return redirect("/")
    return render(request,'add.html')

def update(request,id):
    books=Books.objects.get(id=id)
    form=bookform(request.POST or None,request.FILES,instance=books)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,"edit.html",{'form':form,'Books':books})

def delete(request,id):
    if request.method=="POST":
        books=Books.objects.get(id=id)
        books.delete()
        return redirect("/")
    return render(request,"delete.html")

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"invalid username")
            return redirect('login')
    return render(request,"login.html")

def registration(request):
    if request.method=='POST':
        username=request.POST['username']
        first_name= request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2= request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username Taken")
                return redirect("registration")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email Taken")
                return redirect("registration")
            else:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"password not matched")
            return redirect('registration')

    return render(request,"registration.html")



def logout(request):
    auth.logout(request)
    return redirect('/')

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404