from django.urls import path
from . import views

app_name = "LibrarySys"

urlpatterns = [
    path('', views.BookListView.as_view(), name="book_page"),
    path("detail/<book_id>/", views.BookDetailView.as_view(), name="book_detail"),
    path("search/", views.SearchPageView.as_view(), name="search")
]