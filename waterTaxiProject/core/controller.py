from django.shortcuts import render

def signup_view(request):
    return render(request, 'core/SignUp.html')
