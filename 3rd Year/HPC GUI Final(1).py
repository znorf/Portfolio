#HPC GUI

import numpy as np
from tkinter import *
from functools import partial

#Define functions used for buttons


def search(): #function searches for HPCs
    global HPCbox, drop, options, pos
    HPCwant=str(HPCbox.get())#gets seach query from input box
    
    #following lines search for query within HPC Data
    found=False
    pos=np.array([], dtype=int)#empty array to be filled in with positions of search results within HPCdata array
    options=[]#empty list to be filled in with details of search results
    for i in range(len(names)):
        if HPCwant.lower() in names[i].lower():
            found=True
            pos=np.append(pos, i)
    if found==False:
        options=["none found"]#user is informed if no results are found
    else:
        for i in range(len(pos)):
           op=str(i+1)+'; '+str(HPCdata[pos[i],1])+'; '+str(HPCdata[pos[i],3])+'; '+str(HPCdata[pos[i],4])
           options.append(op)#drop down tab filled with search results
    #drop down tab is destroyed and recreated
    drop.destroy()
    drop=OptionMenu(HPCWindow, menu, *options)
    drop.place(x=67,y=37)
    return

def calculate(): #function calculates CO2 Emissions
    global menu, pos, CPUbox, CIdata, HPCdata
    if menu.get()=="Search Results":
        string='Please select a HPC' #user is informed if they are yet to make a search query
    else:
        found=False
        i=0
        #loop finds position of selected HPC
        while found==False and i<len(menu.get()):
            if menu.get()[i]==';':
                found=True
                ch=int(menu.get()[0:i])-1
                ch=pos[ch]
            else:
                i+=1
        #search for carbon intensity for HPC country
        loc=0
        for i in range(len(CIdata)):
            if CIdata[i,0] in HPCdata[ch,4]:
                loc=i
                #if no country data available, continent data is searched for        
            if loc==0:
                for i in range(len(CIdata)):
                    if HPCdata[ch,10] in CIdata[i,0]:
                        loc=i
                        #if no country or continent data available, world value            
                    elif loc==0:
                        loc=len(CIdata)-1

        #calculates CO2 emissions in grams
        CO2Em=float(CIdata[loc,3])*float(HPCdata[ch,13])*int(CPUbox.get())
        CO2Em=str(round(CO2Em,1))
        #creates output tect
        string=HPCdata[ch,1]+', '+HPCdata[ch,4]+' uses '+str(round(float(HPCdata[ch,13]),4))+' kW per CPU/GPU'
        string=string+'\nOver '+str(CPUbox.get())+' kCPU/GPU hours, '+CO2Em+'kg of CO2 is released'+'\n(according to '+HPCdata[ch,5]+' data)'
    #places output text in text box
    results.delete(1.0, 'end')
    results.insert('1.0',string)
    return

#create window for calculator
HPCWindow = Tk()
HPCWindow.geometry('450x350')
HPCWindow.title('HPC Calculator')

#define necessary array sand lists for functions
options=[]
file = open('HPC_Power_Data.csv') #data taken from Our World in Data
HPCdata = np.genfromtxt('HPC_Power_Data.csv', delimiter=';', dtype=str)
file.close()
file = open('carbon-intensity-electricity_2022.csv')#data taken from Our World in Data
CIdata=np.genfromtxt('carbon-intensity-electricity_2022.csv', delimiter=',', dtype=str)
file.close()
names=HPCdata[:,1]
pos=np.array([], dtype=int)

#create HPC query box
HPClab=Label(HPCWindow, text="HPC Search")
HPClab.place(x=0,y=10)
HPCbox=Entry(HPCWindow)
HPCbox.place(x=110,y=10)

#create dropdown menu
menu=StringVar()
menu.set("Search Results")
drop=OptionMenu(HPCWindow, menu, "Search Results")
drop.place(x=67,y=37)
drop.config(width=14)

#create CPU hour input box
CPUlab=Label(HPCWindow, text="CPU/GPU Hrs (khrs)")
CPUlab.place(x=0,y=80)
CPUbox=Entry(HPCWindow)
CPUbox.place(x=110,y=80)

#create button to run each function
searchback=partial(search)
SearchButton=Button(HPCWindow,text="Search", command=searchback,width=5)
SearchButton.place(x=0,y=40)

callback=partial(calculate)
calcButton=Button(HPCWindow,text="Calculate", command=callback,width=7)
calcButton.place(x=0,y=120)

#create results box
results=Text(HPCWindow)
results.place(x=0,y=160)

#run loop
HPCWindow.mainloop()
