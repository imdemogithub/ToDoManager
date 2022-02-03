from django.shortcuts import render, redirect
from .forms import UserForm

# Create your views here.
def index(request):
    form = UserForm()
    return render(request, "index.html", {'form': form, 'title':'first page','candidates': ['deep','meet','nayan','kinjal']})

def form_data(request):
    print(request.POST['city'])
    return redirect(index)