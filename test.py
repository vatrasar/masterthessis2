import random
row1=[2,3,4]
row2=[1,2000999,3.4]
row3=[123944,3.343434,5.5343434]
rows=[]
rows.append(row1)
rows.append(row2)
rows.append(row3)
for i in rows:
    print("%10.2f %10.2f %.2f"%(i[0],i[1],i[2]))
