from django.shortcuts import render

# Create your views here.
def index_view(request):
    # request.session['username'] = 'linux'
    return render(request, 'index/index.html')