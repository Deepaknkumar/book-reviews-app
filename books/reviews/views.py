import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Book, Review

dev_key = ""    # your developer key

def index(request):
    books = Book.objects.all()[:100]
    context = { "books" : books}
    if request.user.is_authenticated:
        context.update({"loggedin": True})
        context.update({"user":request.user})
    else:
        context.update({"loggedin": False})
    return render(request, "reviews/display_books.html",context)


def book_info(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
        reviews = Review.objects.all().filter(book=book)
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": dev_key, "isbns": book.isbn})
        gdinfo = res.json()['books'][0]
        gdid = gdinfo['id']
        resreviews = requests.get("https://www.goodreads.com/book/show.json", params={"key": dev_key, "id": gdid,"text_only":True })
        reviewsdata = resreviews.json()
    except Book.DoesNotExist:
        raise Http404("Book does not exist in the database.")
    context = {"book":book, "gdinfo" : gdinfo, "reviewsdata":reviewsdata, "userreviews":reviews, "user": request.user}
    if request.user.is_authenticated:
        context.update({"loggedin":True})
        try:
            userreview = Review.objects.get(user=request.user,book=book)
            context.update({"userreview":userreview})
        except Review.DoesNotExist:
            pass
    else:
        context.update({"loggedin":False})
    return render(request, "reviews/book_info.html",context)

def login_page(request):
    return render(request, "reviews/login_page.html")


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password = password)
    if user is not None:
        login(request, user)
        context = { "user":user}
        return render(request,"reviews/accounts_page.html",context)
    else:
        return render(request,"reviews/error.html",{"message":"Incorrect credentials."})


def logout_user(request):
    logout(request)
    return redirect('index')

def signup_page(request):
    return render(request,"reviews/signup_page.html")


def signup_user(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    user = User.objects.create_user(username=username, email=email, password=password)
    user.first_name = firstname
    if lastname is not None:
        user.last_name = lastname
    user.save()
    return render(request,"reviews/error.html",{"message":"User {0} Created.".format(firstname)})

def search_book(request):
    keyword = request.GET['search_keyword']
    books1 = Book.objects.all().filter(isbn__contains=keyword)
    books2 = Book.objects.all().filter(title__contains=keyword)
    books3 = Book.objects.all().filter(author__contains=keyword)
    results_count = len(books1)+len(books2)+len(books3)
    context = {"books1":books1,"books2":books2,"books3":books3, "user":request.user, "keyword": keyword, "results_count":results_count}
    return render(request,"reviews/search_results.html",context)

def create_review(request, bookid):
    rating = request.POST.get('rating',False)
    rating = int(rating)
    if rating < 0 and rating > 5:
        return render(request,"reviews/error.html",{"message": "Rating should be between 0 to 5"})
    review = request.POST.get('review',False)
    review  = Review(user=request.user,book_id=bookid, rating=rating, review = review)
    review.save()
    return redirect('index')

def accounts_page(request,username):
    if request.user.is_authenticated:
        reviews = Review.objects.all().filter(user = request.user)
        context = {"reviews":reviews,"user":request.user}
        return render(request,"reviews/accounts_page.html",context)
    else:
        return render(request,"reviews/error.html",{"message":"Please login first."})


