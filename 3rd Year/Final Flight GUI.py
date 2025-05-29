from geopy.geocoders import Nominatim #module needs to be installed using pip
import numpy as np
from geopy.distance import great_circle
from tkinter import *
from functools import partial

#functions defined for buttons

def config():#re-configures GUI for different number of flights
    global flights, flight_button, results, calc_button
    
    #removes existing GUI components
    results.destroy()
    calc_button.destroy()
    for i in range(flights):
        
        globals()['flight_label'+str(i+1)].destroy()
        globals()['dep_box'+str(i+1)].destroy()
        globals()['dep_label'+str(i+1)].destroy()
        globals()['des_box'+str(i+1)].destroy()
        globals()['des_label'+str(i+1)].destroy()
    
      
    #adds correct number of GUI components
    flights=int(flight_box.get())
    for i in range(flights):
    
        globals()['flight_label'+str(i+1)]=Label(flight_window, text="Flight No "+str(i+1)+':')
        globals()['flight_label'+str(i+1)].place(x=10,y=10*(2+6*i)+60)
        globals()['dep_box'+str(i+1)] = Entry(flight_window)
        globals()['dep_box'+str(i+1)].place(x=90,y=10*(4+6*i)+60,width=130)
        globals()['dep_label'+str(i+1)]=Label(flight_window, text="Departure:")
        globals()['dep_label'+str(i+1)].place(x=30,y=10*(4+6*i)+60)
        globals()['des_box'+str(i+1)] = Entry(flight_window)
        globals()['des_box'+str(i+1)].place(x=300,y=10*(4+6*i)+60,width=130)
        globals()['des_label'+str(i+1)]=Label(flight_window, text="Desination:")
        globals()['des_label'+str(i+1)].place(x=230,y=10*(4+6*i)+60)

    results=Text(flight_window)
    results.place(x=0,y=10*(4+6*(flights+1))+60)
    fill_back=partial(fill,flights)
    calc_button=Button(flight_window,text="Calculate", command=fill_back,width=7)
    calc_button.place(x=211.5,y=10*(4+6*flights)+60)
    return flights

def get_lat_long(addr): #address given can be as accurate as user wants
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(addr)
    lat,long=getLoc.latitude,getLoc.longitude #find coordinates
    addr1=getLoc.address #add1 is address of coords rather than input address
    return addr1, lat, long

def fill(flights):
    global dInfo, locations
    LHDis=1600#km minumum distance for a flight to be considered a long-haul flight (according to civil aviation authority)
    short_em=151#g emissions per km per passenger for a short-haul flight
    long_em=148#g emissions per km per passenger for a long-haul flight
    locations=np.empty([flights,2,], dtype=np.dtype('U100')) #empty array to be filled with flight departure and arrival locations
    dInfo=np.zeros([flights,6]) #empty array to be filled with distance information, c1=column 1, c2=column 2 etc
    #c1=derpature lat, c2=departure long, c3=arrival lat, c4=arrival long
    #c5=distance(km), c6=CO2 emissions(g)
    
    
    string=''#empty string to be used as output

    for i in range(flights):
        dep_box=globals()['dep_box'+str(i+1)]
        des_box=globals()['des_box'+str(i+1)]
        dep=dep_box.get()
        des=des_box.get()
    
        locations[i,0], dInfo[i,0],dInfo[i,1]=get_lat_long(dep)[0],get_lat_long(dep)[1],get_lat_long(dep)[2]
        locations[i,1], dInfo[i,2],dInfo[i,3]=get_lat_long(des)[0],get_lat_long(des)[1],get_lat_long(des)[2]
        #fills empty arrays with data
        coords0=(dInfo[i,0],dInfo[i,1])
        coords1=(dInfo[i,2],dInfo[i,3])
        dInfo[i,4]=great_circle(coords0, coords1).km #calculates distance using great circle, earth radius=6371.009km
    
        if dInfo[i,4]<LHDis:
            dInfo[i,5]=dInfo[i,4]*short_em
        else:
            dInfo[i,5]=dInfo[i,4]*long_em
            #if statement checks whether distance is a long haul flight or short haul then calculated respective carbon emission
        string=string+'\nFlight Number '+str(i+1)+':\n'+str(locations[i,0])+'\nto\n'+str(locations[i,1]+'\nCO2 emissions: '+str(round(dInfo[i,5]/1000,1)))+'kg\n'
    cFoot_max=np.unravel_index(dInfo[:,5].argmax(), dInfo[:,5].shape)[0]
    emiss_max=round(dInfo[cFoot_max,5],1)
    cFoot=sum(dInfo[:,5])
    string=string+'\n\nTotal Emissions: '+str(round(cFoot/1000,1))+'kg\nLargest Contribution: Flight Number '+str(cFoot_max+1)+', '+str(round(emiss_max/1000,1))+'kg ('+str(round(emiss_max/round(cFoot,1)*100,1))+'%)'
    results.delete(1.0, 'end')
    results.insert('1.0',string)
    return
    

flights=1

#window setup
flight_window = Tk()
geo='450x'+str(300+flights*100)
flight_window.geometry(geo)
flight_window.title('Flight Emissions')

#flight number and GUI config button
con_back=partial(config)
flight_box=Entry(flight_window, width=4)        
flight_button=Button(flight_window,text="Enter",command=con_back, width=7)
flight_box.place(x=115,y=10)
flight_button.place(x=211.5,y=40)
flight_label=Label(flight_window, text='Number of Flights:')
flight_label.place(x=10,y=10)



#initial GUI setup
for i in range(flights):
    
    globals()['flight_label'+str(i+1)]=Label(flight_window, text="Flight No "+str(i+1)+':')
    globals()['flight_label'+str(i+1)].place(x=10,y=10*(2+6*i)+60)
    globals()['dep_box'+str(i+1)] = Entry(flight_window)
    globals()['dep_box'+str(i+1)].place(x=90,y=10*(4+6*i)+60,width=130)
    globals()['dep_label'+str(i+1)]=Label(flight_window, text="Departure:")
    globals()['dep_label'+str(i+1)].place(x=30,y=10*(4+6*i)+60)
    globals()['des_box'+str(i+1)] = Entry(flight_window)
    globals()['des_box'+str(i+1)].place(x=300,y=10*(4+6*i)+60,width=130)
    globals()['des_label'+str(i+1)]=Label(flight_window, text="Desination:")
    globals()['des_label'+str(i+1)].place(x=230,y=10*(4+6*i)+60)

#results box and calculation button
results=Text(flight_window)
results.place(x=0,y=10*(4+6*(flights+1))+60)
fill_back=partial(fill,flight_window)
calc_button=Button(flight_window,text="Calculate", command=fill_back,width=7)
calc_button.place(x=211.5,y=10*(4+6*flights)+60)


#run loop
flight_window.mainloop()
