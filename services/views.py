from django.shortcuts import render, redirect
from .models import Service
from django.contrib.auth.decorators import login_required

def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'services': services})

@login_required
def create_service(request):
    if request.user.user_type != 'provider':
        return redirect('/')

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        price = request.POST.get('price')

        Service.objects.create(
            provider=request.user,
            title=title,
            description=desc,
            price=price
        )
        return redirect('/services/')

    return render(request, 'services/create.html')


def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/list.html', {'services': services})