from django.shortcuts import render

def test_link(request):
    return render(request, 'test.html')

def index(request):
    return render(request, 'index.html')