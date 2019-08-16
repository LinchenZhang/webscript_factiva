#%%############################################################################
# Runs a factiva search and saves the number of articles found as time series
###############################################################################


#import python libraries
import time
import os
import pandas as pd
import re
from selenium import webdriver
import numpy as np


#%%############################################################################
# Define some basic functions
###############################################################################
def start_date_func(string):
    """
    returns start_date index given different newspaper inputs
    """
    if string == 'j':
        return 40
    elif string == 'nytf':
        return 41
    elif string == 'lvgs':
        return 80
    elif string == 'usat':
        return 68
    elif string == 'atjc' or string == 'bstngb' or string == 'cgaz':
        return 108
    else:
        raise 'Wrong String'


def end_date_func(string):
    """
    returns end_date index given different newspaper inputs
    """
    if string == 'lvgs':
        return 172
    else:
        return 196


def parse_sector(source, sector_name):
    """
    parse a sector name with certain source to searching terms we put in factiva

    e.g: parse_sector('nytf','auto') returns
    "sc=nytf and la=en and ((auto sector) or (auto industry) or (auto-sector) or
    (auto-industry) or (automotive sector) or (automotive industry) or
    (automotive-sector) or (automotive-industry) or (car sector) or
    (car industry) or (car-sector) or (car-industry))"

    """
    sub_industry = []
    sector_name = str(sector_name)
    string1 = 'sc='+str(source)+' and la=en and ('

    category_array = np.array(category)
    indexs = np.where(category_array == sector_name)
    sub_industry = list(np.array(industry_name)[indexs])

    string2 = ''
    print(sub_industry)
    for sub in sub_industry:
        string3 = '('+sub+' sector) or ('+sub+' industry) or ('+sub+'-sector) or ('+sub+'-industry)'
        string2 = string2 + string3
        if sub_industry[-1]==sub:
            string2 = string2+')'
        else:
            string2 = string2+' or '
    string = string1+string2
    return string

def parse_multi_sectors(source, list_sector_names):
    """
    parse a sector name with certain source to searching terms we put in factiva

    e.g: parse_sector('nytf',['auto','food']) returns
    "sc=nytf and la=en and ((auto sector) or (auto industry) or (auto-sector) or
    (auto-industry) or (automotive sector) or (automotive industry) or
    (automotive-sector) or (automotive-industry) or (car sector) or
    (car industry) or (car-sector) or (car-industry))"

    """
    sub_industry = []
    string1 = 'sc='+str(source)+' and la=en and ('

    category_array = np.array(category)
    indexs = np.where(category_array in list_sector_names)
    sub_industry = list(np.array(industry_name)[indexs])

    string2 = ''
    print(sub_industry)
    for sub in sub_industry:
        string3 = '('+sub+' sector) or ('+sub+' industry) or ('+sub+'-sector) or ('+sub+'-industry)'
        string2 = string2 + string3
        if sub_industry[-1]==sub:
            string2 = string2+')'
        else:
            string2 = string2+' or '
    string = string1+string2
    return string



def save_all_of_class(browser,classname):
    """
    same function used in Uppsala
    """
    current_hits=browser.find_elements_by_class_name(classname)
    text_all=[]
    for temp in current_hits:
        text_temp=temp.text
        text_all.append(text_temp)
    return text_all

#change to current working directory
os.chdir(os.getcwd())

#list of newspapers we want to search
datasets = ['usat']
# datasets = ['j']

#list of sectors we want to search
sectors = ['auto','tech','services','financial','commodities','communications','construction','energy','entertainment','food','gambling','healthcare','hospitatlity','housing','manufacturing','marijuana','tobacco','trade','transport','UNCLEAR','weapons']
# sectors = ['transport','marijuana','tobacco','trade','UNCLEAR','weapons']
# sectors = ['auto']

#%%############################################################################
# read and store sector and category information from excel file
###############################################################################
parse_excel = pd.ExcelFile("extracted_paragraph_n_grams_edited.xlsx")
parse_excel = parse_excel.parse("Sheet2")
industry_name = list(parse_excel['industry_name'])
print(industry_name)

category = list(parse_excel['category'])
print(category)



#load strings used to define
f=open("years.txt", "r")
years = f.readlines()
years = [a.strip('\n') for a in years]
#load the months
f=open("months.txt", "r")
months = f.readlines()
months = [a.strip('\n') for a in months]
#load the days
f=open("last_days.txt", "r")
last_days = f.readlines()
last_days = [a.strip('\n') for a in last_days]
#create the first days
first_days=[1 for a in last_days]

#date indexes at quarterly frequency
years_quarterly=years[0::3]
n_years=len(years)/4
quarters=[1,2,3,4]*48

#combined date strings for the factiva search
start_dates=[str(years[i])+str(months[i])+"01" for i in range(0,len(years))]
end_dates=[str(years[i])+str(months[i])+str(last_days[i]) for i in range(0,len(years))]

#keep only quarterly dates
start_dates=start_dates[0::3]
end_dates=end_dates[2::3]

#go to Cornell library database website
# url = 'https://newcatalog.library.cornell.edu/databases/subject/Economics'
url = "http://resolver.library.cornell.edu/misc/4394263"
# browser=webdriver.Firefox(executable_path='/Users/linchenzhang/Desktop/nimark_RA/webscript_factiva/webscript/geckodriver')
# browser=webdriver.Firefox(executable_path=os.getcwd()+'/geckodriver')
#here I use MAC version of geckodriver. For windows, change to next line and comment out previous line
browser=webdriver.Firefox(executable_path=os.getcwd()+'/geckodriver.exe')

browser.get(url)
time.sleep(1)

#click the factiva link to get access via the Cornell licence
# link=browser.find_element_by_link_text('Factiva')
# link.click()
# time.sleep(1)

#This is the changing language to English part. I comment it our because Cornell already uses English as default value.
# for waiting in range(1,500):
#     try:
#         #change language to english
#         button_settings=browser.find_element_by_xpath("/html/body/div[2]/div/ul[2]/li/a/span")
#         button_settings.click()
#         time.sleep(3)
#         button_language=browser.find_element_by_xpath("/html/body/div[2]/div/ul[2]/li/div/ul/li[2]/a")
#         button_language.click()
#         time.sleep(3)
#         button_english=browser.find_element_by_xpath("/html/body/div[2]/div/ul[2]/li/div/ul/li[2]/ul/li[1]/a")
#         button_english.click()
#         time.sleep(3)
#         break
#     except:
#         time.sleep(1)
#         print("waiting for search path")


#%%############################################################################
# Wait for the search page to load
###############################################################################


for waiting in range(1,500):
    try:
        search_path='/html/body/div[2]/div/ul[1]/li[2]/a'
        link2=browser.find_element_by_xpath(search_path)
        link2.click()
        time.sleep(0)
        print('try0')
        break
    except:
        time.sleep(1)
        print("waiting for search path")


#%%############################################################################
# the main for loop of newspapers and sectors
###############################################################################
for string in datasets:
    for sector in sectors:
        print("string="+string)
        print("sector="+sector)

        start_date = start_date_func(string)
        end_date = end_date_func(string)
        # end_date=196 # end at 2018 Q4
        search_term = parse_sector(string, sector)

        df_all=pd.DataFrame(columns=['comp_name','comp_count','n_comp','n_articles','start_date','end_date'])

        #%%############################################################################
        # enter the region and other search options here (then run rest of code)
        ###############################################################################

        #identify the search field and enter the desired search text

        search_field=browser.find_element_by_id('ftx')
        # search_field.click()

        search_definition=search_term
        # print(search_definition)
        # print(search_field)

        # search_field.send_keys(search_definition)

        #switch to date range entry mode and enter the desired date range
        date_field_path='/html/body/form[2]/div[2]/div[2]/div/table/tbody/tr[2]/td/div[1]/div[1]/table/tbody/tr/td[2]/div[3]/div[1]/table/tbody/tr/td[1]/select/option[10]'
        date_field=browser.find_element_by_xpath(date_field_path)
        date_field.click()

        #pre-define some data containers
        headlines_all=[]
        paragraphs_all=[]
        details_all=[]
        counts_all=[]
        headline_frames_all=[]
        article_frames_all=[]
        error_dates=[]

        #run the loop over the desired dates (this is the main scraping loop)

        for rep in range(start_date,end_date):
            # Check if the excel for certain combo of newspaper and sector already exist
            # If so, use the data in excel file.
            try:
                print("getdata")
                data = pd.ExcelFile(str(string)+'/'+str(string)+'-'+str(sector)+'.xlsx')
                df_all = data.parse("Sheet1")
                # print(list(df_all["start_date"]))
                m = max(list(df_all["start_date"]))
                print("m="+str(m))
                print("data_start_date="+str(start_dates[rep]))
                if int(start_dates[rep]) <= int(m):
                    print(str(start_dates[rep])+"is already done")
                    continue
            except:
                print("no excel file now")

            #find the date and search fields
            for waiting in range(1,500):
                try:

                    #switch to date range entry mode and enter the desired date range
                    date_field_path='/html/body/form[2]/div[2]/div[2]/div/table/tbody/tr[2]/td/div[1]/div[1]/table/tbody/tr/td[2]/div[3]/div[1]/table/tbody/tr/td[1]/select/option[10]'
                    date_field=browser.find_element_by_xpath(date_field_path)
                    date_field.click()
                    # date1=browser.find_element_by_xpath('//*[@id="frdt"]')
                    # date2=browser.find_element_by_xpath('//*[@id="todt"]')
                    day1=browser.find_element_by_xpath('//*[@id="frd"]')
                    day2=browser.find_element_by_xpath('//*[@id="tod"]')
                    month1=browser.find_element_by_xpath('//*[@id="frm"]')
                    month2=browser.find_element_by_xpath('//*[@id="tom"]')
                    year1=browser.find_element_by_xpath('//*[@id="fry"]')
                    year2=browser.find_element_by_xpath('//*[@id="toy"]')

                    search_field=browser.find_element_by_xpath('//*[@id="ftx"]')
                    print('try1')
                    break
                except:
                    time.sleep(1)
                    print('wait1')
                    print("waiting for date and search fields")

            #enter the dates
            for waiting in range(1,500):
                try:
                    start = start_dates[rep]
                    print ('start='+str(start))
                    y1 = start[:4]
                    m1 = start[4:6]
                    d1 = start[6:]
                    end = end_dates[rep]
                    y2 = end[:4]
                    m2 = end[4:6]
                    d2 = end[6:]

                    day1.clear()
                    day1.click()
                    day1.send_keys(d1)
                    day2.clear()
                    day2.click()
                    day2.send_keys(d2)

                    month1.clear()
                    month1.click()
                    month1.send_keys(m1)
                    month2.clear()
                    month2.click()
                    month2.send_keys(m2)

                    year1.clear()
                    year1.click()
                    year1.send_keys(y1)
                    year2.clear()
                    year2.click()
                    year2.send_keys(y2)

                    search_field.clear()
                    search_field.click()
                    search_field.send_keys(search_definition)
                    print('try2')
                    break

                except:
                    time.sleep(1)
                    print('wait2')
                    print("waiting to enter dates and search term")

            #press the search button
            for waiting in range(1,200):
                try:
                    submit=browser.find_element_by_xpath('/html/body/form[2]/div[2]/div[2]/div/div[2]/ul/li[2]/input')
                    time.sleep(2)
                    submit.click()
                    print('try3')
                    break
                except:
                    time.sleep(1)
                    print("waiting for the search button")

            number = 0
            #scrape the FIRST page of the main data
            end_number = 8
            for waiting in range(0,end_number):

                try:
                    headlines_current=save_all_of_class(browser,'enHeadline')
                    leadfields_current=save_all_of_class(browser,'leadFields')
                    paragraphs_current=save_all_of_class(browser,'ensnippet')
                    headlines_all.append(headlines_current)
                    details_all.append(leadfields_current)
                    paragraphs_all.append(paragraphs_current)
                    #hitsCount
                    count=browser.find_elements_by_class_name('hitsCount')[1].text
                    count=re.sub('[^0-9]',"",count)
                    counts_current=[count for a in headlines_current]
                    counts_all.append(counts_current)
                    #store the entire headline frame
                    headline_frames_all.append(browser.find_element_by_id('headlineFrame'))
                    article_frames_all.append(browser.find_element_by_id('articleFrame'))

                    #find the "more companies button" and click many times to make all 100 entries visible
                    show_more_button="/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/span[1]"

                    n_comp=0

                    for i in range(0,100):

                        print("company_clicks: " + str(i))

                        #count the number of companies shown

                        company_names_all_path="/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/ul"

                        company_names_all=browser.find_element_by_xpath(company_names_all_path).text

                        n_comp=len(re.split("\n",company_names_all))

                        print("number of companies found: " + str(n_comp))

                        if n_comp<100:

                            try:

                                browser.find_element_by_xpath(show_more_button).click()

                            except:

                                print("button for 'more companies' not found")

                        if n_comp==100: break

                        if n_comp<10 and i>9: break

                        if n_comp<20 and i>19: break

                        if n_comp<30 and i>29: break

                        if n_comp<40 and i>39: break

                        if n_comp<50 and i>49: break

                        if n_comp<60 and i>59: break

                        if n_comp<70 and i>69: break

                        if n_comp<80 and i>79: break

                        if n_comp<90 and i>89: break

                    # for i in range(0,100):
                    #     #count the number of companies shown
                    #     company_names_all_path="/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/ul"
                    #     company_names_all=browser.find_element_by_xpath(company_names_all_path).text
                    #     n_comp=len(re.split("\n",company_names_all))
                    #     print("number of companies found: " + str(n_comp))
                    #     if n_comp<100:
                    #         try:
                    #             browser.find_element_by_xpath(show_more_button).click()
                    #         except:
                    #             break
                    #     if n_comp==100: break

                    #construct list of the relevant xpaths for company names and corresponding article counts
                    comp_name_x_paths=["/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/ul/li[" + str(i) + "]/span[2]/span[1]" for i in range(1,n_comp+1)]
                    comp_count_x_paths=["/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/ul/li[" + str(i) + "]/span[2]/span[2]" for i in range(1,n_comp+1)]

                    #extract the actuall 100 company names and the corresponding counts
                    comp_names=[browser.find_element_by_xpath(comp_name_x_paths[i]).text for i in range(0,len(comp_name_x_paths))]
                    comp_counts=[browser.find_element_by_xpath(comp_count_x_paths[i]).text for i in range(0,len(comp_count_x_paths))]

                    #construct other variables to be saved
                    df_current=pd.DataFrame([comp_names,comp_counts]).T
                    df_current.columns=['comp_name','comp_count']
                    df_current['n_comp']=n_comp
                    df_current['n_articles']=count
                    df_current['start_date']=start_dates[rep]
                    df_current['end_date']=end_dates[rep]
                    break

                except:
                    time.sleep(1)
                    print("waiting for first page of results")
                    number += 1

            print("number:"+str(number))
            #True means all are exceptions. No result is found. Just go to next date.
            if number == end_number:
                browser.get("https://global-factiva-com.proxy.library.cornell.edu/sb/default.aspx?NAPC=S")
            #Else save the current info to excel file and go back to search page
            else:
                df_all=df_all.append(df_current)
                df_all['search_term']=search_term
                df_all.to_excel(str(string)+'/'+str(string)+'-'+str(sector)+'.xlsx',index=False)
                browser.get("https://global-factiva-com.proxy.library.cornell.edu/sb/default.aspx?NAPC=S")
            #go back to the search page


        ###############################################################################
        # Export the Results
        ###############################################################################

        df_all['search_term']=search_term
        df_all.to_excel(str(string)+'/'+str(string)+'-'+str(sector)+'.xlsx',index=False)
