from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from services.models import Service
from django.shortcuts import render, redirect


def register_view(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)

        # role based redirect
        if user.user_type == 'provider':
            return redirect('/services/create/')
        else:
            return redirect('/services/')
        
    else:
            print(form.errors)   # 🔥 YE ADD KAR

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    services = Service.objects.all()
    return render(request, 'accounts/dashboard.html', {'services': services})