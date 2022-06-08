from user.models import Delivery, DeliveryAgent
from django.shortcuts import render, redirect
from .forms import DeliveryAgentForm, DeliveryBoyForm, Profile,EditProfile,LoginForm,CentralHubForm,EditCentralHubForm,HubForm,EditHubForm,SignUpForm,CityForm
from .models import CentralHub, DeliveryBoy, Hub, State, City
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models import Sum

# Create your views here.
@login_required(login_url="login/")
def home(request):
    username = request.user.get_username()
    superuser = request.user.is_superuser
    is_c_hub = False
    is_hub = False
    hubs = None
    c_hub = None
    hub =None
    history = None
    deliveryboys = None
    is_deliveryboy = False
    p_orders=None
    c_orders=None
    c_orders_count=None
    p_orders_count=None
    no_of_hubs=None
    deliveryagents=None
    total_no_orders=None
    total_fare=None
    user_count=None
    p_deliveries_count=None
    pending=None
    approved=None
    picked=None
    shipped=None
    transit=None
    received=None
    out_for_delivery=None
    delivered=None
    if superuser:
        pending = Delivery.objects.filter(is_approved=False).count()
        approved = Delivery.objects.filter(is_picked=False).count()
        picked = Delivery.objects.filter(is_shipped=False).count()
        shipped = Delivery.objects.filter(is_transit=False).count()
        transit = Delivery.objects.filter(is_received=False).count()
        received = Delivery.objects.filter(out_for_delivery=False).count()
        out_for_delivery = Delivery.objects.filter(out_for_delivery=True).count()
        delivered = Delivery.objects.filter(is_delivered=True).count()

        c_orders_count = Delivery.objects.filter(is_delivered=True).count()
        p_orders_count = Delivery.objects.filter(is_delivered=False).count()
        no_of_hubs = Hub.objects.all().count()
        deliveryagents = DeliveryBoy.objects.all().count()
        total_no_orders = Delivery.objects.all().count()
        user_count = User.objects.filter(is_staff=False).count()
        p_deliveries_count = Delivery.objects.filter(is_approved=False).count()
        total_fare = Delivery.objects.all().aggregate(Sum('total_amount'))
        pass
    if not superuser:
        try:
            c_hub = CentralHub.objects.get(username=username)
            if c_hub is not None:
                is_c_hub=True
                hubs = Hub.objects.filter(central_hub=c_hub.id)
        except:
            try:
                hub = Hub.objects.get(username=username)
                if hub is not None:
                    is_hub=True
                    history = Delivery.objects.filter(source=hub.id)
                    deliveryboys = DeliveryBoy.objects.filter(hub=hub.id)
            except:
                try:
                    deliveryboy = DeliveryBoy.objects.get(username=username)
                    if deliveryboy is not None:
                        is_deliveryboy = True
                        p_orders = DeliveryAgent.objects.filter(delivery_boy=deliveryboy,is_delivered=False)
                        c_orders = DeliveryAgent.objects.filter(delivery_boy=deliveryboy,is_delivered=True)
                except:
                    pass
    return render(request, "datlien/index.html",{
        'username':username,
        'superuser':superuser,
        'is_c_hub':is_c_hub,
        'c_hub':c_hub,
        'hubs':hubs,
        'is_hub':is_hub,
        'hub':hub,
        'history':history,
        "deliveryboys":deliveryboys,
        "is_deliveryboy":is_deliveryboy,
        "p_orders":p_orders,
        "c_orders":c_orders,
        "c_orders_count":c_orders_count,
        "p_orders_count":p_orders_count,
        "no_of_hubs":no_of_hubs,
        "deliveryagents":deliveryagents,
        "total_no_orders":total_no_orders,
        "p_deliveries_count":p_deliveries_count,
        "total_fare":total_fare,
        "user_count":user_count,
        "pending":pending,
        "approved":approved,
        "picked":picked,
        "shipped":shipped,
        "transit":transit,
        "received":received,
        "out_for_delivery":out_for_delivery,
        "delivered":delivered
    })

@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username , password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect(request.GET.get('next'))
            else:
                form = LoginForm()
                message = "Access Denied"
                return render(request,"datlien/login.html",{
                    'form':form,
                    'message': message
                })
        else:
            form = LoginForm()
            message = "Invalid Login"
            return render(request,"datlien/login.html",{
                'form':form,
                'message': message
            })
    form = LoginForm()
    return render(request,"datlien/login.html",{
        'form':form
    })

@unauthenticated_user
def register_view(request):
    if request.method == "POST":
        filledform = SignUpForm(request.POST)
        if filledform.is_valid():
            filledform.save()
            return redirect('home')
        else:
            form = SignUpForm()
            return render(request, "datlien/register.html",{
                'form':form,
                'message':"Please Try Again."
            })
    form = SignUpForm()
    return render(request, "datlien/register.html",{
        'form':form
    })

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url="login/")
def viewCentralHubs(request):
    central_hubs = CentralHub.objects.all()
    username = request.user.get_username()
    superuser = request.user.is_superuser
    return render(request, "datlien/viewCentralHubs.html",{
        'username':username,
        'central_hubs':central_hubs,
        'superuser':superuser,
    })

@login_required(login_url="login/")
def addCentralHub(request):
    if request.method == "POST":
        filledform = CentralHubForm(request.POST)
        if filledform.is_valid():
            filledform.save()          
            User.objects.create_user(filledform.cleaned_data['username'],filledform.cleaned_data['email'],filledform.cleaned_data['password'],is_staff=True)
            u = User.objects.filter(username=filledform.cleaned_data['username'])
            print(u)
            c_hub = CentralHub.objects.filter(username=filledform.cleaned_data['username'])
            hub = Hub(central_hub=c_hub[0],city=c_hub[0].city,username=c_hub[0].username,password=c_hub[0].password,email=c_hub[0].email,address=c_hub[0].address,base_fare=c_hub[0].base_fare)
            hub.save()
            return redirect('home')
        else:
            form = CentralHubForm()
            username = request.user.get_username()
            superuser = request.user.is_superuser
            message = "Try Again"
            return render(request, "datlien/addCentralHub.html",{
                'form':form,
                'username':username,
                'message':message,
                'superuser':superuser
            })
    else:
        form = CentralHubForm()
        username = request.user.get_username()
        superuser = request.user.is_superuser
        return render(request, "datlien/addCentralHub.html",{
            'form':form,
            'username':username,
            'superuser':superuser
        })

@login_required(login_url="login/")
def editCentralHub(request,username):
    if request.method == "POST":
        central_hub = CentralHub.objects.get(username=username)
        filledform = EditCentralHubForm(request.POST,instance=central_hub)
        if filledform.is_valid():
            filledform.save()
            return redirect('home')
        else:
            form = EditCentralHubForm(instance=central_hub)
            username = request.user.get_username()
            superuser = request.user.is_superuser
            message = "Try Again"
            return render(request, "datlien/editCentralHub.html",{
                'form':form,
                'username':username,
                'message':message,
                'superuser':superuser
            })
    else:
        central_hub = CentralHub.objects.get(username=username)
        form = EditCentralHubForm(instance=central_hub)
        username=request.user.get_username()
        superuser = request.user.is_superuser
        return render(request,"datlien/editCentralHub.html",{
            'superuser':superuser,
            'form':form,
            'username':username,
        })

@login_required(login_url="login/")
def viewHubs(request):
    hubs = Hub.objects.all()
    username = request.user.get_username()
    superuser = request.user.is_superuser
    return render(request, "datlien/viewHubs.html",{
        'username':username,
        'hubs':hubs,
        'superuser':superuser,
    })

@login_required(login_url="login/")
def addHub(request):
    if request.method == "POST":
        filledform = HubForm(request.POST)
        if filledform.is_valid():
            filledform.save()
            User.objects.create_user(filledform.cleaned_data['username'],filledform.cleaned_data['email'],filledform.cleaned_data['password'],is_staff=True)
            u = User.objects.filter(username=filledform.cleaned_data['username'])
            print(u)
            return redirect('home')
        else:
            form = HubForm()
            username = request.user.get_username()
            superuser = request.user.is_superuser
            message = "Try Again"
            return render(request, "datlien/addHub.html",{
                'form':form,
                'username':username,
                'message':message,
                'superuser':superuser,
            })
    else:
        form = HubForm()
        username = request.user.get_username()
        superuser = request.user.is_superuser
        return render(request, "datlien/addHub.html",{
            'form':form,
            'username':username,
            'superuser':superuser
        })

@login_required(login_url="login/")
def editHub(request,username):
    if request.method == "POST":
        hub = Hub.objects.get(username=username)
        filledform = EditHubForm(request.POST,instance=hub)
        if filledform.is_valid():
            u = User.objects.get(username=username)
            filledform.save()
            return redirect('home')
        else:
            form = EditHubForm(instance=hub)
            username = request.user.get_username()
            superuser = request.user.is_superuser
            message = "Try Again"
            return render(request, "datlien/editHub.html",{
                'superuser':superuser,
                'form':form,
                'username':username,
                'message':message
            })
    else:
        hub = Hub.objects.get(username=username)
        form = EditHubForm(instance=hub)
        superuser = request.user.is_superuser
        username = request.user.get_username()
        return render(request,"datlien/editHub.html",{
            'form':form,
            'username':username,
            'superuser':superuser,
        })

@login_required(login_url="login/")
def viewStates(request):
    superuser = request.user.is_superuser
    username = request.user.get_username()
    states = State.objects.all()
    return render(request,"datlien/viewStates.html",{
        "states":states,
        'username':username,
        'superuser':superuser,
    })

@login_required(login_url="login/")
def state(request,id):
    superuser = request.user.is_superuser
    username = request.user.get_username()
    st = State.objects.get(pk=id)
    cities = City.objects.filter(state=id)
    central_hubs = CentralHub.objects.filter(state=id)
    return render(request,"datlien/state.html",{
        "cities":cities,
        "state":st,
        'username':username,
        'superuser':superuser,
        "central_hubs":central_hubs,
    })

@login_required(login_url="login/")
def addDeliveryBoy(request,id):
    if request.method=="POST":
        filledform=DeliveryBoyForm(request.POST)
        if filledform.is_valid():
            filledform.save()
            User.objects.create_user(username=filledform.cleaned_data['username'],password=filledform.cleaned_data['password'],is_staff=True)
            return redirect('home')
    superuser = request.user.is_superuser
    username = request.user.get_username()
    initial_dict={
        "hub":id
    }
    form = DeliveryBoyForm(initial=initial_dict)
    return render(request,"datlien/addDeliveryBoy.html",{
        "form":form,
        'username':username,
        'superuser':superuser,
    })

@login_required(login_url="login/")
def addCity(request,id):
    if request.method == "POST":
        filledform = CityForm(request.POST)
        if filledform.is_valid():
            filledform.save()
            return redirect('state',id)
        else:
            st = State.objects.get(pk=id)
            inital_dict={
                "state":st.id
            }
            form = CityForm(initial=inital_dict)
            return render(request,"datlien/addCity.html",{
                "form":form,
                "state":st,
                "message":"Try Again"
            })
    superuser = request.user.is_superuser
    username = request.user.get_username()
    st = State.objects.get(pk=id)
    inital_dict={
        "state":st.id
    }
    form = CityForm(initial=inital_dict)
    return render(request,"datlien/addCity.html",{
        "form":form,
        "state":st,
        'username':username,
        'superuser':superuser,
    })

@login_required(login_url="login/")
def prequest(request):
    superuser = request.user.is_superuser
    username = request.user.get_username()
    hub = Hub.objects.get(username=username)
    approval_req = Delivery.objects.filter(source=hub.id,is_approved=False)
    pickup_req = Delivery.objects.filter(source=hub.id,is_approved=True,is_picked=False)
    shippment_req = Delivery.objects.filter(source=hub.id,is_approved=True,is_picked=True,is_shipped=False)
    transit_req = Delivery.objects.filter(source=hub.id,is_approved=True,is_picked=True,is_shipped=True,is_transit=False)
    history = Delivery.objects.filter(source=hub.id,is_approved=True,is_picked=True,is_shipped=True,is_transit=True)
    return render(request, "datlien/prequest.html",{
        'username':username,
        'superuser':superuser,
        'approval_req': approval_req,
        'pickup_req': pickup_req,
        'shippment_req': shippment_req,
        'transit_req':transit_req,
        'history':history,
    })

@login_required(login_url="login/")
def porders(request):
    superuser = request.user.is_superuser
    username = request.user.get_username()
    hub = Hub.objects.get(username=username)
    received_req = Delivery.objects.filter(destination=hub.id,is_approved=True,is_picked=True,is_shipped=True,is_transit=True,is_received=False)
    out_for_delivery_req = Delivery.objects.filter(destination=hub.id,is_approved=True,is_picked=True,is_shipped=True,is_transit=True,is_received=True,out_for_delivery=False)
    delivery_req = Delivery.objects.filter(destination=hub.id,is_approved=True,is_picked=True,is_shipped=True,is_transit=True,is_received=True,out_for_delivery=True,is_delivered=False)
    return render(request, "datlien/porders.html",{
        'username':username,
        'superuser':superuser,
        'received_req':received_req,
        'out_for_delivery_req':out_for_delivery_req,
        'delivery_req':delivery_req,
    })

@login_required(login_url="login/")
def corders(request):
    superuser = request.user.is_superuser
    username = request.user.get_username()
    hub = Hub.objects.get(username=username)
    incoming_deliveries = Delivery.objects.filter(destination=hub.id,is_approved=True,is_picked=True,is_shipped=True,is_transit=True,is_received=True,out_for_delivery=True,is_delivered=True)
    out_going_deliveries = Delivery.objects.filter(source=hub.id,is_approved=True,is_picked=True,is_shipped=True,is_transit=True,is_received=True,out_for_delivery=True,is_delivered=True)
    return render(request, "datlien/corders.html",{
        'username':username,
        'superuser':superuser,
        'incoming_deliveries':incoming_deliveries,
        'out_going_deliveries':out_going_deliveries,
    })

@login_required(login_url="login/")
def approve(request,id):
    Delivery.objects.filter(pk=id).update(is_approved = True)
    delivery = Delivery.objects.get(pk=id)
    user = User.objects.filter(username=delivery.user)
    to_email = user[0].email
    mail_subject = 'Your Delivery Request has been Approved'
    message='Thanks for using our services. Your order has been approved and it will be Picked up soon.'
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return redirect('prequest')

@login_required(login_url="login/")
def pick(request,id):
    Delivery.objects.filter(pk=id).update(is_picked = True)
    delivery = Delivery.objects.get(pk=id)
    user = User.objects.filter(username=delivery.user)
    to_email = user[0].email
    mail_subject = 'Your Package has been Picked'
    message='Thanks for using our services. Your package will be shipped soon.'
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return redirect('prequest')

@login_required(login_url="login/")
def ship(request,id):
    Delivery.objects.filter(pk=id).update(is_shipped = True)
    delivery = Delivery.objects.get(pk=id)
    user = User.objects.filter(username=delivery.user)
    to_email = user[0].email
    mail_subject = 'Your Package has been Shipped'
    message='Thanks for using our services. Your package will be in transit soon.'
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return redirect('prequest')

@login_required(login_url="login/")
def transit(request,id):
    Delivery.objects.filter(pk=id).update(is_transit = True)
    delivery = Delivery.objects.get(pk=id)
    user = User.objects.filter(username=delivery.user)
    to_email = user[0].email
    mail_subject = 'Your Package is On its Way Destination'
    message='Thanks for using our services. You will receive a confirmation mail soon when it reaches the nearest Hub.'
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return redirect('prequest')

@login_required(login_url="login/")
def receive(request,id):
    Delivery.objects.filter(pk=id).update(is_received = True)
    delivery = Delivery.objects.get(pk=id)
    user = User.objects.filter(username=delivery.user)
    to_email = user[0].email
    mail_subject = 'Your Package has arrived the nearest Hub'
    message='Thanks for using our services. Soon, a Delivery Agent will be assigned to deliver your Package.'
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return redirect('porders')

@login_required(login_url="login/")
def out_for_delivery(request,id):
    if request.method == "POST":
        filledform = DeliveryAgentForm(request.POST)
        if filledform.is_valid():
            Delivery.objects.filter(pk=id).update(is_assigned = True, out_for_delivery=True)
            filledform.save()
            delivery = Delivery.objects.get(pk=id)
            user = User.objects.filter(username=delivery.user)
            to_email = user[0].email
            mail_subject = 'Your Package is assigned to a Delivery Agent'
            message='Thanks for using our services. Soon, Our Delivery Agent will get in touch with you and your Package will be delivered.'
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('porders')
    delivery = Delivery.objects.get(pk=id)
    initial_dict = {
        "delivery":delivery
    }
    form = DeliveryAgentForm(initial=initial_dict)
    return render(request,"datlien/addDeliveryAgent.html",{
        "form":form
    })

@login_required(login_url="login/")
def deliver(request,id):
    username = request.user.get_username()
    delivery = Delivery.objects.get(pk=id)
    delivery_boy = DeliveryBoy.objects.get(username=username)
    Delivery.objects.filter(pk=id).update(is_delivered = True)
    DeliveryAgent.objects.filter(delivery=delivery,delivery_boy=delivery_boy).update(is_delivered = True)
    user = User.objects.filter(username=delivery.user)
    to_email = user[0].email
    mail_subject = 'Congratulations 😉😎🎉'
    message='Your Package is delivered. Hope you like our services.'
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return redirect('home')

@login_required(login_url="login/")
def profile(request):
    superuser = request.user.is_superuser
    username = request.user.get_username()
    initial_dict = {
        "first_name":request.user.first_name,
        "last_name":request.user.last_name,
        "email":request.user.email,
        "username":request.user.username,
        "password":None
    }
    form = Profile(initial=initial_dict)
    return render(request, "datlien/profile.html",{
        'username':username,
        'superuser':superuser,
        'form':form,
    })

@login_required(login_url="/login")
def editprofile(request):
    if request.method == "POST":
        username = request.user.get_username()
        user = User.objects.get(username=username)
        filledform = EditProfile(request.POST, instance=user)
        if filledform.is_valid():
            filledform.save()
            u = User.objects.get(username=username)
            u.set_password(filledform.cleaned_data['password'])
            return redirect('profile')
        else:
            superuser = request.user.is_superuser
            username = request.user.get_username()
            message="Try again"
            initial_dict = {
                "first_name":request.user.first_name,
                "last_name":request.user.last_name,
                "email":request.user.email,
                "username":request.user.username,
                "password":request.user.password
            }
            form = EditProfile(initial=initial_dict)
            return render(request, "datlien/editprofile.html",{
                'username':username,
                'superuser':superuser,
                'form':form,
                'message':message,
            })
    else:
        superuser = request.user.is_superuser
        username = request.user.get_username()
        initial_dict = {
            "first_name":request.user.first_name,
            "last_name":request.user.last_name,
            "email":request.user.email,
            "username":request.user.username,
            "password":request.user.password
        }
        form = EditProfile(initial=initial_dict)
        return render(request, "datlien/editprofile.html",{
            'username':username,
            'superuser':superuser,
            'form':form,
        })

@login_required(login_url="login/")
def users(request):
    superuser = request.user.is_superuser
    username = request.user.get_username()
    users= User.objects.filter(is_staff=False)
    return render(request, "datlien/users.html",{
        'username':username,
        'superuser':superuser,
        'users':users,
    })

@login_required(login_url="login/")
def orders_history(request):
    if request.method=="POST":
        from_date = request.POST['fromdate']
        to_date = request.POST['todate']
        orders_history = Delivery.objects.raw('select * from user_delivery where created_on between "'+from_date+'" and "'+to_date+'"')
        superuser = request.user.is_superuser
        username = request.user.get_username()
        return render(request, "datlien/orders_history.html",{
            'username':username,
            'superuser':superuser,
            'orders_history':orders_history,
            'message':"Filter Results"
        })
    superuser = request.user.is_superuser
    username = request.user.get_username()
    orders_history= Delivery.objects.all()
    return render(request, "datlien/orders_history.html",{
        'username':username,
        'superuser':superuser,
        'orders_history':orders_history,
    })

@login_required(login_url="login/")
def history(request,id):
    superuser = request.user.is_superuser
    username = request.user.get_username()
    user = User.objects.get(pk=id)
    orders_history= Delivery.objects.filter(user=user.username)
    return render(request, "datlien/history.html",{
        'username':username,
        'superuser':superuser,
        'orders_history':orders_history,
        'user':user.username,
    })

@login_required(login_url="login/")
def c_hub_history(request,id):
    superuser = request.user.is_superuser
    username = request.user.get_username()
    c_hub = CentralHub.objects.get(pk=id)
    hub = Hub.objects.filter(username=c_hub.username)
    hubs = Hub.objects.filter(central_hub=c_hub)
    orders_history= Delivery.objects.filter(source=hub[0].id)
    return render(request, "datlien/c_hub_history.html",{
        'username':username,
        'superuser':superuser,
        'orders_history':orders_history,
        'c_hub':c_hub,
        'hubs':hubs,
    })

@login_required(login_url="login/")
def hub_history(request,id):
    superuser = request.user.is_superuser
    username = request.user.get_username()
    hub = Hub.objects.get(pk=id)
    orders_history= Delivery.objects.filter(source=hub.id)
    return render(request, "datlien/hub_history.html",{
        'username':username,
        'superuser':superuser,
        'orders_history':orders_history,
        'hub':hub,
    })