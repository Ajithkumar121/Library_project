from .import views
from django.urls import path

app_name='Library'
urlpatterns = [
    path('',views.index,name="index"),
    path('books/<int:book_id>/',views.detail,name="detail"),
    path('add/',views.add_book,name="add_book"),
    path('update/<int:id>/',views.update,name="update"),
    path('delete/<int:id>/',views.delete,name="delete"),
    path('registration/', views.registration, name="registration"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),



]