import ftplib
from ..models import Storm, Advisory
import datetime


def connect():
    base_url = 'ftp.nhc.noaa.gov'
    ftp = ftplib.FTP(base_url)
    ftp.login()
    ftp.cwd('atcf/pub/')

    return ftp

def format_date(row):
    print(row)
    months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
    data = row.split()
    month =months.index(data[-3])+1
    day = int(data[-2])
    year = int(data[-1])
    if len(data[0])==4:
        x = data[0][:2]
    else:
        x = data[0][0]
    hour = int(x)

    return {'month':month, 'day':day, 'year':year, 'hour':hour}

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
        for i, row in enumerate(fp[0].split("\\n")):
            fp.append(row)
            if "LOCATION..." in row:
                location = format_location(row)
            elif "MAXIMUM SUSTAINED WINDS..." in row:
                max_s_winds = format_max_sustained_winds(row)
            elif " 2017" in row and len(row.split()) == 7:
                date_dict = format_date(row)




        print(date_dict)


        new_advisory = Advisory(advisory_id=advisory_id,
                                stormid=storm,
                                date=datetime.datetime(date_dict['year'],
                                                       date_dict['month'],
                                                       date_dict['day'],
                                                       date_dict['hour']),
                                storm_location=location,
                                max_sus_wind=max_s_winds,
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







