company=[]
etf=[]

file=open('input.dat', 'r')
idx_etf=open('etf.dat', 'r')

while True :
    line=file.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    company.append(line)

del company[0]
file.close()

while True :
    line=idx_etf.readline()
    if len(line)==0:
        break
    line=line.lstrip()
    line=line.rstrip()
    etf.append(int(line))
idx_etf.close()

for i in etf:
    print(company[i])

##################### etf리스트 받아왔다 #####################

