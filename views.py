from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from .middlewares import auth, guest
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher
# Create your views here.

def my_view(request):
    try:
        Student = Student.objects.get(user=request.user)
        return HttpResponse("User is a student")
    # User is a student
    except Student.DoesNotExist:
        try:
            Teacher = Teacher.objects.get(user=request.user)
            return HttpResponse("User is a teacher")
        # User is a teacher
        except Teacher.DoesNotExist:
            return HttpResponse("User is neither a student nor a teacher")


''''
class StudentRegistrationForm(forms.ModelForm):
    # Define form fields here
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if username is unique
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    '''
# Your views can then use this form for registration or other purposes
@guest
def register_student(request):
    if request.method == 'POST':
        form = Student(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')  # Redirect to a success page
    else:
        form = Student()
    return render(request, 'auth/register.html', {'form': form})    
''''
#GENERAL REGISTRATION PAGE
@guest 
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password1':'','password2':""}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html',{'form':form}) 
'''


'''
@guest
def register_student_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)  # Pass request.FILES for handling uploaded files
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'auth/register_student.html', {'form': form})
'''

#TEACHER REGISTRATION PAGE
@guest
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('teacher_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register_teacher.html', {'form': form})

@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('student_dashboard')  
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'auth/login.html',{'form':form}) 


#creating separate dashboards for students and teachers.
@auth

def student_dashboard(request):
    user = request.user
    if user.is_authenticated:
        try:
            student = Student.objects.get(user=user)
            return render(request, 'auth/student_dashboard.html')
        except Student.DoesNotExist:
            pass







# LOGOUT 

def logout_view(request):
    logout(request)
    return redirect('login')



