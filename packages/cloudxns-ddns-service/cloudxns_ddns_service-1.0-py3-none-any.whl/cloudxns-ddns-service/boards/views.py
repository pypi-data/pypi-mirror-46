
from django.http import HttpResponse
from django.shortcuts import render
from .models import Board


# Create your views here.
def home_1(request):
    boards = Board.objects.all()
    boards_names = list()

    for board in boards:
        boards_names.append(board.name)

    response_html = '<br>'.join(boards_names)

    return HttpResponse(response_html)

def home_2(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def view_1(request):
    parm = request.GET['parm']
    print(parm)
    return HttpResponse('Hello, World 1 ! %s' %(parm))

def view_2(request, value):
    return HttpResponse("Hello, World 2 ! %s" % (value))

def view_3(request, value):
    return HttpResponse("Hello, World 3 ! %s" % (value))

def view_4(request, parm):
    return HttpResponse("Hello, World 4 ! %s" % (parm))
