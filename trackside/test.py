from DLMSimulator import DLM
from utils import *
import matplotlib.pyplot as plt
import numpy as np
import time
import random


if __name__ == '__main__':

    data = np.empty((16,16))
    data[:,:] = np.nan
    ptlist = [(x,y,random.uniform(0,100)) for x in range(16) for y in range(16)]
    ptlist = np.array(ptlist)
    ptlist[233:][:,2] = 100
    data[ptlist[:,1].astype('int'), ptlist[:,0].astype('int')] = ptlist[:,2]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ion()
    im = ax.imshow(data)
    plt.show(block=False)
    fig.show()
    fig.canvas.draw()
    fig.suptitle('Sensor Values and Response', fontsize=20)
    plt.xlabel('', fontsize=18)
    plt.ylabel('', fontsize=16)
    plt.xticks([])
    plt.yticks([])

    d = DLM(errors=0)

    for i in range(100000):
        d.run()
        pkt = parse_packet(d.packet)
        for k,v in pkt.items():
            name = k
            resp = v
            break
        id_ = d.sensors_dict[name]['id']
        x = (id_-1)%16
        y = (id_-1)//16
        data[x][y] = resp

        time.sleep(0.2)
        im.set_array(data)
        fig.show()
        fig.canvas.draw()
        val = random.randint(0,10)
        plt.xlabel(f'hello hello hello hello \n hello hello hello \n hello hello hello ', fontsize=18)