from django.urls import path
from . import views

app_name = "LibrarySys"

urlpatterns = [
    path('', views.BookListView.as_view(), name="book_page"),
]