import csv
import matplotlib.pyplot as plt
import numpy as np

d = {0: "layer selective, head incremental", 1: "layer incremental, head incremental", 
     2: "layer selective, head selective", 3: "layer incremental, head selective", 
     4: "layer incremental, single head", 5: "single layer, single head",
     6: "layer reverse incremental, single head", 7: "layer reverse incremental, head incremental"}
for TASK in ['MRPC', 'RTE', 'QNLI', 'SST-2']:
    for n in range(8):
        filename = f'acc{n}_{TASK}'

        x= list(range(12))
        y = np.zeros((12, len(x)))

        file = open(f'{filename}.csv')
        data_arr = np.loadtxt(file, delimiter=",")

        print("len:"+str(len(data_arr)))

        for i in range(len(data_arr)):
            y[int(data_arr[i][0])-1, x.index(int(data_arr[i][1]))] = data_arr[i][2]
        if n in [0, 1, 4, 5]:
            x2 = [str(x0) for x0 in x]
            for i in range(6):
                plt.plot(x2, y[i,:], label='layer'+str(i+1), linestyle="-")
            for i in range(6, 12):
                plt.plot(x2, y[i,:], label='layer'+str(i+1), linestyle=":")
        elif n in [2, 3]:
            z = np.zeros((12, 7))
            for i in range(12):
                for j in range(6):
                    z[i][j] = y[i][j*2]
                z[i][6] = y[i][11]
            x2 = list(map(str, range(7)))
            for i in range(6):
                plt.plot(x2, z[i,:], label='layer'+str(i+1), linestyle="-")
            for i in range(6, 12):
                plt.plot(x2, z[i,:], label='layer'+str(i+1), linestyle=":")
        elif n in [6, 7]:
            x2 = [str(x0) for x0 in x]
            for i in range(6):
                plt.plot(x2, y[i,:], label='layer'+str(12-i), linestyle="-")
            for i in range(6, 12):
                plt.plot(x2, y[i,:], label='layer'+str(12-i), linestyle=":")

        plt.xlabel(d[n])
        plt.legend()
        plt.savefig(f'{filename}.png', bbox_inches='tight')
        plt.cla()