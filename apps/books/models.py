from django.contrib.messages.api import error
from django.db import models
from django.db.models.deletion import CASCADE
from ..users.models import User

# Create your models here.
class BookManager(models.Manager):
    def book_validator(self, data):
        errors = []
        if len(data['title']) < 2:
            errors.append('Book title must be at least 2 characters')
        if len(data['author']) < 2:
            errors.append('Author name must be at lest 2 characters')
        if len(data['review']) < 2:
            errors.append('Review must be at least 2 characters')
        if  not data['rating']:
            errors.append('Must give a rating')
        if data['rating'] and int(data['rating']) > 5:
            errors.append('Rating must be between 1 and 5')
        check_books = Book.objects.all()
        for book in check_books:
            if data['title'].title() == book.title and data['author'].title() == book.author:
                errors.append('Book has already been added')
                break
        return errors
    def add_book(self, data, user_id):
        user = User.objects.get(id = user_id)
        book = Book.objects.create(
            title = data['title'].title(),
            author = data['author'].title(),
            uploaded_by = user
        )
        return book.id

    def add_review(self, data, user_id, book_id):
        review_owner = User.objects.get(id = user_id)
        book_reviewing = Book.objects.get(id = book_id)
        review = Review.objects.create(
            review = data['review'],
            rating = data['rating'],
            user = review_owner,
            book = book_reviewing
        )
        return review.id


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name='uploaded_books', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # users_who_liked = models.ManyToManyField(User, related_name='liked_books')
    objects = BookManager()


class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name='book_reviews', on_delete= CASCADE)
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()