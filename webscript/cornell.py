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

#change the working directory
# os.chdir('/Users/linchenzhang/Desktop/nimark_RA/webscript_factiva/webscript/')
os.chdir(os.getcwd())
# os.chdir('Users\\linchenzhang\\Desktop\\nimark_RA\\webscript_factiva\\web_script\\reintroductionandrequest\\')
# os.chdir('C:\\Users\\messi\\Desktop\\RAnimark\\web_script\\reintroductionandrequest\\')
#start and end dates of the scrapesstart_date=168

start_date=40 # start in 1980 Q1 (for WSJ)
# start_date=41 # start in 1980 Q2 (for NYT)
#start_date=108 # start in 1997 Q1 (for USAT) (company information starts only in 1997)
#start_date=108 # start in 1997 Q1 (for atjc) (company information starts only in 1997)
#start_date=108 # start in 1997 Q1 (for bstngb) (company information starts only in 1997)
# start_date=108 # start in 1997 Q1 (for cgaz) (company information starts only in 1997)




#end_date=42
end_date=196 # end at 2018 Q4
#end_date=122 # end at 2018 Q4

df_all=pd.DataFrame(columns=['comp_name','comp_count','n_comp','n_articles','start_date','end_date'])

parse_excel = pd.ExcelFile("extracted_paragraph_n_grams_edited.xlsx")
parse_excel = parse_excel.parse("Sheet2")
industry_name = list(parse_excel['industry_name'])
print(industry_name)

category = list(parse_excel['category'])
print(category)
#%%############################################################################
# Define some basic functions
###############################################################################

def save_all_of_class(browser,classname):
    current_hits=browser.find_elements_by_class_name(classname)
    text_all=[]
    for temp in current_hits:
        text_temp=temp.text
        text_all.append(text_temp)
    return text_all

def parse_sector(source, sector_name):
    """
    parse a sector name to searhing terms we put in factiva
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

# print(parse_sector('nydf', 'auto'))


#%%############################################################################
# Load the sector definitions and prepare the serach term strings
###############################################################################

#(hd="auto industry" or hd=""auto sector")
#(hd="tech sector" or hd="technology sector" or hd="tech industry")

#search_term="(SC=J AND pg=A1)"
#search_term="(hd=industry or hd=sector) and (sales or quarter or fiscal) and (sc=j or sc=nytf or sc=wp or sc=bstngb or sc=usat or sc=phli)"
#search_term='(hd=industry or hd=sector) and ns=ccat and (sc=j or sc=nytf or sc=wp or sc=bstngb or sc=usat or sc=phli)'
#search_term='(hd="auto industry" or hd="auto sector") and ns=ccat and (sc=j or sc=nytf or sc=wp or sc=bstngb or sc=usat or sc=phli)'


#search_term='(the OR a OR an) and la=en and sc=j'
# search_term='(the OR a OR an) and la=en and sc=nytf'
#search_term='(the OR a OR an) and la=en and sc=usat'
#search_term='(the OR a OR an) and la=en and sc=atjc'
#search_term='(the OR a OR an) and la=en and sc=bstngb'
# search_term='(the OR a OR an) and la=en and sc=lvgs'
#search_term='(the OR a OR an) and la=en and sc=cgaz'
# search_term = 'sc=nytf and la=en and ((tech sector) or (tech industry) or (tech-sector) or (tech-industry) or (techmotive sector) or (automotive industry) or (automotive-sector) or (automotive-industry) or (car sector) or (car industry) or (car-sector) or (car-industry))'
# search_term = 'sc=nytf and la=en and ((auto sector) or (auto industry) or (auto-sector) or (auto-industry) or (automotive sector) or (automotive industry) or (automotive-sector) or (automotive-industry) or (car sector) or (car industry) or (car-sector) or (car-industry))'
# search_term = parse_sector('nytf', 'services')
search_term = parse_sector('j', 'services')
# search_term = parse_sector('j', 'tech')

#load strings used to define
f=open("years.txt", "r")
years = f.readlines()
years = [a.strip('\n') for a in years]
#load the months
f=open("months.txt", "r")
months = f.readlines()
months = [a.strip('\n') for a in months]
#load the months
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

#go to the uppsala library database website
url = 'https://newcatalog.library.cornell.edu/databases/subject/Economics'
# url='http://www.ub.uu.se/soktips-och-sokteknik/databaser-a-o/'
# browser=webdriver.Firefox(executable_path='/Users/linchenzhang/Desktop/nimark_RA/webscript_factiva/webscript/geckodriver')
browser=webdriver.Firefox(executable_path=os.getcwd()+'/geckodriver')
# browser=webdriver.Firefox(executable_path=r'C:\Users\messi\Desktop\RAnimark\web_script\reintroductionandrequest\geckodriver.exe')
#browser=webdriver.Edge()
browser.get(url)
time.sleep(1)

#click on the "I accept cookies button"
# ok_button_path="/html/body/div[2]/div/p/button"
# browser.find_element_by_xpath(ok_button_path).click()
# time.sleep(1)


# continue_link = driver.find_element_by_link_text('Continue')

#click the factiva link to get access via the uppsala licence
# factiva_path='//*[@id="F"]'
link=browser.find_element_by_link_text('Factiva')
link.click()
time.sleep(1)

#switch to popup and wait
# handle_new=browser.window_handles[1]
# browser.switch_to_window(handle_new)
# time.sleep(10)

for waiting in range(1,500):
    try:
        #change language to english
        button_settings=browser.find_element_by_xpath("/html/body/div[2]/div/ul[2]/li/a/span")
        button_settings.click()
        time.sleep(3)
        button_language=browser.find_element_by_xpath("/html/body/div[2]/div/ul[2]/li/div/ul/li[2]/a")
        button_language.click()
        time.sleep(3)
        button_english=browser.find_element_by_xpath("/html/body/div[2]/div/ul[2]/li/div/ul/li[2]/ul/li[1]/a")
        button_english.click()
        time.sleep(3)
        break
    except:
        time.sleep(1)
        print("waiting for search path")


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
# enter the region and other search options here (then run rest of code)
###############################################################################
# genius_bar = '/html/body/form[2]/div[2]/div[2]/div/table/tbody/tr[2]/td/div[1]/div[1]/table/tbody/tr/td[2]/div[2]/div[1]/span/div/div'
# genius_bar = '/html/body/form[2]/div[2]/div[2]/div/table/tbody/tr[2]/td/div[1]/div[1]/table/tbody/tr/td[2]/div[2]/div[1]/span/div/label[2]'
# genius_bar_button = browser.find_element_by_xpath(genius_bar)
# genius_bar_button.click()
# new_ftx = '/html/body/form[2]/div[2]/div[2]/div/table/tbody/tr[2]/td/div[1]/div[1]/table/tbody/tr/td[2]/div[2]/div[1]/span/div/div'
new_ftx = '/html/body/form[2]/div[2]/div[2]/div/table/tbody/tr[2]/td/div[1]/div[1]/table/tbody/tr/td[2]/div[2]/div[2]/div/div[1]/div[2]/div'
#identify the search field and enter the desired search text

search_field=browser.find_element_by_id('ftx')
search_field.click()
# search_field=browser.find_element_by_xpath(new_ftx)
search_definition=search_term
print(search_definition)
print(search_field)
# search_field.click()
search_field.send_keys(search_definition)

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
n_rep=len(last_days)
counter=start_date

#for rep in range(start_date,len(quarters)):
for rep in range(start_date,end_date):

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

        # try:
        #     print("start_date")
        #     print(start_dates)
        #     print(start_dates[rep])
        #     date1.clear()
        #     date1.click()
        #     date1.send_keys(start_dates[rep])
        #
        #     print("end_date")
        #     print(end_dates)
        #     print(end_dates[rep])
        #     date2.clear()
        #     date2.click()
        #     date2.send_keys(end_dates[rep])
        #
        #     search_field.clear()
        #     search_field.click()
        #     search_field.send_keys(search_definition)
        #     print('try2')
        #     break
        # except:
        #     time.sleep(1)
        #     print('wait2')
        #     print("waiting to enter dates and search term")

    #press the search button
    for waiting in range(1,50):
        try:
            submit=browser.find_element_by_xpath('/html/body/form[2]/div[2]/div[2]/div/div[2]/ul/li[2]/input')
            time.sleep(1)
            submit.click()
            print('try3')
            break
        except:
            time.sleep(1)
            print("waiting for the search button")

    #scrape the FIRST page of the main data
    for waiting in range(1,20):
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
                #count the number of companies shown
                company_names_all_path="/html/body/form[2]/div[2]/div[2]/div[5]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/ul"
                company_names_all=browser.find_element_by_xpath(company_names_all_path).text
                n_comp=len(re.split("\n",company_names_all))
                print("number of companies found: " + str(n_comp))
                if n_comp<100:
                    try:
                        browser.find_element_by_xpath(show_more_button).click()
                    except:
                        break
                if n_comp==100: break

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

    #go back to the search page
    df_all=df_all.append(df_current)
    # browser.get("https://global.factiva.com/sb/default.aspx")
    browser.get("https://global-factiva-com.proxy.library.cornell.edu/sb/default.aspx?NAPC=S")

###############################################################################
# Export the Results
###############################################################################

df_all['search_term']=search_term
# df_all.to_excel('company_scraper_nytf_from1980_temp.xlsx',index=False)
df_all.to_excel('wsj_services.xlsx',index=False)
