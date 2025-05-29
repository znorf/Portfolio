import numpy as np
from tkinter import *
from functools import partial


def config():#re-configures GUI for different number of flights
    global observatories, obs_button, results, calc_button
    
    #removes existing GUI components
    results.destroy()
    calc_button.destroy()
    for i in range(observatories):
        
        globals()['obs_label'+str(i+1)].destroy()
        globals()['obsname_box'+str(i+1)].destroy()
        globals()['obsname_label'+str(i+1)].destroy()
        globals()['hours_box'+str(i+1)].destroy()
        globals()['hours_label'+str(i+1)].destroy()
    
      
    #adds correct number of GUI components
    observatories=int(obs_box.get())
    for i in range(observatories):
    
        globals()['obs_label'+str(i+1)]=Label(obs_window, text="Observatory No "+str(i+1)+':')
        globals()['obs_label'+str(i+1)].place(x=10,y=10*(2+6*i)+60)
        globals()['obsname_box'+str(i+1)] = Entry(obs_window)
        globals()['obsname_box'+str(i+1)].place(x=120,y=10*(4+6*i)+60,width=130)
        globals()['obsname_label'+str(i+1)]=Label(obs_window, text="Observatory name:")
        globals()['obsname_label'+str(i+1)].place(x=10,y=10*(4+6*i)+60)
        globals()['hours_box'+str(i+1)] = Entry(obs_window)
        globals()['hours_box'+str(i+1)].place(x=350,y=10*(4+6*i)+60,width=130)
        globals()['hours_label'+str(i+1)]=Label(obs_window, text="Hours of use:")
        globals()['hours_label'+str(i+1)].place(x=270,y=10*(4+6*i)+60)

    results=Text(obs_window)
    results.place(x=0,y=10*(4+6*(observatories+1))+60)
    fill_back=partial(fill,observatories)
    calc_button=Button(obs_window,text="Calculate", command=fill_back,width=7)
    calc_button.place(x=211.5,y=10*(4+6*observatories)+60)
    return observatories

def identify_obs(obswant): #address given can be as accurate as user wants
    found=False
    pos=np.array([], dtype=int)
    #for loop f
    for i in range(len(names)):
        if obswant.lower() in names[i].lower():
            found=True
            pos=np.append(pos, i)
    if found==False:
        index=-1
    elif len(pos)==1:
        index=pos[0]
    else:
        index=-2
    return index

def fill(observatories):
    global Info, locations
    obsnames=np.empty([observatories], dtype=np.dtype('U100')) #empty array to be filled with flight departure and arrival locations
    Info=np.zeros([observatories,5]) #empty array to be filled with information, c1=column 1, c2=column 2 etc
    #c1=operating costs, c2=lifetime costs, c3=annual costs, c4=CO2 emissions, c5=contribution to lifetime
    
    
    string=''#empty string to be used as output

    for i in range(observatories):
        obsname_box=globals()['obsname_box'+str(i+1)]
        hours_box=globals()['hours_box'+str(i+1)]
        obsname=obsname_box.get()
        hours=hours_box.get()
        
        if identify_obs(obsname) == -1:
            string = string+'\nObservatory Number '+str(i+1)+': '+str(obsdata[identify_obs(obsname),0])+'\nWe do not have data on that observatory.'
        elif identify_obs(obsname) == -2:
            string = string+'\nObservatory Number '+str(i+1)+': '+str(obsdata[identify_obs(obsname),0])+'\nThere are multiple obsevatories with similar names.'
        else:
            obsnames[i]  = names[identify_obs(obsname)]
            Info[i,0],Info[i,1],Info[i,2] = obsdata[identify_obs(obsname),5], obsdata[identify_obs(obsname),6], obsdata[identify_obs(obsname),7]
            Info[i,3] = (float(hours)/(24*365))*Info[i,0]
            Info[i,4] = (float(hours)/(24*365))*Info[i,2]/Info[i,1]*100
            if Info[i,0] == 0:
                string = string+'\nObservatory Number '+str(i+1)+': '+str(obsdata[identify_obs(obsname),0])+'\nHours of use: '+str(hours)+'\nOperating emission = N/A\nContribution to observatory lifetime footprint = '+str(round(Info[i,4],5))+'%\n'
            else:
                string = string+'\nObservatory Number '+str(i+1)+': '+str(obsdata[identify_obs(obsname),0])+'\nHours of use: '+str(hours)+'\nOperating emission = '+str(round(Info[i,3]*1000,1))+'kg CO2e\nContribution to observatory lifetime footprint = '+str(round(Info[i,4],5))+'%\n'


    
    cFoot=sum(Info[:,3])
    string=string+'\n\nTotal Emissions: '+str(round(cFoot*1000,1))+'kg CO2e'
    results.delete(1.0, 'end')
    results.insert('1.0',string)
    return



file = open('Observatory database.txt') 
obsdata = np.genfromtxt('Observatory database.txt', delimiter=';', dtype=str)
file.close()
names=obsdata[:,0]
operation=obsdata[:,5]
lifetime=obsdata[:,6]
annual=obsdata[:,7]


observatories=1

#window setup
obs_window = Tk()
ob='450x'+str(300+observatories*100)
obs_window.geometry(ob)
obs_window.title('Observatory Emissions')

#flight number and GUI config button
con_back=partial(config)
obs_box=Entry(obs_window, width=4)        
obs_button=Button(obs_window,text="Enter",command=con_back, width=7)
obs_box.place(x=150,y=10)
obs_button.place(x=211.5,y=40)
obs_label=Label(obs_window, text='Number of Observatories:')
obs_label.place(x=10,y=10)



#initial GUI setup
for i in range(observatories):
    
    globals()['obs_label'+str(i+1)]=Label(obs_window, text="Observatory No "+str(i+1)+':')
    globals()['obs_label'+str(i+1)].place(x=10,y=10*(2+6*i)+60)
    globals()['obsname_box'+str(i+1)] = Entry(obs_window)
    globals()['obsname_box'+str(i+1)].place(x=120,y=10*(4+6*i)+60,width=130)
    globals()['obsname_label'+str(i+1)]=Label(obs_window, text="Observatory name:")
    globals()['obsname_label'+str(i+1)].place(x=10,y=10*(4+6*i)+60)
    globals()['hours_box'+str(i+1)] = Entry(obs_window)
    globals()['hours_box'+str(i+1)].place(x=350,y=10*(4+6*i)+60,width=130)
    globals()['hours_label'+str(i+1)]=Label(obs_window, text="Hours of use:")
    globals()['hours_label'+str(i+1)].place(x=270,y=10*(4+6*i)+60)

#results box and calculation button
results=Text(obs_window)
results.place(x=0,y=10*(4+6*(observatories+1))+60)
fill_back=partial(fill,obs_window)
calc_button=Button(obs_window,text="Calculate", command=fill_back,width=7)
calc_button.place(x=211.5,y=10*(4+6*observatories)+60)


#run loop
obs_window.mainloop()

#CPUhrs=float(input("\nPlease enter the amount of CPU hrs required for this project: "))

