from ..models import cities
import csv
from django.contrib.gis.geos import GEOSGeometry

def add_cities():
    with open('cities_upload.csv',  encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if cities.objects.filter(name=row['NAME'], state=row['STATE']).exists():

                    pass
                else:
                    try:
                        print(row['NAME']+", "+ row['STATE'])
                        long = float(row['LONGITUDE'])
                        print()
                        lat = float(row['LATITUDE'])
                        new = cities(name=row['NAME'],
                                  state = row['STATE'],
                                  population=row['POP_2010'],
                                  coords=GEOSGeometry('POINT(%s %s)' % (long, lat), srid=4326),)

                        new.save()
                    except Exception as e:
                         print(e)
            except Exception as e:
                print(e)
        print("\n\nUPLOAD COMPLETE")



