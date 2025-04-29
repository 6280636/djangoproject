from cProfile import Profile
from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import EmployeeLoginForm, TaskForm
from .models import Order, Procedure, Component, Profile


# Create your views here.


def home(request):
    return render(request, 'home.html')


# def signup(request):

#     if request.method == 'GET':
#         return render(request, 'signup.html', {
#             'form': UserCreationForm()
#         })

#     else:
#         if request.POST['password1'] == request.POST['password2']:
#             try:
#                 user = User.objects.create_user(
#                     username=request.POST['username'], password=request.POST['password1'])
#                 user.save()
#                 login(request, user)
#                 return redirect('tasks')

#             except IntegrityError:
#                 return render(request, 'signup.html', {
#                     'form': UserCreationForm,
#                     'error': 'Username already exist'
#                 })

#         return render(request, 'signup.html', {
#             'form': UserCreationForm,
#             'error': 'Password do not match'
#         })

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Please correct the error below.'
            })


def tasks(request):
    return render(request, 'tasks.html')


def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valida data'
            })


def signout(request):
    logout(request)
    return redirect('employee_login')


# def signin(request):
#     if request.method == 'GET':
#         return render(request, 'signin.html', {
#             'form': AuthenticationForm()
#         })
#     else:
#         user = authenticate(
#             request, username=request.POST['username'], password=request.POST['password']
#         )
#         if user is None:
#             return render(request, 'signin.html', {
#                 'form': AuthenticationForm,
#                 'error': 'Username or password is incorrect'
#             })
#         else:
#             login(request, user)
#             return redirect('order_search')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('order_search')
        else:
            return render(request, 'signin.html', {
                'form': form,
                'error': 'Usuario o contraseña incorrectos'
            })


def order_detail(request, order_id):
    if request.method == "GET":
        try:
            order = Order.objects.get(order_id=order_id)
           
            return render(request, 'order_detail.html', {
                'order': order,
                
            })
        except Order.DoesNotExist:
            return render(request, 'order_detail.html', {
                'error': 'Order does not exist'
            })
        
def order_search(request):
    order = None
    error = None

    if request.method == 'POST':
        order_id = request.POST.get('orderId')
        if order_id:
            try:
                order = Order.objects.get(order_id=order_id)
            except Order.DoesNotExist:
                error = 'Order does not exist'

    return render(request, 'order_detail.html', {
        'order': order,
        'error': error
    })
def verify_components(request, order_id):
    # carga la orden o devuelve 404
    order = get_object_or_404(Order, order_id=order_id)
    components = Component.objects.filter(codeitem=order.codeitem)
    half = len(components) // 2
    components_first_half = components[:half]
    components_second_half = components[half:]
    # renderiza el template pasando el objeto order
    return render(request, 'verify_components.html', {
        'order': order,
        'components': components,
        'components_first_half': components_first_half,
        'components_second_half': components_second_half,
        
    })

def procedure_detail(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    order = Order.objects.filter(codeitem__procedure=procedure).first()  # o .get() si solo hay uno
    return render(request, 'procedure_detail.html', {
        'procedure': procedure,
        'order': order,
    })

def employee_login(request):
    """
    Vue de connexion basée sur le numéro d'employé.
    """
    if request.method == 'POST':
        form = EmployeeLoginForm(request.POST)
        if form.is_valid():
            employee_number = form.cleaned_data['employee_number']
            try:
                profile = Profile.objects.get(employee_number=employee_number)
                user = profile.user
                login(request, user)
                return redirect('order_search')  # Remplace 'home' par la page vers laquelle tu veux rediriger
            except Profile.DoesNotExist:
                 if not form.errors.get('employee_number'):
                    form.add_error('employee_number', "Le numéro d'employé est invalide.")
    else:
        form = EmployeeLoginForm()

    return render(request, 'employee_login.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = EmployeeLoginForm(request.POST)
#         if form.is_valid():
#             employee_number = form.cleaned_data['employee_number']
#             try:
#                 profile = Profile.objects.get(employee_number=employee_number)
#                 user = profile.user
#                 user = authenticate(request, username=user.username, password=employee_number)
#                 if user is not None:
#                     login(request, user)
#                     return redirect('employee_login')  # O la página a la que desees redirigir
#                 else:
#                     messages.error(request, "Número de empleado o contraseña incorrectos.")
#             except Profile.DoesNotExist:
#                 messages.error(request, "No se encontró un perfil con ese número de empleado.")
#     else:
#         form = EmployeeLoginForm()
#     return render(request, 'employee_login.html', {'form': form})
