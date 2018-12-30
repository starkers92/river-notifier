from bs4 import BeautifulSoup

import matplotlib.pyplot as plt

import get_url




class River:
    def __init__(self,name,BOM_height_gauge_url,BOM_rain_gauge_url,BOM_rain_gauge_names):
        self.name=name
        self.height_gauge=BOM_height_gauge_url
        self.rain_gauge=BOM_rain_gauge_url
        self.rain_gauge_names = BOM_rain_gauge_names
        
        self.last_height=0
        self.plot=0
        self.time_list = []
        self.level_list = []
    
    def scrape_BOM_height_list(self):
        raw_html = get_url.simple_get(self.height_gauge)  #download river data
        
        html = BeautifulSoup(raw_html, 'html.parser') #parse using html parser

        raw_list=[] #search through html, all tabulated data is added to a list
        for p in html.select('td'):
            raw_list.append(p.text)
        self.level_list = raw_list[1::2] #data is in format time,level, so break it into two lists
        self.time_list = raw_list[0::2]

        #strip years from time data
        for i in range(0,len(self.time_list)):
            tmp_str = self.time_list[i]
            self.time_list[i] = tmp_str[0:5]+' '+tmp_str[-5:]

        self.level_list = [float(i) for i in self.level_list] #change from str to float

        self.last_level=self.level_list[-1] #grab the last river level for an output

    def scrape_BOM_rain_list(self):
        raw_html = get_url.simple_get(self.rain_gauge)

        html = BeautifulSoup(raw_html, 'html.parser') #parse using html parser
        #html.prettify()
        html.get_text()
        for string in html.stripped_strings:
            if string=='Paterson River':
                print(string)
            
       
        

        
    def plot_height_list(self):
        fig, ax = plt.subplots(1,1) #now plot the river level, getting a tick mark every three hours
        ax.plot(self.level_list)
        length = len(self.level_list)
        xtick_time=180 #every 3 hours
        xtime_interval=15 #fixme: assuming data comes every 15 minutes, #get this from the data
        no_of_ticks_per_hour = (xtime_interval/60)
        no_of_ticks = int(xtick_time*no_of_ticks_per_hour)
        x_list = []
        x_str_list = []
        for i in range(0,no_of_ticks):
            x_list.append(int(length*i/no_of_ticks))
            if (i%4)==0:
                x_str_list.append(self.level_list[int(length*i/no_of_ticks)])
            else:
                x_str_list.append('')

        ax.set_xticks(x_list)
        plt.grid()
        ax.set_xticklabels(x_str_list,rotation=45)
        plt.show()
        self.plot=[fig,ax]
    
allyn = River('Allyn','http://www.bom.gov.au/fwo/IDN60232/IDN60232.561019.tbl.shtml','http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html',['Mount Barrington','Careys Peak'])
allyn.scrape_BOM_height_list()
#allyn.plot_height_list()
allyn.scrape_BOM_rain_list()
