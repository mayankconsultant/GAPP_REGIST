import csv

from REGISTER.models import states, county, payam


def run():
    states.objects.all().delete()
    county.objects.all().delete()
    payam.objects.all().delete()

    fhand = open('all_data.csv')

    reader = csv.reader(fhand)

    for r in reader:
        # print(r)
        s, created = states.objects.get_or_create(name=r[0])
        c, created = county.objects.get_or_create(name=r[1], states=s)
        p, created = payam.objects.get_or_create(name=r[2], county=c)
