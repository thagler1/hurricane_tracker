import ftplib
from ..models import Storm, Advisory
import datetime



def classify_storm(row):
    print(row)
    choices = Advisory.category_choices
    category = [(value, key) for value, key in choices if key in row]
    name = row[row.index(category[0][1])+len(category[0][1]):row.index('Advisory')]
    name = name.rstrip()
    name = name.lstrip()
    return category[0][0], name




def normalize_time(timezone, datetime_obj):
    timezones = {
        'AST': -4,
        'EST': -5,
        'EDT': -4,
        'CST': -6,
        'CDT': -5,
        'MST': -7,
        'MDT': -6,
        'PST': -8,
        'PDT': -7,
        'AKST': -9,
        'AKDT': -8,
        'HAST': -10,
        'HADT': -9,
    }
    return datetime_obj +datetime.timedelta(hours =timezones[timezone]*-1 )


def connect():
    print("attempting to connect..")
    base_url = 'ftp.nhc.noaa.gov'
    ftp = ftplib.FTP(base_url)
    ftp.login()
    print("logged in..")
    ftp.cwd('atcf/pub/')
    print("switching directories")

    return ftp

def format_date(row):
    print(row)
    months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
    data = row.split()
    month =months.index(data[-3])+1
    day = int(data[-2])
    year = int(data[-1])
    timezone = data[2]
    am_pm = data[1]
    if len(data[0])==4:
        x = data[0][:2]
    else:
        x = data[0][0]
    hour = int(x)
    if am_pm == 'AM':
        pass
    else:
        hour+=12

    return {'month':month, 'day':day, 'year':year, 'hour':hour, 'timezone':timezone}

def format_location(row):
    coords = row.split('...')
    return coords[1]

def format_max_sustained_winds(row):
    trash, spd , km= row.split('...')
    return spd

def check_advisory(advisory_num, advisory_id, storm,):
    if not Advisory.objects.filter(advisory_id=advisory_id).exists():
        # storm has been seen before, advisory has not. Add Advisory
        fp = []
        ftp = connect()
        ftp.retrbinary('RETR ' + advisory_id, lambda s, w=fp.append: w(str(s)))
        ftp.close()
        category = 0
        for i, row in enumerate(fp[0].split("\\n")):

            fp.append(row)
            if "LOCATION..." in row:
                location = format_location(row)
            elif "MAXIMUM SUSTAINED WINDS..." in row:
                max_s_winds = format_max_sustained_winds(row)
            elif " 2017" in row and len(row.split()) == 7:
                date_dict = format_date(row)
            elif 'Advisory Number' in row:
                category, name = classify_storm(row)




        cdt_time = normalize_time(date_dict['timezone'],datetime.datetime(date_dict['year'],
                                                       date_dict['month'],
                                                       date_dict['day'],
                                                       date_dict['hour']))

        new_advisory = Advisory(advisory_id=advisory_id,
                                stormid=storm,
                                date=cdt_time,
                                storm_location=location,
                                max_sus_wind=max_s_winds,
                                category=category,
                                current_name = name,
                                content=("\n".join([line for line in fp])))
        new_advisory.save()


def check_storm(stormid):
    if not Storm.objects.filter(stormid=stormid).exists():
        cyclone_num = stormid[:2]
        cyclone_num = cyclone_num[:-4]
        print(cyclone_num)
        newstorm = Storm(stormid=stormid,
                         region=stormid[:2],
                         annual_cyclone_number=1,
                         year = 2017
                         )

        newstorm.save()
        return newstorm
    else:
        return Storm.objects.get(stormid=stormid)






def update_data():
    ftp = connect()
    dir_files = ftp.nlst() #these are the file names in str format
    ftp.close()

    # scroll through missing ftp files and build data set
    for ftpfile in dir_files[1:]:
        stormid, type, advisory_num = ftpfile.split(".")

        storm = check_storm(stormid)
        check_advisory(advisory_num, ftpfile, storm)







