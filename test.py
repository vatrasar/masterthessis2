import numpy as np
test=np.random.RandomState()
test.normal()

for i in range(0,1000):
    print(test.normal())
