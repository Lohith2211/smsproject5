from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
def projecthomepage(request):
    return render(request,'adminapp/projecthomepage.html')
# Create your views here.
def printpagecall(request):
    return render(request,'adminapp/printer.html')
def printpagelogic(request):
    if request.method=="POST":
        user_input=request.POST['user_input']
        print(f'User_input:{user_input}')
    a1= {'user_input':user_input}
    return render(request,'adminapp/printer.html',a1)

def exceptionpagecall(request):
    return render(request, 'adminapp/Exception.html')

def exceptionpagelogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        result = None
        error_message = None
        try:
            num = int(user_input)
            result = 10 / num
        except Exception as e:
            error_message = str(e)
        return render(request, 'adminapp/Exception.html', {'result': result, 'error': error_message})
    return render(request, 'adminapp/Exception.html')

import string
import random
def randompagecall(request):
    return render(request,'adminapp/randomexample.html')

def randomlogic(request):
    if request.method == "POST":
        number1 = int(request.POST['number1'])
        ran = ''.join(random.sample(string.ascii_uppercase + string.digits, k=number1))
    a1 = {'ran':ran}
    return render(request,'adminapp/randomexample.html',a1)

def calculatorpagecall(request):
    return render(request,'adminapp/calculator.html')

def calculatorlogic(request):
    result = None
    if request.method == 'POST':
        num1 = float(request.POST.get('num1'))
        num2 = float(request.POST.get('num2'))
        operation = request.POST.get('operation')

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2 if num2 != 0 else 'Infinity'

    return render(request, 'adminapp/calculator.html', {'result': result})


def datetimeexamplepagecall(request):
    return render(request, 'adminapp/datetimeexample.html')

import datetime
import calendar
def datetimeexamplelogic(request):
    if request.method == "POST":
        number1 = int(request.POST['date1'])
        x = datetime.datetime.now()
        from datetime import timedelta
        ran = x + timedelta(days=number1)
        ran1=ran.year
        ran2= calendar.isleap(ran1)
        if ran2 == False:
            ran3 = "Not leap year"
        else:
            ran3 = "leap year"
    a1 = {'ran': ran,'ran3':ran3,'ran1':ran1,'number1':number1}
    return render(request,'adminapp/datetimeexample.html',a1)

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
    else:
        form = TaskForm()
    tasks = Task.objects.all()
    return render(request, 'adminapp/add_task.html',
                    {'form': form, 'tasks': tasks})


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('add_task')

from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render
def UserRegisterPageCall(request):
    return render(request, 'adminapp/UserRegisterPage.html')
def UserRegisterLogic(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password1']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken.')
                return render(request, 'adminapp/UserRegisterPage.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'OOPS! Email already registered.')
                return render(request, 'adminapp/UserRegisterPage.html')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.save()
                messages.info(request, 'Account created Successfully!')
                return render(request, 'adminapp/Projecthomepage.html')
        else:
            messages.info(request, 'Passwords do not match.')
            return render(request, 'adminapp/UserRegisterPage.html')
    else:
        return render(request, 'adminapp/UserRegisterPage.html')

def UserLoginPageCall(request):
    return render(request, 'adminapp/UserLoginpage.html')

def UserLoginLogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if len(username) == 10:
                # Redirect to StudentHomePage
                messages.success(request, 'Login successful as student!')
                return redirect('studentapp:StudentHomePage')  # Replace with your student homepage URL name
                #return render(request, 'studentapp:StudentHomePage.html')
            elif len(username) == 7:
                # Redirect to FacultyHomePage
                # messages.success(request, 'Login successful as faculty!')
                # return redirect('facultyapp:FacultyHomePage')  # Replace with your faculty homepage URL name
                 return render(request, 'facultyapp/FacultyHomepage.html')
            else:
                # Invalid username length
                messages.error(request, 'Username length does not match student or faculty criteria.')
                return render(request, 'adminapp/UserLoginpage.html')
        else:
            # If authentication fails
            messages.error(request, 'Invalid username or password.')
            return render(request, 'adminapp/UserLoginpage.html')
    else:
        return render(request, 'adminapp/UserLoginpage.html')














def logout(request):
    auth.logout(request)
    return redirect('projecthomepage')


def student_list(request):
    students = StudentList.objects.all()
    return render(request, 'adminapp/student_list.html', {'students': students})

# from .forms import StudentForm
# from .models import StudentList

# def add_student(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('student_list')
#     else:
#         form = StudentForm()
#     return render(request, 'adminapp/add_student.html', {'form': form})

from django.contrib.auth.models import User
from .models import StudentList
from .forms import StudentForm
from django.shortcuts import redirect, render
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            register_number = form.cleaned_data['Register_Number']
            try:
                user = User.objects.get(username=register_number)
                student.user = user  # Assign the matching User to the student
            except User.DoesNotExist:
                form.add_error('Register_Number', 'No user found with this Register Number')
                return render(request, 'adminapp/add_student.html', {'form': form})
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminapp/add_student.html', {'form': form})



# contacts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import Contact
from .forms import ContactForm
from django.conf import settings

def contact_list(request):
    query = request.GET.get('q')
    contacts = Contact.objects.filter(name_icontains=query) | Contact.objects.filter(email_icontains=query) if query else Contact.objects.all()
    return render(request, 'adminapp/contact_list.html', {'contacts': contacts, 'query': query})

def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'adminapp/add_contact.html', {'form': form})

def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'adminapp/delete_contact.html', {'contact': contact})

def send_contact_email(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        email = request.POST['email']
        message = f"Name: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone_number}\nAddress: {contact.address}"
        send_mail('Contact Details', message, settings.EMAIL_HOST_USER, [email])
        return redirect('contact_list')
    return render(request, 'adminapp/send_contact_email.html', {'contact': contact})


# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm
from .models import Feedback  # If you want to save feedback to a database

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Save the feedback to the database
            Feedback.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                feedback=form.cleaned_data['feedback']
            )
            messages.success(request, "Thank you for your feedback!")
            return redirect('feedback_view')  # Redirect after successful submission
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeedbackForm()
    return render(request, 'adminapp/feedback_form.html', {'form': form})
