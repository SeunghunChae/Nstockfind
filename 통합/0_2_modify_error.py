import csv

error=[]
file=open('에러.csv', 'r')
line=file.readline() #헤더 갖다버림
while True :
    line=file.readline()
    if len(line)==0:
        break
    error.append(line.split(','))

for i in error:
    if 'fund' in i[3].lower():
            i[1]=i[1]+'fund'
    elif 'bond' in i[3].lower():
            i[1]=i[1]+'bond'
    elif 'shares' in i[3].lower():
            i[1]=i[1]+'shares'


file=open('에러.csv', 'r')
for i in error:
    result=','.join(i)
    with open('에러2.csv','a',newline='') as f:
            f.write(result)
