from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.
def index(request):
    utilities = Utility.objects.order_by('name')
    context = {'utilities': utilities}
    return render(request, 'index.html', context)


def utility(request, utility_id):
    utility = get_object_or_404(Utility, pk=utility_id)
    bills = utility.bill_set.order_by('end_date')
    return render(request, 'utility.html', {'utility': utility, 'bills': bills})


def month(request):
    occupants = Occupant.objects.
    return render(request, 'month.html', {})
