from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login,authenticate, logout
from account.forms import RegistrationForm, AccountAuthForm, AccountUpdateForm
from blog.models import BlogPost

def registeration_form(request):
    context={}
    if request.POST:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            raw_pass = form.cleaned_data.get('password1')
            account = authenticate(email=email, password = raw_pass)
            login(request,account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request,'account/registration_form.html',context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context={}
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form =  AccountAuthForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email,password=password)

            if user:
                login(request,user)
                return redirect('home')
    else:
        form = AccountAuthForm()
    
    context['login_form'] = form

   
    return render(request,'account/login.html',context)


def account_view(request):

    if not request.user.is_authenticated:
        return redirect('login')
    
    context={}
    if request.POST:
        # i am going to pass the instance because i am referencing it inside the 
        #AccountUpdateForm to get the PRIMARY KEY of a user that's aurthetcated
        # Tbat way i can use it in the form to authentiicate the account
        form = AccountUpdateForm(request.POST, instance = request.user)
        if form.is_valid():

            #before saving the form get the initials to reflect in form
            form.initial = {
                "email": request.POST['email'],
                "username":request.POST['username']
            }
            #this commmits the changes to the database
            form.save()

            #add it to context and display a success message
            context['success_message'] = "Updated"

    else:
        # these r the intial properties ujser will se on landing the update info for account page
        form = AccountUpdateForm(initial={"email":request.user.email, "username":request.user.username})

    context['account_form'] = form
    blog_posts = BlogPost.objects.filter(author=request.user)
    context['blog_post'] = blog_posts
    return render(request,'account/account.html',context)

def must_auth_view(request):
    return render(request,'account/must_authenticate.html',{})
