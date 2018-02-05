from django.db import models
import calendar
from datetime import date


class Utility(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.name)


class Bill(models.Model):
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def get_charge_for_month(self, year, month):
        days_in_month = calendar.monthrange(year, month)[1]
        start = latest_date(date(year, month, 1), self.start_date)
        end = earliest_date(date(year, month, days_in_month), self.end_date)

        days_for_rent = (end-start).days + 1

        return self.charge / days_in_month * days_for_rent

    def get_days_for_billing_cycle(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return str(self.utility.name) + ": " + str(self.charge) + \
               ", " + calendar.month_abbr[self.start_date.month] + " " + str(self.start_date.day) + \
               " - " + calendar.month_abbr[self.end_date.month] + " " + str(self.end_date.day)


class Occupant(models.Model):
    name = models.CharField(max_length=1024)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def get_rent_for_month(self, year, month):
        days_in_month = calendar.monthrange(year, month)[1]
        start = latest_date(date(year, month, 1), self.start_date)
        end = earliest_date(date(year, month, days_in_month), self.end_date)

        days_for_rent = (end-start).days + 1

        return self.rent / days_in_month * days_for_rent

    def __str__(self):
        return str(self.name)


def earliest_date(date1, date2):
    if date1 < date2:
        return date1
    else:
        return date2


def latest_date(date1, date2):
    if date1 > date2:
        return date1
    else:
        return date2
