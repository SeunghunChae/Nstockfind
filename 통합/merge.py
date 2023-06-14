import csv

for i in range(1,8):
    print(str(i)+'_정상.csv')
    file=open(str(i)+'_정상.csv', 'r')

    if i!=1:
        line=file.readline() # 첫번째 줄 날리기 
    while True :
        line=file.readline()
        if len(line)==0:
            break
        with open('정상.csv','a',newline='') as f:
            f.write(line)
    file.close()

for i in range(1,8):
    print(str(i)+'_에러.csv')
    file=open(str(i)+'_에러.csv', 'r')

    if i!=1:
        line=file.readline() # 첫번째 줄 날리기 
    while True :
        line=file.readline()
        if len(line)==0:
            break
        with open('에러.csv','a',newline='') as f:
            f.write(line)
    file.close()

for i in range(1,8):
    print(str(i)+'_누락목록.csv')
    file=open(str(i)+'_누락목록.csv', 'r')

    if i!=1:
        line=file.readline() # 첫번째 줄 날리기 
    while True :
        line=file.readline()
        if len(line)==0:
            break
        with open('누락목록.csv','a',newline='') as f:
            f.write(line)
    file.close()

for i in range(1,8):
    print(str(i)+'_한국.csv')
    file=open(str(i)+'_한국.csv', 'r')

    if i!=1:
        line=file.readline() # 첫번째 줄 날리기 
    while True :
        line=file.readline()
        if len(line)==0:
            break
        with open('한국.csv','a',newline='') as f:
            f.write(line)
    file.close()

