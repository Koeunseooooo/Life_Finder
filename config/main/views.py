from django.shortcuts import render


# Create your views here.
def first(request):
    return render(request, 'main/main.html')
