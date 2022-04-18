from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Book, Review
from ..users.models import User


# Create your views here.
# home page
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    books = Book.objects.all()
    books_with_reviews = []
    for book in books:
        if book.reviews:
            books_with_reviews.append(book)
    context= {
        'reviews': Review.objects.all().order_by('-created_at')[:3],
        'books': books_with_reviews,
        'user': User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'dashboard.html', context)

def review_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'user': user,
        'books': Book.objects.all()
    }
    return render(request, 'review.html', context)

def add_book_and_review(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/books/review')
    else:
        book_id = Book.objects.add_book(request.POST, request.session['user_id'])
        Review.objects.add_review(request.POST, request.session['user_id'], book_id)
        return redirect(f'/books/{book_id}')

def show_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id= request.session['user_id'])
    book_to_get= Book.objects.get(id = book_id)
    context = {
        'reviews': Review.objects.filter(book= book_to_get),
        'book': book_to_get,
        'user' : user
    }
    return render(request, 'show_book.html', context)

def create_review(request, book_id):
    errors = Book.objects.review_validator(request.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect(f'/books/{book_id}')
    else:
        book = Book.objects.get(id = book_id)
        reviews = Review.objects.filter(book = book)
        all_user_ids = []
        for review in reviews:
            all_user_ids.append(review.user.id)
            if request.session['user_id'] in all_user_ids:
                messages.error(request, 'You already reviewed this book')
            if request.session['user_id'] not in all_user_ids:
                Review.objects.add_review(request.POST, request.session['user_id'], book_id )
            return redirect(f'/books/{book_id}')

def add_review_to_existing_book(request):
    errors = []
    if len(request.POST['review']) < 2:
        errors.append('Review must be at least 2 characters')
    if not request.POST['rating']:
        errors.append('Must give a rating')
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/books/review')
    else:
        book_to_get = Book.objects.get(id = request.POST['id'])
        reviews = Review.objects.filter(book = book_to_get)
        all_user_ids = []
        for review in reviews:
            all_user_ids.append(review.user.id)
        if request.session['user_id'] in all_user_ids:
            messages.error(request, 'You already reviewed this book')
            return redirect('/books/review')
        if request.session['user_id'] not in all_user_ids:
            Review.objects.create(
                review = request.POST['review'],
                rating = request.POST['rating'],
                user = User.objects.get(id = request.session['user_id']),
                book = book_to_get
            )
            id = request.POST['id']
            return redirect(f'/books/{id}')

def delete_review(request, review_id):
    review = Review.objects.get(id = review_id)
    book_id = review.book.id
    print(book_id)
    review.delete()
    return redirect(f'/books/{book_id}')
