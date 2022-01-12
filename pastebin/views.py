from django.shortcuts import render


def index(request):
    context = {}
    context['title'] = 'PasteBin'
    return render(request, 'index.html', context)
