from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name= 'dash'),
    path('review', views.review_page),
    path('create', views.add_book_and_review),
    path('<int:book_id>', views.show_book),
    path('add_review/<int:book_id>', views.create_review),
    path('add_review', views.add_review_to_existing_book),
    path('delete_review/<int:review_id>', views.delete_review)
]