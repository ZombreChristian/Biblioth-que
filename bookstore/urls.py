from . import views
from django.urls import path ,include


urlpatterns = [
   #path('', views.home, name='home'),
    path('', views.login_form, name='home'),
    path('login/', views.loginView, name='login'),
    path('regform/', views.register_form, name='regform'),
    path('register/', views.registerView, name='register'),
    path('logout/', views.logoutView, name='logout'),
   path('forgot/', views.forgot, name='forgot'),

    path('librarian/', views.librarian, name='librarian'),
    path('publisher/', views.publisher, name='publisher'),
    path('dashboard/', views.dashboard, name='dashboard'),
#admin
     path('create_user_form/', views.create_user_form, name='create_user_form'),
     path('aluser/', views.ListUserView.as_view(), name='aluser'),
     path('alvuser/<int:pk>', views.ALViewUser.as_view(), name='alvuser'),
     path('aeuser/<int:pk>', views.AEditUser.as_view(), name='aeuser'),
     path('aduser/<int:pk>', views.ADeleteUser.as_view(), name='aduser'),
     path('aabook_form/', views.aabook_form, name='aabook_form'),
     path('aabook/', views.aabook, name='aabook'),
     path('albook/', views.ABookListView.as_view(), name='albook'),
     path('ambook/', views.AManageBook.as_view(), name='ambook'),
    path('adbook/<int:pk>', views.ADeleteBook.as_view(), name='adbook'),
    path('avbook/<int:pk>', views.AViewBook.as_view(), name='avbook'),
    path('aebook/<int:pk>', views.AEditView.as_view(), name='aebook'),
     path('alchat/', views.AListChat.as_view(), name='alchat'),
    path('acchat/', views.ACreateChat.as_view(), name='acchat'),
    path('asearch/', views.asearch, name='asearch'),
    path('create_use/', views.create_user, name='create_user'),
     #path('aluser/', views.ListUserView.as_view(), name='aluser'),

   path('adrequest/', views.ADeleteRequest.as_view(), name='adrequest'),
   path('afeedback/', views.AFeedback.as_view(), name='afeedback'),
   
    path('adbookk/<int:pk>', views.ADeleteBookk.as_view(), name='adbookk'),




# Publisher URL's
   path('publisher/', views.UBookListView.as_view(), name='publisher'),
    path('about/', views.about, name='about'),
    path('ulchat/', views.UListChat.as_view(), name='ulchat'),
    path('ucchat/', views.UCreateChat.as_view(), name='ucchat'),
    path('request_form/', views.request_form, name='request_form'),
    path('feedback_form/', views.feedback_form, name='feedback_form'),
    path('delete_request/', views.delete_request, name='delete_request'),
    path('send_feedback/', views.send_feedback, name='send_feedback'),



]

