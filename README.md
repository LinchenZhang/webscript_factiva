# Factiva Webscript Project

# Instructions:

1. Git clone this webscript_factiva repository.
2. Navigate to repository in command line/terminal and open the webscript sub-directory.
3. Install all necessary packages as per Requirement.md.
4. Call python cornell.py (factiva_scraper_uppsala_company_info_v3.py and factiva_scraper_uppsala_company_names_v4.py are preivous work of Stefan which I referred a lot in creating my own Cornell version of webscript in Factiva)
5. Relevant outputs (excel files) are also listed in the repository.

# Files:
* cornell.py: Cornell version python code of webscript in Factiva
* cornell_info.py: unfinished and not working imitation of factiva_scraper_uppsala_company_info_v3.py
* factiva_scraper_uppsala_company_names_v4.py: Uppsala version python code of webscript in Factiva
* factiva_scraper_uppsala_company_info_v3.py: Futher modification of webscript data got using Uppsala website
* extracted_paragraph_n_grams_edited.xlsx: source excel to match sector with category
* output excel files: The remaining excel files are all outputs

# NEW Script Outline (Using bitbucket API to get URLs)
1. Get list of URLs paired with last modified date
    1. Generate bitbucket client using user input username and password
    2. Get repository URLs from client
    3. Filter out URLs of repositories that have already been checked and haven't been updated since the last run of the script
2. Clone repos from URLs into a subdirectory
    1. pass on repo objects paired with last modified date
3. For each repo, parse its do and R files for rdrobust
    1. If rdrobust occurs at least once, record URL, number of rdrobust occurrences, and DOI if extractable
    2. Write outputs rdr_counts.csv and checked_URL.csv

# Notes:
If you want to clone all the repos disregarding the checked_URL information, please change df = pd.read_csv("checked_URL.csv") around line 35 in rdrsrch_fxn.py to df = pd.read_csv("checked_URL_empty.csv"), delete the repos directory in your working space, and then rerun the code.

# OLD Script Outline (Using Google Spreadsheet API to get DOIs)
1. Get DOIList as list of strings
    1. Change replication_list spreadsheet on google sheets to public
    2. Query the doi column and store as python list using google sheets API (based on code from [here](https://developers.google.com/sheets/api/quickstart/python))
2. Pull the git repos
    1. Read list object of DOI strings; for each clone the repo into a subdirectory using gitPython
    2. Record DOIs that fail to clone in a pd.Series
3. Parse the code, count occurrences of rdrobust by DOI
    1. Generate accumulator pd.Series
    2. For each DOI, count number of rdrobust occurrences in do and R files; if nonzero, add to accumulator
4. Print/return report
    1. Export list of DOIs containing rdrobust and the frequency of rdrobust in the DOI as rdr_counts.csv
    2. Export list of DOIs which fail to clone in badRepos.csv
