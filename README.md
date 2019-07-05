# webscript_factiva

# Instructions:

1. Git clone the rdrobust_search2 repository
2. Navigate to repository in command line/terminal
3. Install all necessary packages as per Requirement.md
4. Call python rdrobust_search.py (we only check new repos modified/added since last updated checked time)
5. Relevant rdrobust occurence information is outputed as rdr_counts.csv, and updated time information of URLs is stored at checked_URL.csv

# Files:
* rdrsrch_fxns.py: a module containing the functions necessary to run rdrobust_search
* rdrobust_search.py: a script to output the report on rdrobust's frequency
* rdrsrch_test.py: test script for rdrsrch_fxns.py
* rdr_counts.csv: column A contains URLs of papers with code containing rdrobust, column B is number of appearance of rdrobust in the respective paper's code, column C is DOIs if extractable from the repo
* checked_URL.csv: column A contains URL of checked repo, column B contains date of repo's last update

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
