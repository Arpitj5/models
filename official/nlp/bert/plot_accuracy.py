import csv
import matplotlib.pyplot as plt
import numpy as np

x= [11,10,9,8,7,6,5,4,3,2,1,0]
y = np.zeros((12, len(x)))

file = open('accuracy_inference.csv')
data_arr = np.loadtxt(file,delimiter=",")

print("len:"+str(len(data_arr)))

for i in range(len(data_arr)):
    y[int(data_arr[i][0])-1, x.index(int(data_arr[i][1]))] = data_arr[i][2]

x2 = [str(x0) for x0 in x]

for i in range(12):
    plt.plot(x2,y[i,:], label='layer'+str(i+1),linestyle="-")
plt.legend()
plt.show()