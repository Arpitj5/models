import csv
import matplotlib.pyplot as plt
import numpy as np

x= [32,24,16,12,8,6,4,3]
y = np.zeros((12, len(x)))

file = open('accuracy_combined.csv')
data_arr = np.loadtxt(file,delimiter=",")

print("len:"+str(len(data_arr)))

for i in range(len(data_arr)):
    y[int(data_arr[i][1])-1, x.index(int(data_arr[i][2]))] = data_arr[i][3]
    
x2 = [str(x0) for x0 in x]

for i in range(12):
    plt.plot(x2,y[i,:], label='layer'+str(i+1),linestyle="-")
plt.legend()
plt.show()