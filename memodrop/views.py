from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


from . import forms

# Create your views here.
class Register(View):
    
    def get(self, request):
        context = {
            'register_form': forms.RegisterUser
        }

        return render(request, 'entry_point.html', context)
    
    def post(self, request):
        form = forms.RegisterUser(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        
        context = {
            'register_form': form
        }
        return render(request, 'entry_point.html', context)
    
class Login(LoginView):
    authentication_form = AuthenticationForm
    template_name = 'entry_point.html'
    next_page = '/'

class Main(LoginRequiredMixin, View):

    def get(self, request):
        return HttpResponse(f'Welcome {request.user.username}!')