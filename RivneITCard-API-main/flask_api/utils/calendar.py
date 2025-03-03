from datetime import datetime, timedelta

def get_calendar(month, year):
    # Create a list of tuples of each day of the month and its day of the week
    # (day, weekday)
    month_days = []
    date = datetime(year, month, 1)
    while date.month == month:
        month_days.append((date.day, date.weekday()))
        date += timedelta(days=1)

    # Create a list of dates for the month
    calendar = []
    for day, weekday in month_days:
        if weekday == 6:
            week = [None, None, None, None, None, None, None]
        if day == 1:
            week = [None] * weekday + [datetime(year, month, day)]
        else:
            week.append(datetime(year, month, day))
            if weekday == 6:
                calendar.append(week)
        if day == month_days[-1][0]:
            week += [None] * (6 - weekday)
            calendar.append(week)

    print(calendar)

_month = 3
_year = 2023
get_calendar(_month, _year)
