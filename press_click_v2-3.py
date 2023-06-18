from pynput.mouse import Button, Controller
import numpy as np
import csv
import threading
import time
from socket import *
import numpy as np
import pyautogui
pyautogui.FAILSAFE = False

prev_sensor = np.zeros(8)
colors = ['b', 'r', 'y', 'g', 'c', 'k', 'm', '#e41a1c']
plot_num= 10 # plot されるセンサ値の数
plot_idx = 0
press_id=1 #圧力センサー
accel_x_id=2 #加速度計
accel_y_id=3 #加速度計
accum_x, accum_y=pyautogui.position()
log=[[accum_x,accum_y,0],]

mouse = Controller()

class ReceiveThread(threading.Thread):
    def __init__(self, PORT=12345):
        threading.Thread.__init__(self)
        self.data = 'hoge'
        self.kill_flag = False
        # line information
        self.HOST = "127.0.0.1"
        self.PORT = PORT
        self.BUFSIZE = 1024
        self.ADDR = (gethostbyname(self.HOST), self.PORT)
        # bind
        self.udpServSock = socket(AF_INET, SOCK_DGRAM)
        self.udpServSock.bind(self.ADDR)
        self.received = False

    def get_data(self):
        data_ary = []
        for i in reversed(range(8)):
            num = int(str(self.data[i*8:(i+1)*8]))
            data_ary.append(num / 167.0 / 10000)
        self.received = False
        return data_ary

    def run(self):
        while True:
            try:
                data, self.addr = self.udpServSock.recvfrom(self.BUFSIZE)
                self.data = data.decode()
                self.received = True
            except:
                pass

th= ReceiveThread()
th.setDaemon(True)
th.start()
loop_counter = 0
button_counter =0
diff_x = 0
diff_y = 0
while True:
  loop_counter+= 1
  print("loop",loop_counter,"px:",accum_x," py:",accum_y," dx:",diff_x," dy:",diff_y)
  if not th.data:
    break
  if th.received:
    sensor_data = th.get_data()
    diff_x = int(100*(sensor_data[accel_x_id-1]-2.4)**3)
    diff_y = int(-1*200*(sensor_data[accel_y_id-1]-2.4)**3)
    if diff_x*diff_x+diff_y*diff_y>5:

      accum_x=accum_x+diff_x
      accum_y=accum_y+diff_y
      if accum_x>800:
          accum_x = 800
      if accum_x<0:
          accum_x = 0
      if accum_y>480:
          accum_y = 480
      if accum_y<0:
          accum_y = 0
      #pyautogui.moveTo(accum_x,accum_y)
      mouse.position=[accum_x,accum_y]

    if sensor_data[press_id-1]>2.0 and button_counter > 7:
        break
    elif sensor_data[press_id-1]>0.1 and button_counter > 7:
      pyautogui.click()
      button_counter = 0
    else :
      button_counter += 1
    click=1 if button_counter==0 else 0
    log.append([diff_x,diff_y,click])

  time.sleep(0.05)
  
with open('./plot.csv','w') as f:
    writer=csv.writer(f)
    writer.writerows(log)
