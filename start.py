from datetime import datetime, date, time

from flask import Flask
from flask import render_template, redirect, url_for, request
from typing import List


def intersection(a1, b1, a2, b2):
    if (a1 < b2 < b1) or (a1 < a2 < b1) or (a2 < b1 < b2) or (a2 < a1 < b2) or (a1 == a2 and b1 == b2):
        return True
    else:
        return False


def SomeText(a):
    return a+"A"


BigStruct = []
lisstID = []
f = open('resource_bookings_input.txt', 'r')
f.readline()
temp_list = f.readlines()

for Str in temp_list:
   if Str[Str.rfind(",")+1:Str.rfind(",")+5] == "2020":
       ResourceId = Str[0:Str.find(",")]

       i = Str.find(",")
       StartDateTime = datetime(int(Str[i+1:i+5]), int(Str[i+6:i+8]), int(Str[i+9:i+11]), int(Str[i+12:i+14]), int(Str[i+15:i+17]), int(Str[i+18:i+20]))

       i=Str.rfind(",")
       EndDateTime   = datetime(int(Str[i+1:i+5]), int(Str[i+6:i+8]), int(Str[i+9:i+11]), int(Str[i+12:i+14]), int(Str[i+15:i+17]), int(Str[i+18:i+20]))

       Struct = [ResourceId, StartDateTime, EndDateTime]
       BigStruct.append(Struct)
       lisstID.append(ResourceId)


def IsResourceAvailable(ResourceId, StartDateTime, EndDateTime):
    for el in BigStruct:
        if ResourceId == el[0] and intersection(StartDateTime, EndDateTime, el[1], el[2]):
            return False
    return True


def AvailableToday(resourceid, date):
    hourlist = [] # type: List[bool]
    for hour in range(24):
        start = datetime.combine(date, time(hour, 0))
        end = datetime.combine(date, time(hour, 59, 59))
        if IsResourceAvailable(resourceid, start, end):
            hourlist.append(True)
        else:
            hourlist.append(False)
    return hourlist


def FindFreeInterval(StartDateTime, EndDateTime):
    FreeResources=[]
    for i in BigStruct:
        if IsResourceAvailable(i[0], StartDateTime, EndDateTime)==False:
            continue
        FreeResources.append(i[0])
    return list(set(FreeResources))


today = date.today()
DateList = []
for i in list(range(737425, 737791)):
    DateList.append(date.fromordinal(i))


app = Flask(__name__)
results = [] # type: List[str]
lisstID = list(set(lisstID))


@app.route('/', methods=['GET'])
def start_page():
    return render_template('booking.html', results=[], today=today)


@app.route('/main', methods=['GET'])
def main():
    return render_template('booking.html', results=results, today=today)


@app.route('/table')
def table():
    return render_template('table.html', DateList=DateList, ListID=lisstID, AvailableToday=AvailableToday)


@app.route('/add_result', methods=['POST'])
def add_result():
    a = datetime(int(request.form['StartDateTime'][0:4]), int(request.form['StartDateTime'][5:7]), int(request.form['StartDateTime'][8:10]), 0, 0, 0)
    b = datetime(int(request.form['EndDateTime'][0:4]), int(request.form['StartDateTime'][5:7]), int(request.form['StartDateTime'][8:10]), 23, 59, 59)
    global results
    results = ', '.join(FindFreeInterval(a, b))
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()
