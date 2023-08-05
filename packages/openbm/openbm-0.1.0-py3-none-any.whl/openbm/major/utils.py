# import pendulum


# def decode_jobid(jobid, dayshift, tz):
#    """ Create a datetime instance along with the job name and schedule type
#        from jobid string"""
#    offset = int(jobid[-5:])
#    juliandate = jobid[-8:-5]
#    schedule_type = jobid[-9]
#    job_name = jobid[:-10]
#    timestamp = pendulum.from_format(juliandate, 'DDDD', tz=tz)
#    if pendulum.now().format('DDDD') < juliandate:
#        timestamp = timestamp.subtract(years=1)
#    timestamp = timestamp.set(hour=dayshift.hour, minute=dayshift.minute,
#                              second=dayshift.second)
#    timestamp = timestamp.add(seconds=offset)
#    return (timestamp, job_name, schedule_type)


def dsndate_fmt(datetime):
    """ Converts a datetime object to a DSN time format.
    Given the following time object time(2017, 11, 3, 9) will return the
    following string: D171103 """
    return f"D{datetime.strftime('%y%m%d')}"


def dsntime_fmt(datetime):
    """ Converts a datetime object to a DSN time format.
    Given the following time object time(2017, 11, 3, 9, 11, 0, 20)
    will return the following string: T110020"""
    return f'T{datetime.strftime("%H%M%S")}'
