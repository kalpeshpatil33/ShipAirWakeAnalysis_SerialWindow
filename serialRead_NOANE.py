from serial import *
from Tkinter import *
import time
import sqlite3
import time 
import numpy as np
#import untitled0

#Serial connection
# /dev/cu.usbserial-A100P0K1
Base_serialPort = "/dev/cu.usbmodem1411"
Base_baudRate = 115200

Rover_serialPort = "/dev/cu.usbserial-A100P0K1"
Rover_baudRate = 115200

#make a TkInter Window
Base_root = Tk()
Base_root.wm_title("Reading Serial from Base")

Rover_root = Tk()
Rover_root.wm_title("Reading Serial from Rover")

Panel_root = Tk()
Panel_root.wm_title("Control Pannel")

# make a scrollbar
Base_scrollbar = Scrollbar(Base_root)
Base_scrollbar.pack(side=RIGHT, fill=Y)

Rover_scrollbar = Scrollbar(Rover_root)
Rover_scrollbar.pack(side=RIGHT, fill=Y)

# make a text box to put the serial output
Base_log = Text ( Base_root)
Base_log.pack()

Rover_log = Text ( Rover_root)
Rover_log.pack()

Panel_log = Text(Panel_root, width = 100, height = 6)
Panel_log.pack()

# attach text box to scrollbar
Base_log.config(yscrollcommand=Base_scrollbar.set)
Base_scrollbar.config(command=Base_log.yview)

Rover_log.config(yscrollcommand=Rover_scrollbar.set)
Rover_scrollbar.config(command=Rover_log.yview)

# attach button
Base_B = Button(Base_root, text ="QUIT",command = quit)
Base_B.pack()

Rover_B = Button(Rover_root, text ="QUIT",command = quit)
Rover_B.pack()

Panel_B = Button(Panel_root, text ="QUIT",command = quit)
#Panel_B.grid(row=2, column=3, columnspan=2)
Panel_B.pack()

Base_timestr = time.strftime("%Y%m%d-%H%M%S")
Base_file_name = "BASE: " + Base_timestr
Base_file_name_database = "BASE: " + Base_timestr + " database"
Base_text_file = open(Base_file_name, 'w')

Rover_timestr = time.strftime("%Y%m%d-%H%M%S")
Rover_file_name = "Rover: " + Rover_timestr
Rover_text_file = open(Rover_file_name, 'w')

Base_ser = Serial(Base_serialPort , Base_baudRate, timeout=0, writeTimeout=0) #ensure non-blocking
Panel_log.insert(INSERT,"Base connected to == ")
Panel_log.insert(END,Base_serialPort)

Rover_ser = Serial(Rover_serialPort , Rover_baudRate, timeout=0, writeTimeout=0) #ensure non-blocking
Panel_log.insert(INSERT,'\n')
Panel_log.insert(INSERT,"Rover connected to == ")
Panel_log.insert(END,Rover_serialPort)

time.sleep(5)

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute("drop table if exists imuBaseTable;")
c.execute("CREATE TABLE imuBaseTable(c1 TEXT, c2 TEXT,  c3 TEXT, c4 TEXT, c5 TEXT, c6 TEXT, c7 TEXT, c8 TEXT, c9 TEXT, c10 TEXT, c11 TEXT, c12 TEXT, c13 TEXT, c14 TEXT) ")

c.execute("drop table if exists gpggaBaseTable;")
c.execute("CREATE TABLE gpggaBaseTable(c1 TEXT, c2 TEXT,  c3 TEXT, c4 TEXT, c5 TEXT, c6 TEXT, c7 TEXT, c8 TEXT, c9 TEXT, c10 TEXT, c11 TEXT, c12 TEXT, c13 TEXT, c14 TEXT, c15 TEXT, c16 TEXT) ")

c.execute("drop table if exists gpvtgBaseTable;")
c.execute("CREATE TABLE gpvtgBaseTable(c1 TEXT, c2 TEXT,  c3 TEXT, c4 TEXT, c5 TEXT, c6 TEXT, c7 TEXT, c8 TEXT, c9 TEXT, c10 TEXT, c11 TEXT, c12 TEXT) ")

c.execute("drop table if exists imuRoverTable;")
c.execute("CREATE TABLE imuRoverTable(c1 TEXT, c2 TEXT,  c3 TEXT, c4 TEXT, c5 TEXT, c6 TEXT, c7 TEXT, c8 TEXT, c9 TEXT, c10 TEXT, c11 TEXT, c12 TEXT, c13 TEXT, c14 TEXT) ")

c.execute("drop table if exists gpggaRoverTable;")
c.execute("CREATE TABLE gpggaRoverTable(c1 TEXT, c2 TEXT,  c3 TEXT, c4 TEXT, c5 TEXT, c6 TEXT, c7 TEXT, c8 TEXT, c9 TEXT, c10 TEXT, c11 TEXT, c12 TEXT, c13 TEXT, c14 TEXT, c15 TEXT, c16 TEXT) ")

c.execute("drop table if exists gpvtgRoverTable;")
c.execute("CREATE TABLE gpvtgRoverTable(c1 TEXT, c2 TEXT,  c3 TEXT, c4 TEXT, c5 TEXT, c6 TEXT, c7 TEXT, c8 TEXT, c9 TEXT, c10 TEXT, c11 TEXT, c12 TEXT) ")


# window Position
def Panel_center_window(Panel_width=300, Panel_height=200):
    # get screen width and height
    Panel_screen_width = Panel_root.winfo_screenwidth()
    Panel_screen_height = Panel_root.winfo_screenheight()

    # calculate position x and y coordinates
    Panel_x = (Panel_screen_width/2) - (Panel_width/2) - 475
    Panel_y = (Panel_screen_height/2) - (Panel_height/2) - 475 
    Panel_root.geometry('%dx%d+%d+%d' % (Panel_width, Panel_height, Panel_x, Panel_y))
    
def Base_center_window(Base_width=300, Base_height=200):
    # get screen width and height
    Base_screen_width = Base_root.winfo_screenwidth()
    Base_screen_height = Base_root.winfo_screenheight()

    # calculate position x and y coordinates
    Base_x = (Base_screen_width/2) - (Base_width/2) - 350
    Base_y = (Base_screen_height/2) - (Base_height/2) 
    Base_root.geometry('%dx%d+%d+%d' % (Base_width, Base_height, Base_x, Base_y))

def Rover_center_window(Rover_width=300, Rover_height=200):
    # get screen width and height
    Rover_screen_width = Rover_root.winfo_screenwidth()
    Rover_screen_height = Rover_root.winfo_screenheight()

    # calculate position x and y coordinates
    Rover_x = (Rover_screen_width/2) - (Rover_width/2) + 325
    Rover_y = (Rover_screen_height/2) - (Rover_height/2) 
    Rover_root.geometry('%dx%d+%d+%d' % (Rover_width, Rover_height, Rover_x, Rover_y))

#make our own buffer
#useful for parsing commands
#Serial.readline seems unreliable at times too
Base_serBuffer = ""
Rover_serBuffer = ""

def logsBase(data):
    line = data.replace('\r\n', '')
    line = data.replace('\n', '')
    line = data.replace('*', ',')
    line = line.split(",")
#    print(len(line))
    
    if ("$GPGGA" in line and len(line) == 16 ):
        if "$GPGGA" in line[0]:
#            print((line))
            Panel_log.insert(INSERT,"GPGGA FIX ACQUIRED \n ")
            c.execute("Insert or Ignore into gpggaBaseTable Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", line)
            conn.commit()
        else:
            Panel_log.insert(INSERT,"GPGGA FIX MISSING \n ")
#            graph(float(line[2]),float(line[4]))
    if ("$GPVTG" in line and len(line) == 12):
        if "$GPVTG" in line[1]:
#            print((line))
            Panel_log.insert(INSERT,"GPVTG FIX ACQUIRED \n")
            c.execute("Insert or Ignore into gpvtgBaseTable Values(?,?,?,?,?,?,?,?,?,?,?,?)", line)
            conn.commit()
        else:
            Panel_log.insert(INSERT,"GPVTG FIX MISSING \n ")
    
    if ("$VNYIA" in line and len(line) == 14):
        if "$VNYIA" in line[3]:
#            print((line))
            Panel_log.insert(INSERT,"IMU FIX ACQUIRED \n")
            c.execute("Insert or Ignore into imuBaseTable Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", line)
            conn.commit()
        else:
            Panel_log.insert(INSERT,"IMU FIX MISSING \n ")

def logsRover(data):
    line = data.replace('\r\n', '')
    line = data.replace('\n', '')
    line = data.replace('*', ',')
    line = line.split(",")
    print(len(line))
    
    if ("$GPGGA" in line and len(line) == 16 ):
        if "$GPGGA" in line[0]:
#            print((line))
            Panel_log.insert(INSERT,"GPGGA FIX ACQUIRED \n ")
            c.execute("Insert or Ignore into gpggaRoverTable Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", line)
            conn.commit()
        else:
            Panel_log.insert(INSERT,"GPGGA FIX MISSING \n ")
#            graph(float(line[2]),float(line[4]))
    if ("$GPVTG" in line and len(line) == 12):
        if "$GPVTG" in line[1]:
#            print((line))
            Panel_log.insert(INSERT,"GPVTG FIX ACQUIRED \n")
            c.execute("Insert or Ignore into gpvtgRoverTable Values(?,?,?,?,?,?,?,?,?,?,?,?)", line)
            conn.commit()
        else:
            Panel_log.insert(INSERT,"GPVTG FIX MISSING \n ")
    
    if ("$VNYIA" in line and len(line) == 14):
        if "$VNYIA" in line[3]:
#            print((line))
            Panel_log.insert(INSERT,"IMU FIX ACQUIRED \n")
            c.execute("Insert or Ignore into imuRoverTable Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", line)
            conn.commit()
        else:
            Panel_log.insert(INSERT,"IMU FIX MISSING \n ")

def Base_readSerial():
    while True:
        Base_c = Base_ser.read() # attempt to read a character from Serial
        
        #was anything read?
        if len(Base_c) == 0:
            break
        
        # get the buffer from outside of this function
        global Base_serBuffer
        global Base_text_file
        
        # check if character is a delimeter
        if Base_c == '\r':
            Base_c = '' # don't want returns. chuck it
            
        if Base_c == '\n':
            Base_serBuffer += "\n" # add the newline to the buffer
            
            #add the line to the TOP of the log
            Base_log.insert('0.0', Base_serBuffer)
            logsBase(Base_serBuffer)
            Base_text_file.write(Base_serBuffer)
            Base_text_file.flush()
            Base_serBuffer = "" # empty the buffer
        else:
            Base_serBuffer += Base_c # add to the buffer
    
    Base_root.after(10, Base_readSerial) # check serial again soon

def Rover_readSerial():
    while True:
        Rover_c = Rover_ser.read() # attempt to read a character from Serial
        
        #was anything read?
        if len(Rover_c) == 0:
            break
        
        # get the buffer from outside of this function
        global Rover_serBuffer
        global Rover_text_file
        
        # check if character is a delimeter
        if Rover_c == '\r':
            Rover_c = '' # don't want returns. chuck it
            
        if Rover_c == '\n':
            Rover_serBuffer += "\n" # add the newline to the buffer
            
            #add the line to the TOP of the log
            Rover_log.insert('0.0', Rover_serBuffer)
            logsRover(Rover_serBuffer)
            Rover_text_file.write(Rover_serBuffer)
            Rover_text_file.flush()
            Rover_serBuffer = "" # empty the buffer
        else:
            Rover_serBuffer += Rover_c # add to the buffer
    
    Rover_root.after(10, Rover_readSerial) # check serial again soon

def quit():
   Rover_root.destroy()
   Rover_text_file.close()
   conn.close()
def quit():
   Base_root.destroy()
   Base_text_file.close()
   conn.close()

# after initializing serial, an arduino may need a bit of time to reset
Base_root.after(10, Base_readSerial)
Rover_root.after(10, Rover_readSerial)
Panel_root.after(100)

Base_center_window(650, 450)
Rover_center_window(650, 450)
Panel_center_window(325, 165)
Panel_root.mainloop()
Base_root.mainloop()
Rover_root.mainloop()
