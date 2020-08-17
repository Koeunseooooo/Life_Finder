from django.shortcuts import render

def first(request):
    return render(request, 'main/main.html')
