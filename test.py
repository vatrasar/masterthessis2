import random
test={}
for i in range(0,21):
    test[i]=0
for i in range(0,338):
  test[int((random.random()*1040)/50.0)]=test[int((random.random()*1040)/50.0)]+1
for i in test:
    print(test[i])