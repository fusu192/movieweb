
from django.shortcuts import render

def page_not_found(request,exception):
    return render(request, '404.html')

def page_permission_denied(request,exception):
    return render(request, '403.html')

def page_inter_error(request):
    return render(request, '500.html')


def bad_request(request,exception):
    return render(request, '400.html')