from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from collections import defaultdict
from datetime import timedelta, date

from . import models
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

class Home(LoginRequiredMixin, View):

    def get(self, request):

        context = {
            
        }
        return render(request, 'home.html', context)
    
class Friendship(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        friendships = models.Friendship.objects.filter(
            Q(user_1=request.user) | Q(user_2=request.user),
            status=1
        )

        # Get all friend IDs (i.e., the user in the friendship that is not the current user)
        friend_ids = friendships.values_list('user_1', 'user_2')

        # Flatten and filter out self
        friend_ids_flat = set()
        for u1, u2 in friend_ids:
            if u1 != request.user.id:
                friend_ids_flat.add(u1)
            if u2 != request.user.id:
                friend_ids_flat.add(u2)

        # Exclude current friends and self
        users = models.User.objects.exclude(id__in=friend_ids_flat).exclude(id=request.user.id)

        request_sent_ids = models.Friendship.objects.filter(user_1=request.user, status=0).values_list('user_2', flat=True)
        request_recieved_ids = models.Friendship.objects.filter(user_2=request.user, status=0).values_list('user_1', flat=True)
        for user in users:
            user.pending_request_sent = user.id in request_sent_ids
            user.pending_request_recieved = user.id in request_recieved_ids


        context = {
            'friendships': friendships,
            'users': users
        }
        return render(request, 'friendships.html', context)
    
    def post(self, request):
        

        if request.POST.get('user_2_id'):
            user_1 = request.user
            user_2_id = request.POST.get('user_2_id')
            user_2 = get_object_or_404(models.User, id=user_2_id)

            if models.Friendship.objects.filter(
                Q(user_1=user_1, user_2=user_2) | Q(user_1=user_2, user_2=user_1)
            ).exists():
                return redirect('friendships')
                # return HttpResponse(f'Friendship or friendship request between you and {user_2.username} already exists.')
            else:
                new_friendship = models.Friendship(user_1=user_1, user_2=user_2)
                new_friendship.save()
                return redirect('friendships')
                # return HttpResponse(f'Friendship request succesfully sent to {user_2.username}!')
        else:
            if request.POST.get('delete_request'):
                user_2 = request.user
                user_1_id = request.POST.get('user_1_id')
                user_1 = get_object_or_404(models.User, id=user_1_id)

                friendship = get_object_or_404(Friendship, user_1=user_1, user_2=user_2, status=0)
                friendship.delete()

                return redirect('friendships')
                # return HttpResponse(f'You denied {user_1.username}'s friendship request!')
            else:
                user_2 = request.user
                user_1_id = request.POST.get('user_1_id')
                user_1 = get_object_or_404(models.User, id=user_1_id)

                friendship = get_object_or_404(models.Friendship, user_1=user_1, user_2=user_2, status=0)
                friendship.status = 1
                friendship.save()

                return redirect('friendships')
                # return HttpResponse(f'Now you and {user_1.username} are friends!')

class Memos(LoginRequiredMixin, View):
    def get(self, request, id):
        other_user = get_object_or_404(models.User, id=id)

        memos = models.Memo.objects.filter(
            Q(user_1=request.user, user_2=other_user) | Q(user_1=other_user, user_2=request.user)
        )

        # Agrupa os memos por data
        memos_by_date = defaultdict(list)
        for memo in memos:
            memos_by_date[memo.date].append(memo)

        # Descobre o intervalo de datas
        if memos:
            min_date = min(memo.date for memo in memos)
        else:
            min_date = date.today()

        max_date = date.today()

        # Cria um dicionário com todas as datas (mesmo sem memo)
        full_memos = {}
        current = min_date
        while current <= max_date:
            full_memos[current] = memos_by_date.get(current, [])
            current += timedelta(days=1)

        memos = dict(sorted(full_memos.items()))

        have_sent_today = False
        for memo in memos.get(date.today(), []):
            if memo.user_1 == request.user:
                have_sent_today = True
                break

        
        context = {
            'other_user': other_user,
            'memos': memos,
            'today': date.today(),
            'current_user': request.user,
            'have_sent_today': have_sent_today
        }
        return render(request, 'memos.html', context)
    
    def post(self, request, id):
        user_1 = request.user
        user_2 = get_object_or_404(models.User, id=id)
        content = request.POST.get('content')
        image = request.POST.get('image')

        new_memo = models.Memo(user_1=user_1, user_2=user_2, content=content, image=image)
        new_memo.save()

        return redirect('memos', id=id)