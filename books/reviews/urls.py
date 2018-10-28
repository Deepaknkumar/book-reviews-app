from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index,name = "index"),
    url(r'^book/(\d+)/', views.book_info, name = "book_info"),
    url(r'signup_page/', views.signup_page, name ="signup_page"),
    url(r'signup_user',views.signup_user, name="signup_user"),
    url(r'login_page/',views.login_page, name="login_page"),
    url(r'login_user/',views.login_user,name="login_user"),
    url(r'logout_user',views.logout_user,name="logout_user"),
    url(r'search/',views.search_book,name="search_book"),
    url(r'create_review/(\w+)/',views.create_review,name="create_review"),
    url(r'accounts/(\w+)/',views.accounts_page, name="accounts_page")
]
