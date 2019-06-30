#%%############################################################################
# Runs a factiva search and saves the number of articles found as time series
###############################################################################

#import python libraries
import time
import os
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#change the working directory
os.chdir('C:\\Users\\messi\\Desktop\\RAnimark\\web_script\\reintroductionandrequest\\')

# os.chdir('C:\\Users\\stepi468\\Dropbox\\Studies\\Research\\CN Sectors and news focus\\news_data\\factiva_sector_scraper\\')
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

#%%############################################################################
# Load the sector definitions and prepare the serach term strings
###############################################################################

#load the scraped company names
#data=pd.read_excel("matched_names_edited_v2.xlsx")

#load the first round scraped factiva details and re-try subsamples
#data=pd.read_excel("data_master\\MASTER_scraped_company_details_ROUND_1_COMBINED.xlsx")
#no_results=data[data.scraped_name=="no results found"]
#error_message=data[data.scraped_name=="error message"]
#list_message=data[data.scraped_name=="list found"]
#unmatched=no_results.append(error_message)
#unmatched=list_message
#scraped_names=sorted(list(set(unmatched.name.tolist())))

#load the unmatched names only (second try, after adding further newspapers)
data_unmatched=pd.read_excel("data_master\\TEMP_company_counts_unmatched.xlsx")
names_scraped=data_unmatched.comp_name.tolist()

#OK=data.OK.tolist()
#dummy_nan=[1 if str(a)=="nan" else 0 for a in OK]
#data['dummy_nan']=dummy_nan
#unmatched=data[data.OK==1]
#unmatched=data[data.dummy_nan==1]
#scraped_names=sorted(list(set(unmatched.name.tolist())))

#go to the uppsala library database website
url='http://www.ub.uu.se/soktips-och-sokteknik/databaser-a-o/'
browser=webdriver.Firefox()
#browser=webdriver.Edge()
browser.get(url)
time.sleep(1)

#click on the "I accept cookies button"
ok_button_path="/html/body/div[2]/div/p/button"
browser.find_element_by_xpath(ok_button_path).click()
time.sleep(1)

#click the factiva link to get access via the uppsala licence
factiva_path='//*[@id="F"]'
link=browser.find_element_by_xpath(factiva_path)
link.click()
time.sleep(3)

#switch to popup and wait
handle_new=browser.window_handles[1]
browser.switch_to_window(handle_new)
time.sleep(10)

#switch to english
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

#navigate to company search
for waiting in range(1,500):
    try:
        #change language to english
        button_companies_markets=browser.find_element_by_xpath("/html/body/div[2]/div/ul[1]/li[6]/a")
        button_companies_markets.click()
        time.sleep(3)
        break
    except:
        time.sleep(1)
        print("waiting for search path")


#%%############################################################################
# enter the region and other search options here (then run rest of code)
###############################################################################

#load and count the scraped names to be explored
#scraped_names=['Snap Inc.','Microsoft Corporation','Pitschner']
n_rep=len(names_scraped)

#define the relevant xpaths and regular expressions
name_path="/html/body/form[2]/div[3]/div[1]/table/tbody/tr[2]/td[1]/h4"
exp_naics=re.compile(r"(<tr><td>NAICS<\/td><td align=.right.>)([0-9]*)(<\/td><td>)([A-Za-z,´`' \(\)]*)(<\/td><\/tr>)")
exp_dummy_US=re.compile(r'<p>(USA|United States|UNITED STATES)<\/p>')
exp_no_results=re.compile(r'((No results\.)(<\/div>)|No further information found for this company)')
exp_checkbox=re.compile(r'<td class="checkboxes"><input type="checkbox" name="ppc" value="0"><\/td>')
exp_footer=re.compile('<div class="provider">Powered by Factiva Companies and Executives<\/div>')
exp_error=re.compile('<td>We are unable to process your request at this time')
exp_general_information=re.compile('<h3>General Information<\/h3>')

#create an empty_dataframe for the results
data_all = pd.DataFrame(columns=('name','scraped_name','dummy_US','naics','naics_name'))

for count in range(3490,n_rep):
    a=names_scraped[count]

    #define the search field and send the current firm name
    if count==0: browser.get("https://global.factiva.com/cof/default.aspx")
    if count>0 and len(browser.find_elements_by_xpath('//*[@id="ct"]'))==0: browser.get("https://global.factiva.com/cof/default.aspx")
    scraped_name_current=a
    search_field=browser.find_element_by_xpath('//*[@id="ct"]')
    search_field.send_keys(scraped_name_current)
    time.sleep(1)
    search_field.send_keys(Keys.DOWN)
    time.sleep(1)
    search_field.send_keys(Keys.ENTER)
    dummy_results=[]

    #repeatedly get the source until at least one regex hit is satisfied
    for waiting in range(1,100):
        source=browser.page_source
        if re.search(exp_naics,source): print ("naics found"); dummy_results="yes"; break
        if re.search(exp_no_results,source): print ("no results found"); dummy_results="no"; break
        if re.search(exp_general_information,source) and not re.search(exp_naics,source): dummy_results="no"; break
        if re.search(exp_checkbox,source): print ("checkbox found"); dummy_results="checkbox"; break
        if re.search(exp_error,source): print ("error message found"); dummy_results="error"; break
        time.sleep(3)
        print("waiting for results page to load: " + a)

    if dummy_results=="error":
        naics_name_current="error message"
        naics_code_current="error message"
        name_current="error message"
        dummy_US="error message"
        time.sleep(2)
        browser.back


    if dummy_results=="yes":
        naics_temp=re.finditer(exp_naics,source)
        naics_temp=[a for a in naics_temp]
        naics_code_current=[a.group(2) for a in naics_temp]
        naics_name_current=[a.group(4) for a in naics_temp]
        naics_code_current=naics_code_current[0]
        naics_name_current=naics_name_current[0]
        name_current=browser.find_element_by_xpath(name_path).text
        if re.search(exp_dummy_US,source): dummy_US=1
        if not re.search(exp_dummy_US,source): dummy_US=0
        time.sleep(2)
        browser.back

    if dummy_results=="no":
        naics_name_current="no results found"
        naics_code_current="no results found"
        name_current="no results found"
        dummy_US="no results found"
        time.sleep(2)
        browser.back

    if dummy_results=="checkbox":
        naics_name_current="list found"
        naics_code_current="list found"
        name_current="list found"
        dummy_US="list found"
        time.sleep(2)
        browser.back

    #add variables to dataframe
    data_all.loc[count] = [a,name_current,dummy_US,naics_code_current,naics_name_current]
    print(str(count+1) + " of " + str(n_rep))
    time.sleep(3)

###############################################################################
# Export the Results
###############################################################################

data_all.to_excel('scraped_company_details_temp.xlsx',index=False)
