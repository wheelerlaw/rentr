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
    year_month = request.GET['month']

    year = int(year_month[:4])
    month = int(year_month[5:])
    days_in_month = calendar.monthrange(year, month)[1]

    first_of_month = date(year, month, 1)
    last_of_month = date(year, month, days_in_month)

    if month is 1:
        next_month_name = calendar.month_abbr[month+1]
        prev_month_name = calendar.month_abbr[12]

        next_year_month = str(year) + '-2'
        prev_year_month = str(year-1) + '-12'

    elif month is 12:
        next_month_name = calendar.month_abbr[1]
        prev_month_name = calendar.month_abbr[month-1]

        next_year_month = str(year+1) + '-01'
        prev_year_month = str(year) + '-11'

    else:
        next_month_name = calendar.month_abbr[month+1]
        prev_month_name = calendar.month_abbr[month-1]

        next_year_month = str(year) + '-' + ('00' + str(month+1))[-2:]
        prev_year_month = str(year) + '-' + ('00' + str(month-1))[-2:]

    occupants = Occupant.objects\
        .filter(end_date__gte=first_of_month, start_date__lte=last_of_month)\
        .order_by('name')

    utilities = Utility.objects\
        .filter(bill__end_date__gte=first_of_month, bill__start_date__lte=last_of_month)\
        .order_by('name')\
        .values_list('name', flat=True)\
        .distinct()


    charges = {}

    charges['total'] = {'rent': 0}
    for utility in utilities:
        charges['total'][utility] = 0

    for occupant in occupants:
        charges[occupant.name] = {'rent': 0}
        for utility in utilities:
            charges[occupant.name][utility] = 0

    for day in range(1, days_in_month+1):
        this_day = date(year, month, day)
        for occupant in occupants:
            if occupant.start_date <= this_day <= occupant.end_date:
                charges[occupant.name]['rent'] += occupant.rent / days_in_month
                charges['total']['rent'] += occupant.rent / days_in_month
            else:
                # Need to distribute to other occupants
                other_occupants = Occupant.objects.filter(end_date__gte=this_day, start_date__lte=this_day).exclude(name=occupant.name)
                for other_occupant in other_occupants:
                    charges[other_occupant.name]['rent'] += occupant.rent / days_in_month / len(other_occupants)
                    charges['total']['rent'] += occupant.rent / days_in_month / len(other_occupants)

        bills = Bill.objects.filter(end_date__gte=this_day, start_date__lte=this_day)

        for bill in bills:
            billing_cycle_len = bill.get_days_for_billing_cycle()
            occupants_for_this_day = Occupant.objects.filter(end_date__gte=this_day, start_date__lte=this_day)
            for occupant_for_this_day in occupants_for_this_day:
                charges[occupant_for_this_day.name][bill.utility.name] += bill.charge\
                                                                          / billing_cycle_len / len(occupants_for_this_day)
                charges['total'][bill.utility.name] += bill.charge \
                                                       / billing_cycle_len / len(occupants_for_this_day)

    for occupant in charges:
        total = 0
        for occupant_charge in charges[occupant]:
            if occupant_charge is not "rent":
                total += charges[occupant][occupant_charge]
        charges[occupant]['total'] = total

    month_name = calendar.month_name[month]

    context = {
        'month_name': month_name,
        'occupants': occupants,
        'utilities': utilities,
        'charges': charges,
        'next_year_month': next_year_month,
        'prev_year_month': prev_year_month,
        'next_month_name': next_month_name,
        'prev_month_name': prev_month_name
    }
    return render(request, 'month.html', context)
