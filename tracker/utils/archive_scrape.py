import ftplib
from ..models import Storm, Advisory
import datetime



def classify_storm(row):
    print(row)
    choices = Advisory.category_choices
    category = [(value, key.upper()) for value, key in choices if key.upper() in row]
    try:
        name = row[row.index(category[0][1])+len(category[0][1]):row.index('ADVISORY')]
    except:
        name = "none"
    name = name.rstrip()
    name = name.lstrip()
    if len(category)>1:
        return category[0][0], name
    else:
        return 0, name




def normalize_time(timezone, datetime_obj):
    timezones = {
        'AST': -1,
        'EST': 0,
        'EDT': -1,
        'CST': 1,
        'CDT': 0,
        'MST': 2,
        'MDT': 1,
        'PST': 3,
        'PDT': 2,
        'AKST': 4,
        'AKDT': 3,
        'HAST': 5,
        'HADT': 4,
	    'HST':5,
	    'HDT':4,
    }
    return datetime_obj +datetime.timedelta(hours =timezones[timezone] )


def connect():
    print("attempting to connect..")
    base_url = 'ftp.nhc.noaa.gov'
    try:
        ftp = ftplib.FTP(base_url)
        print("connected to %s at %s, attempting to log in"%(base_url, datetime.datetime.now()))
        ftp.login()
    except:
        print("failed to connect to %s"%(base_url))
    print("logged in..")
    ftp.cwd('atcf/archive/2015/messages/')
    print("switching directories")

    return ftp

def format_date(row):
    print(row)
    months = 'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()
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
        if hour ==24:
            hour+= -12

    return {'month':month, 'day':day, 'year':year, 'hour':hour, 'timezone':timezone}

def format_location(row):
    coords = row.split('...')
    return coords[1]

def format_max_sustained_winds(row):
    trash, spd , km= row.split('...')

    return int(spd.split()[0])

def format_speed(row):
    first = row.split(' AT ')[1]
    second = first.split('MPH')[0]
    return int(second.strip())

def format_pressure(row):
    first = row.split('...')[1]
    return float(first.split()[0])




def check_advisory(advisory_num, advisory_id, storm,):
    if not Advisory.objects.filter(advisory_id=advisory_id).exists():
        # storm has been seen before, advisory has not. Add Advisory
        fp = []
        ftp = connect()
        ftp.retrbinary('RETR ' + advisory_id, lambda s, w=fp.append: w(str(s)))
        ftp.close()
        category = 0
        content = ""
        for i, row in enumerate(fp[0].split("\\n")):

            content = "\n".join([content, row])
            if "LOCATION..." in row:
                location = format_location(row)
            elif "MAXIMUM SUSTAINED WINDS..." in row:
                max_s_winds = format_max_sustained_winds(row)
            elif " 2015" in row and len(row.split()) == 7:
                date_dict = format_date(row)
            elif 'ADVISORY NUMBER' in row:
                category, name = classify_storm(row)
            elif 'PRESENT MOVEMENT...' in row:
                try:
                    speed = format_speed(row)
                except:
                    speed = 0
            elif 'MINIMUM CENTRAL PRESSURE' in row:
                pressure = format_pressure(row)




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
                                content=content)
        new_advisory.save()


def check_storm(stormid):
    if not Storm.objects.filter(stormid=stormid).exists():
        cyclone_num = stormid[:2]
        cyclone_num = cyclone_num[:-4]
        print(cyclone_num)
        newstorm = Storm(stormid=stormid,
                         region=stormid[:2],
                         annual_cyclone_number=1,
                         year = 2015
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
        if 'public' in str(ftpfile):

            stormid, type, advisory_num, *rest = ftpfile.split(".")

            storm = check_storm(stormid)
            check_advisory(advisory_num, ftpfile, storm)







