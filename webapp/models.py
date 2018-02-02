from django.db import models
import calendar


class Utility(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.name)


class Bill(models.Model):
    utility = models.ForeignKey(Utility, on_delete=models.CASCADE)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.utility.name) + ": " + str(self.charge) + \
               ", " + calendar.month_abbr[self.start_date.month] + " " + str(self.start_date.day) + \
               " - " + calendar.month_abbr[self.end_date.month] + " " + str(self.end_date.day)


class Occupant(models.Model):
    name = models.CharField(max_length=1024)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.name)
