from django.http import HttpResponse

def index(request):
    return HttpResponse("Bacckend en Django: Helados Villaizan")
