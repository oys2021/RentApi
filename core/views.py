from django.shortcuts import render

def api_root(request):
    return render(request, 'core/api_home.html')
