from tkinter import *
import time
from playsound import playsound
from tkinter import messagebox

alarm =Tk()
alarm.title("Alarm Clock")
alarm.geometry("738x383")
alarm.minsize(738,383)
alarm.maxsize(738,383)


alarmtime = StringVar()
msgi =StringVar()
Clockimg = PhotoImage(file="rs\\bg.png")
img = Label(alarm,image=Clockimg)
img.grid()  

title= PhotoImage(file="rs\\title.png")
head = Label(alarm,image=title)
head.place(x=235,y=5)

def ala():
    a= alarmtime.get()

    AlarmT = a
    CurrentTime = time.strftime("%H:%M")

    while AlarmT !=CurrentTime:
        CurrentTime = time.strftime("%H:%M")

        if AlarmT == CurrentTime:
            playsound('rs/tring.wav')
            msg = messagebox.showinfo('Info',f'{msgi.get()}')
            if msg=='ok':
                alarm.destroy()

inp= PhotoImage(file="rs\\input.png")
inputt = Label(alarm,image=inp)
inputt.place(x=70,y=100)

altime = Entry(alarm,textvariable=alarmtime,font=('comic sans',18),width=10)
altime.place(x=225,y=110)

ms= PhotoImage(file="rs\\ms.png")
msg = Label(alarm,image=ms,)
msg.place(x=70,y=160)

msginput = Entry(alarm,textvariable=msgi,font=('comic sans',18))
msginput.place(x=225,y=170)

set= PhotoImage(file="rs\\set.png")
submit = Button(alarm,image=set,command=ala)
submit.place(x=235,y=250)
alarm.mainloop()