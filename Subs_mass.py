import time
import math
from collections import deque, defaultdict
import matplotlib.pyplot as plt
from random import randint
import paho.mqtt.client as mqtt

msg_mass = 1.0

def on_message(client, userdata, message):
    print("massage receveid : ", str(message.payload.decode("utf-8")))    
    global msg_mass
    msg_mass= float(message.payload.decode("utf-8"))

class myData:
    def __init__(self,max_entries = 20):
        self.axis_x = deque(maxlen = max_entries)
        self.axis_y = deque(maxlen = max_entries)
        #self.axis_y2 = deque(maxlen = max_entries)

        self.max_entries = max_entries

        self.buf1 = deque(maxlen=5)
        #self.buf2 = deque(maxlen=5)

    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)
        #self.axis_y2.append(y2)


class RealtimePlot:
    def __init__(self, axes):
        self.axes = axes
        self.lineplot, = axes.plot([], [], "ro-")
        #self.lineplot2, = axes.plot([], [], "go-")

    def plot(self, dataPlot):
        self.lineplot.set_data(dataPlot.axis_x, dataPlot.axis_y)
        #self.lineplot2.set_data(dataPlot.axis_x, dataPlot.axis_y2)

        self.axes.set_xlim(min(dataPlot.axis_x),max(dataPlot.axis_x))

        ymin = min([min(dataPlot.axis_y)])-5
        ymax = max([max(dataPlot.axis_y)])+5

        self.axes.set_ylim(ymin,ymax)
        self.axes.relim()

def main():
    broker = "192.168.1.101"
    client = mqtt.Client("P1")
    count = 0;
    fig, axes = plt.subplots()
    plt.title('Mass Plot')
    data = myData();
    plotting = RealtimePlot(axes)
    while True:            
        client.connect(broker)
        client.loop_start()    
        client.subscribe("esp/pot/mass")
        client.on_message = on_message
        data.add(count,msg_mass)
        plotting.plot(data)
        plt.pause(0.251)
        count+=1
        
        client.loop_stop()

if __name__ == "__main__" : main()