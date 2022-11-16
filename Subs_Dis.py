import time
import math
from collections import deque, defaultdict
import matplotlib.pyplot as plt
from random import randint
import paho.mqtt.client as mqtt

msg_dis = 1.0
msg_condition = 1.0
msg_con = 1.0

def on_message(client, userdata, message):
    
    if (message.topic =="esp/hcsr04/distance"):
        global msg_dis
        msg_dis= float(message.payload.decode("utf-8"))
    if (message.topic =="esp/alarm"):
        global msg_con
        global msg_condition
        msg_condition= float(message.payload.decode("utf-8"))
    else :
        global msg_con
        global msg_condition
        msg_condition = 4.0
    

    

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
    plt.title('Distance Plot')
    data = myData();
    plotting = RealtimePlot(axes)
    client.publish("esp/alarm","4")  
    while True:            
        client.connect(broker)
        client.loop_start()
          
        client.subscribe("esp/hcsr04/distance")
        client.subscribe("esp/alarm")
        client.on_message = on_message
        msg_con = msg_condition
        data.add(count,msg_dis)
        plotting.plot(data)
        plt.pause(0.251)
        count+=1
        if  msg_dis <= 5.0 and msg_con != 0.0:
            client.publish("esp/alarm","3")
        elif msg_dis > 5.0 and msg_dis <= 20:            
            client.publish("esp/alarm","2")
            msg_con = 2.0
        elif msg_dis > 20.0 and msg_dis <= 40.0:            
            client.publish("esp/alarm","1")
            msg_con = 1.0
        elif msg_dis > 40.0:            
            client.publish("esp/alarm","4")
            msg_con = 4.0
       
        time.sleep(5)
        client.loop_stop()


if __name__ == "__main__" : main()