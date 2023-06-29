file=open('REFFINSTATEMENTIN_CHN.dat', 'r')

company=[]
while True :
    line=file.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    temp=line.split()
    company.append(temp)

del company[0]
file.close()

ric=[]
for i in company:
    ric.append(i[0].split('.')[1])
ric2=list(set(ric))

count=[0]*len(ric2)

for i in ric:
    for j in range(len(ric2)):
        if i==ric2[j]:
            count[j]+=1
print('REFFINSTATEMENTIN_CHN')
print(ric2)
print(count)

##########################################################
file=open('REFFINSTATEMENTIN_HKG.dat', 'r')

company=[]
while True :
    line=file.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    temp=line.split()
    company.append(temp)

del company[0]
file.close()

ric=[]
for i in company:
    ric.append(i[0].split('.')[1])
ric2=list(set(ric))

count=[0]*len(ric2)

for i in ric:
    for j in range(len(ric2)):
        if i==ric2[j]:
            count[j]+=1
print('REFFINSTATEMENTIN_HKG')
print(ric2)
print(count)


##########################################################
file=open('REFFINSTATEMENTIN_JPN.dat', 'r')

company=[]
while True :
    line=file.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    temp=line.split()
    company.append(temp)

del company[0]
file.close()

ric=[]
for i in company:
    ric.append(i[0].split('.')[1])
ric2=list(set(ric))

count=[0]*len(ric2)

for i in ric:
    for j in range(len(ric2)):
        if i==ric2[j]:
            count[j]+=1
print('REFFINSTATEMENTIN_JPN')
print(ric2)
print(count)



##########################################################
file=open('REFFINSTATEMENTIN_VNM.dat', 'r')

company=[]
while True :
    line=file.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    temp=line.split()
    company.append(temp)

del company[0]
file.close()

ric=[]
for i in company:
    ric.append(i[0].split('.')[1])
ric2=list(set(ric))

count=[0]*len(ric2)

for i in ric:
    for j in range(len(ric2)):
        if i==ric2[j]:
            count[j]+=1
print('REFFINSTATEMENTIN_VNM')
print(ric2)
print(count)
