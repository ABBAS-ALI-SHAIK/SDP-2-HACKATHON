from datlien.views import deliver
from django.shortcuts import render,HttpResponse, redirect
from .forms import LoginForm,SignUpForm,DeliveryForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import access_roles, unauthenticate_user
from .models import Delivery
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from datlien.models import Hub

# Create your views here.
@login_required(login_url='login/')
@access_roles
def home(request):
    if request.method == "POST":
        request.POST._mutable = True
        request.POST['user']=request.user.get_username()
        filledform = DeliveryForm(request.POST)
        if request.POST['source']==request.POST['destination']:
            message = "Source & Destination Shouldn't be the Same ❗"
            username = request.user.get_username()
            initial_dict = {
                "user" : username,
            }
            form = DeliveryForm(initial=initial_dict)
            history = Delivery.objects.filter(user=username)
            return render(request, "user/index.html",{
                'username':username,
                'form':form,
                'history':history,
                'message':message
            })
        if filledform.is_valid():
            delivery = filledform.save(commit=False)
            src_hub_fare = Hub.objects.get(pk=delivery.source.id)
            dst_hub_fare = Hub.objects.get(pk=delivery.destination.id)
            delivery.total_amount = int(int(src_hub_fare.base_fare) + int(dst_hub_fare.base_fare) + (delivery.weight*20/100)) 
            delivery.save()
            return redirect('userhome')
        else:
            message = "Try Again"
            username = request.user.get_username()
            initial_dict = {
                "user" : username,
            }
            form = DeliveryForm(initial=initial_dict)
            history = Delivery.objects.filter(user=username)
            return render(request, "user/index.html",{
                'username':username,
                'form':form,
                'history':history,
                'message':message
            })
    else:
        username = request.user.get_username()
        initial_dict = {
            "user" : username,
        }
        form = DeliveryForm(initial=initial_dict)
        history = Delivery.objects.filter(user=username)
        return render(request, "user/index.html",{
            'username':username,
            'form':form,
            'history':history,
        })

@unauthenticate_user
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username , password=password)
        if user is not None:
            if user.is_staff:
                form = LoginForm()
                message = "Access Denied"
                return render(request,"user/login.html",{
                    'form':form,
                    'message': message
                })
            login(request, user)
            return redirect(request.GET.get('next'))
        else:
            form = LoginForm()
            message = "Invalid Login"
            return render(request,"user/login.html",{
                'form':form,
                'message': message
            })
    form = LoginForm()
    return render(request,"user/login.html",{
        'form':form
    })

@unauthenticate_user
def register_view(request):
    if request.method == "POST":
        filledform = SignUpForm(request.POST)
        if filledform.is_valid():
            user = filledform.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = filledform.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            form = SignUpForm()
            return render(request, "user/register.html",{
                'form':form,
                "successmessage":"Please confirm your email address to complete the registration"
            })
        else:
            form = SignUpForm()
            return render(request, "user/register.html",{
                'form':form,
                'message':"Please Try Again."
            })
    form = SignUpForm()
    return render(request, "user/register.html",{
        'form':form
    })

def logout_view(request):
    logout(request)
    return redirect('userhome')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()     
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')