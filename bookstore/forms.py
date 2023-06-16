
from django.contrib.auth.models import User
from django import forms

from bookstore.models import Book, Chat


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publisher', 'year', 'uploaded_by', 'desc')                



class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('message', )
