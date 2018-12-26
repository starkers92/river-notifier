from bs4 import BeautifulSoup

import matplotlib.pyplot as plt

import get_url




class River:
    def __init__(self,name,gauge,rain_gauge):
        self.name=name
        self.gauge=gauge
        self.rain_gauge=rain_gauge
        self.last_level=0
        self.plot=0
    
    def get_bom_river(self):
        raw_html = get_url.simple_get(self.gauge)  #download river data
        
        html = BeautifulSoup(raw_html, 'html.parser') #parse using html parser

        raw_list=[] #search through html, all tabulated data is added to a list
        for p in html.select('td'):
            raw_list.append(p.text)
        river_levels = raw_list[1::2] #data is in format time,level, so break it into two lists
        river_times = raw_list[0::2]

        #strip years from time data
        for i in range(0,len(river_times)):
            tmp_str = river_times[i]
            river_times[i] = tmp_str[0:5]+' '+tmp_str[-5:]

        river_levels = [float(i) for i in river_levels] #change from str to float

        fig, ax = plt.subplots(1,1) #now plot the river level, getting a tick mark every three hours
        ax.plot(river_levels)
        length = len(river_levels)
        xtick_time=180 #every 3 hours
        xtime_interval=15 #fixme: assuming data comes every 15 minutes, #get this from the data
        no_of_ticks_per_hour = (xtime_interval/60)
        no_of_ticks = int(xtick_time*no_of_ticks_per_hour)
        x_list = []
        x_str_list = []
        for i in range(0,no_of_ticks):
            x_list.append(int(length*i/no_of_ticks))
            if (i%4)==0:
                x_str_list.append(river_times[int(length*i/no_of_ticks)])
            else:
                x_str_list.append('')

        ax.set_xticks(x_list)
        plt.grid()
        ax.set_xticklabels(x_str_list,rotation=45)
        plt.show()
        self.plot=[fig,ax]

        self.last_level=river_levels[-1] #grab the last river level for an output

    
allyn = River('Allyn','http://www.bom.gov.au/fwo/IDN60232/IDN60232.561019.tbl.shtml',0)
allyn.get_bom_river()
