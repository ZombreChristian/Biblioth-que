from datetime import timezone
import itertools
from django.utils import timezone

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.hashers import make_password
from bookstore import models
from bookstore.forms import BookForm, ChatForm, UserForm
from bookstore.models import Book, Chat, CustomUser, DeleteRequest, Feedback
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

from django.contrib import auth, messages

def login_form(request):
	return render(request, 'bookstore/login.html')

def register_form(request):
	return render(request, 'bookstore/register.html')


def forgot(request):
      return render(request, 'bookstore/forget_password.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_superuser:
                return redirect('dashboard')
            elif user.is_librarian:
                return redirect('librarian')
            else:
                return redirect('publisher')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('home')



    

def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        hashed_password = make_password(password)

        user = User(username=username, email=email, password=hashed_password)
        user.save()

        messages.success(request, 'Compte créé avec succès!!!')
        return redirect('home')
    else:
        messages.error(request, 'Création échouée, veuillez réessayer')
        return redirect('regform')



def logoutView(request):
	logout(request)
	return redirect('home')

def dashboard(request):
	book = Book.objects.all().count()
	user = CustomUser.objects.all().count()

	context = {'book':book, 'user':user}

	return render(request, 'dashboard/home.html', context)

def publisher(request):
	return render(request, 'publisher/home.html')

def librarian(request):
    book_count = Book.objects.all().count()
    user_count = CustomUser.objects.all().count()
    context = {'book_count': book_count, 'user_count': user_count}

    return render(request, 'librarian/home.html', context)

def create_user_form(request):
    choice = ['1', '0', 'Publisher', 'Admin', 'Librarian']
    choice = {'choice': choice}

    return render(request, 'dashboard/add_user.html', choice)

def create_user(request):
    choice = ['1', '0', 'Publisher', 'Admin', 'Librarian']
    choice = {'choice': choice}
    if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            userType=request.POST['userType']
            email=request.POST['email']
            password=request.POST['password']
            password = make_password(password)
            print("User Type")
            print(userType)
            if userType == "Publisher":
                a = CustomUser(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_publisher=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')
            elif userType == "Admin":
                a = CustomUser(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')
            elif userType == "Librarian":
                a = CustomUser(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_librarian=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('aluser')    
            else:
                messages.success(request, 'Member was not created')
                return redirect('create_user_form')
    else:
        return redirect('create_user_form')


class ListUserView(generic.ListView):
    model = CustomUser
    template_name = 'dashboard/list_users.html'
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        return CustomUser.objects.order_by('-id')
    


class ALViewUser(DetailView):
    model = CustomUser
    template_name='dashboard/user_detail.html'


class AEditUser(SuccessMessageMixin, UpdateView): 
    model = CustomUser
    form_class = UserForm
    template_name = 'dashboard/edit_user.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully updated"


class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = CustomUser
    template_name='dashboard/confirm_delete3.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully deleted"


def aabook_form(request):
	return render(request, 'dashboard/add_book.html')




def aabook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES['cover']
        pdf = request.FILES['pdf']
        uploaded_by = request.user

        a = Book(
            title=title,
            author=author,
            year=year,
            publisher=publisher,
            desc=desc,
            cover=cover,
            pdf=pdf,
            uploaded_by=uploaded_by
        )
        a.save()

        messages.success(request, 'Book was uploaded successfully!!!!!')
        return redirect('albook')
    else:
        messages.error(request, 'Book was not uploaded successfully')
        return redirect('aabook_form')


class ABookListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/book_list.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')


class AManageBook(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'dashboard/manage_books.html'
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		return Book.objects.order_by('-id')

class ADeleteBook(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'dashboard/confirm_delete2.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was dele successfully'

class AViewBook(LoginRequiredMixin,DetailView):
	model = Book
	template_name = 'dashboard/book_detail.html'
        


class AEditView(LoginRequiredMixin,UpdateView):
	model = Book
	form_class = BookForm
	template_name = 'dashboard/edit_book.html'
	success_url = reverse_lazy('ambook')
	success_message = 'Data was updated successfully'


class AListChat(LoginRequiredMixin, ListView):
	model = Chat
	template_name = 'dashboard/chat_list.html'

	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


class ACreateChat(LoginRequiredMixin, CreateView):
	form_class = ChatForm
	model = Chat
	template_name = 'dashboard/chat_form.html'
	success_url = reverse_lazy('alchat')        
        
class AFeedback(LoginRequiredMixin,ListView):
	model = Feedback
	template_name = 'dashboard/feedback.html'
	context_object_name = 'feedbacks'
	paginate_by = 3

	def get_queryset(self):
		return Feedback.objects.order_by('-id')


class ADeleteRequest(LoginRequiredMixin,ListView):
	model = DeleteRequest
	template_name = 'dashboard/delete_request.html'
	context_object_name = 'feedbacks'
	paginate_by = 3

	def get_queryset(self):
		return DeleteRequest.objects.order_by('-id')

def asearch(request):
    query = request.GET['query']
    print(type(query))
    #data = query.split()
    data = query
    print(len(data))
    if( len(data) == 0):
        return redirect('dashborad')
    else:
                a = data

                # Searching for It
                qs5 =models.Book.objects.filter(id__iexact=a).distinct()
                qs6 =models.Book.objects.filter(id__exact=a).distinct()

                qs7 =models.Book.objects.all().filter(id__contains=a)
                qs8 =models.Book.objects.select_related().filter(id__contains=a).distinct()
                qs9 =models.Book.objects.filter(id__startswith=a).distinct()
                qs10 =models.Book.objects.filter(id__endswith=a).distinct()
                qs11 =models.Book.objects.filter(id__istartswith=a).distinct()
                qs12 =models.Book.objects.all().filter(id__icontains=a)
                qs13 =models.Book.objects.filter(id__iendswith=a).distinct()


                files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

                res = []
                for i in files:
                    if i not in res:
                        res.append(i)


                # word variable will be shown in html when user click on search button
                word="Searched Result :"
                print("Result")

                print(res)
                files = res

                page = request.GET.get('page', 1)
                paginator = Paginator(files, 10)
                try:
                    files = paginator.page(page)
                except PageNotAnInteger:
                    files = paginator.page(1)
                except EmptyPage:
                    files = paginator.page(paginator.num_pages)

                if files:
                    return render(request,'dashboard/result.html',{'files':files,'word':word})
                return render(request,'dashboard/result.html',{'files':files,'word':word})

class ADeleteBookk(LoginRequiredMixin,DeleteView):
	model = Book
	template_name = 'dashboard/confirm_delete.html'
	success_url = reverse_lazy('dashboard')
	success_message = 'Data was dele successfully'


class UBookListView(LoginRequiredMixin,ListView):
	model = Book
	template_name = 'publisher/book_list.html'
	context_object_name = 'books'
	paginate_by = 2

	def get_queryset(self):
		return Book.objects.order_by('-id')



def about(request):
	return render(request, 'publisher/about.html')	        


class UListChat(LoginRequiredMixin, ListView):
	model = Chat
	template_name = 'publisher/chat_list.html'

	def get_queryset(self):
		return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')

class UCreateChat(LoginRequiredMixin, CreateView):
	form_class = ChatForm
	model = Chat
	template_name = 'publisher/chat_form.html'
	success_url = reverse_lazy('ulchat')



def request_form(request):
	return render(request, 'publisher/delete_request.html')

def feedback_form(request):
	return render(request, 'publisher/send_feedback.html')


# 

def delete_request(request):
    if request.method == 'POST':
        book_id = request.POST.get('delete_request')
        current_user = request.user

        if book_id:
            username = current_user.username
            user_request = f"{username} wants book with id {book_id} to be deleted"
            DeleteRequest.objects.create(delete_request=user_request)
            messages.success(request, 'Request was sent')
        else:
            messages.error(request, 'Book ID is required')

    return redirect('request_form')



# def send_feedback(request):
# 	if request.method == 'POST':
# 		feedback = request.POST['feedback']
# 		current_user = request.user
# 		user_id = current_user.id
# 		username = current_user.username
# 		feedback = username + " " + " says " + feedback

# 		a = Feedback(feedback=feedback)
# 		a.save()
# 		messages.success(request, 'Feedback was sent')
# 		return redirect('feedback_form')
# 	else:
# 	    messages.error(request, 'Feedback was not sent')
# 	    return redirect('feedback_form')

def send_feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        current_user = request.user

        if feedback_text:
            feedback = f"{current_user.username} says {feedback_text}"
            Feedback.objects.create(feedback=feedback)
            messages.success(request, 'Feedback was sent')
        else:
            messages.error(request, 'Feedback text is required')

    return redirect('feedback_form')