# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# User Authentication Views
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('book_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Book CRUD Views
from .models import Book
from django.contrib.auth.decorators import login_required

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required
def book_create(request):
    if request.method == 'POST':
        Book.objects.create(
            title=request.POST['title'],
            author=request.POST['author'],
            genre=request.POST['genre'],
            rating=request.POST['rating']
        )
        return redirect('book_list')
    return render(request, 'book_form.html')

@login_required
def book_update(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.genre = request.POST['genre']
        book.rating = request.POST['rating']
        book.save()
        return redirect('book_list')
    return render(request, 'book_form.html', {'book': book})

@login_required
def book_delete(request, pk):
    Book.objects.get(pk=pk).delete()
    return redirect('book_list')

# To reset password
from django.contrib.auth.models import User

def custom_password_reset(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            context['success'] = "Password updated successfully. You can now log in."
        except User.DoesNotExist:
            context['error'] = "Email not found. Please enter the correct registered email."

    return render(request, 'custom_reset.html', context)
