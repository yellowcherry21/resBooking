from datetime import datetime, date, time

from flask import Flask
from flask import render_template, redirect, url_for, request


def intersection(a1, b1, a2, b2):
    if (a1 < b2 < b1) or (a1 < a2 < b1) or (a2 < b1 < b2) or (a2 < a1 < b2) or (a1 == a2 and b1 == b2):
        return True
    else:
        return False


BigStruct = []
ListID = []
f = open('resource_bookings_input.txt', 'r')
f.readline()
List = f.readlines()

j=0
while j<len(List):
   Str = List[j]
   i=0
   ResourceId=Str[0:Str.find(",")]

   i=Str.find(",")
   StartDateTime = datetime(int(Str[i+1:i+5]),int(Str[i+6:i+8]),int(Str[i+9:i+11]),int(Str[i+12:i+14]),int(Str[i+15:i+17]),int(Str[i+18:i+20]))

   i=Str.rfind(",")
   EndDateTime   = datetime(int(Str[i+1:i+5]),int(Str[i+6:i+8]),int(Str[i+9:i+11]),int(Str[i+12:i+14]),int(Str[i+15:i+17]),int(Str[i+18:i+20]))

   Struct = [ResourceId, StartDateTime, EndDateTime]
   BigStruct.append(Struct)
   ListID.append(ResourceId)
   j=j+1


def IsResourceAvailable(ResourceId, StartDateTime, EndDateTime):
    i = 0
    while i<len(BigStruct):
        if ResourceId == BigStruct[i][0] and intersection(StartDateTime, EndDateTime, BigStruct[i][1], BigStruct[i][2]):
            return False
        i = i+1
    return True


def AvailableToday(resourceid, str_date):
    x = date(int(str_date[0:4]), int(str_date[5:7]), int(str_date[8:10]))
    start = datetime.combine(x, time(0, 0))
    end = datetime.combine(x, time(23, 59, 59))
    return IsResourceAvailable(resourceid, start, end)


def FindFreeInterval(StartDateTime, EndDateTime):
    FreeResources=[]
    for i in BigStruct:
        if IsResourceAvailable(i[0], StartDateTime, EndDateTime)==False:
            continue
        FreeResources.append(i[0])
    return list(set(FreeResources))


d = list(range(737425, 737791))
DateList = []
for i in d:
    DateList.append(str(date.fromordinal(i)))


app = Flask(__name__)
results = []
ListID = list(set(ListID))


@app.route('/', methods=['GET'])
def start_page():
    return render_template('booking.html', results=[])


@app.route('/main', methods=['GET'])
def main():
    return render_template('booking.html', results=results)


@app.route('/table')
def table():
    return render_template('table.html', DateList=DateList, ListID=ListID, AvailableToday=AvailableToday)


@app.route('/add_result', methods=['POST'])
def add_result():
    a = datetime(int(request.form['StartDateTime'][0:4]), int(request.form['StartDateTime'][5:7]), int(request.form['StartDateTime'][8:10]), 0, 0, 0)
    b = datetime(int(request.form['EndDateTime'][0:4]), int(request.form['StartDateTime'][5:7]), int(request.form['StartDateTime'][8:10]), 23, 59, 59)
    global results
    results = ', '.join(FindFreeInterval(a, b))
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()
