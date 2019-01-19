from bs4 import BeautifulSoup

import matplotlib.pyplot as plt

import get_url



class Area:
    class Rain_Gauges:
        gauge_strings = []
        gauge_urls = []

    
    class River_Gauges:
        gauge_strings = []
        gauge_urls = []

def get_html(url):
    print('Getting URL...')
    try:
        raw_html = get_url.simple_get(url)
        print('Retrieved URL!')
    except:
        return
    return raw_html

def get_strings_from_html_tags(raw_html,tag):
    print('Returning all "<', tag, '>", from html data.')
    html = BeautifulSoup(raw_html, 'html.parser') #parse using html parser
    html.prettify()
    tag = str(tag)
    html.find_all(tag)
    raw_string = []
    for i in range(0,len(html.find_all(tag))):
        raw_string.append(html.find_all(tag)[i])
    return raw_string    

def remove_html_tags(raw_string,tag_list):
    print('Removing "', tag_list, '" from data.')
    import re
    clean_string = []
    for i in range(0,len(raw_string)):
        temp_str = str(raw_string[i])
        for j in range(0,len(tag_list)):
            temp_str = re.sub(str(tag_list[j]), '',temp_str)
        clean_string.append(temp_str)
    return clean_string    

#init class
allyn = Area()
#set river and rain gauge
allyn.River_Gauges.gauge_urls='http://www.bom.gov.au/fwo/IDN60232/IDN60232.561019.tbl.shtml'
allyn.Rain_Gauges.gauge_urls='http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html'

html_data = get_html(allyn.Rain_Gauges.gauge_urls)
raw_html_strings = get_strings_from_html_tags(html_data,'td')
tags_to_remove = ['<td align="left">','<td align="right">','</td>','<td>','\xa0','\n','<h4>','</h4>','<h3>','</h3>']
cleaned_html_strings = remove_html_tags(raw_html_strings,tags_to_remove)
