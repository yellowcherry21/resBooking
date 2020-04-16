import datetime

def Intersection(a1,b1,a2,b2):
    if (a1<b2 and b2<b1) or (a1<a2 and a2<b1) or (a2<b1 and b1<b2) or (a2<a1 and a1<b2) or (a1==a2 and b1==b2):
        return True
    else:
        return False

BigStruct = []
f = open('resource_bookings_input.txt', 'r')
f.readline()
List = f.readlines()

j=0
while j<len(List):
   Str = List[j]
   i=0
   ResourceId=Str[0:Str.find(",")]

   i=Str.find(",")
   StartDateTime = datetime.datetime(int(Str[i+1:i+5]),int(Str[i+6:i+8]),int(Str[i+9:i+11]),int(Str[i+12:i+14]),int(Str[i+15:i+17]),int(Str[i+18:i+20]))
   
   i=Str.rfind(",")
   EndDateTime   = datetime.datetime(int(Str[i+1:i+5]),int(Str[i+6:i+8]),int(Str[i+9:i+11]),int(Str[i+12:i+14]),int(Str[i+15:i+17]),int(Str[i+18:i+20]))
   
   Struct = [ResourceId, StartDateTime, EndDateTime]
   BigStruct.append(Struct)
   j=j+1

def IsResourceAvailable(ResourceId, StartDateTime, EndDateTime):
    i=0
    while i<len(BigStruct):
        if ResourceId==BigStruct[i][0] and Intersection(StartDateTime,EndDateTime,BigStruct[i][1],BigStruct[i][2]):
            return False
        i=i+1
    return True

def FindFreeInterval(StartDateTime, EndDateTime):
    FreeResources=[]
    for i in BigStruct:
        if IsResourceAvailable(i[0], StartDateTime, EndDateTime)==False:
            continue
        FreeResources.append(i[0])
    print("Free Resources list:")
    print(list(set(FreeResources)))

a=datetime.datetime(2020,3,28,12,0,0)
b=datetime.datetime(2020,3,28,14,0,0)

def Solving():
    print('start solving')
    FindFreeInterval(a,b)
    return IsResourceAvailable("427",a,b)

def main():
    print('main start');

if (__name__ == '__main__'):
    main();

def Test_Positive():
    print('start test')
    # Arrange
    # Read data from file
    # Act
    result = Solving()
    # Assert
    if (result):
        print('Test succeeded')
    else:
        print('Test fail')

Test_Positive()