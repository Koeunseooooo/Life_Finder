from django.shortcuts import render

# from datetime import date
# from datetime import datetime
# import arrow

import datetime

def first(request):
    today_date = datetime.date.today().isoformat()
    return render(request, 'main/main.html',{'today_date': today_date})


# from datetime import date


def base(request):
    today_date = datetime.date.today().isoformat()
    print(type(today_date))
    print(today_date)

    return render(request, 'main/base.html',{'today_date': today_date})


    # today = date.today()
    # today_date = str(today.year) + '-' + str(today.month).zfill(2) + '-' + str(today.day).zfill(2) + '/'
    # # today_date = today.time.strftime('%Y-%m-%d')
    # print(today_date)
    # today_date = str(date.today().strftime('%Y-%m-%d'))
    # arrow.utcnow().to('Asia/Seoul').format('YYYY-MM-DD')
    # today_date = datetime.today().strftime('%Y-%m-%d')
    # today_date = date.today().isoformat()