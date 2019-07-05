# Factiva Webscript Project

# Instructions:

1. Git clone this webscript_factiva repository.
2. Navigate to repository in command line/terminal and open the webscript sub-directory.
3. Install all necessary packages as per Requirement.md.
4. Call cornell.py.
5. Relevant outputs (excel files) are also listed in the repository.
6. To change searching sector or dataset, just change the line "search_term = parse_sector('D', 'S')", where D/S stands for new dataset/sector you are looking for. Note that the dataset is a Factiva encoded string. (E.g Wall Street Journal is 'j'). Also, change the saving excel file name in last line with your new dataset/sector.

# Files:
* cornell.py: Cornell version python code of webscript in Factiva
* cornell_info.py: unfinished and not working imitation of factiva_scraper_uppsala_company_info_v3.py
* factiva_scraper_uppsala_company_names_v4.py: Uppsala version python code of webscript in Factiva
* factiva_scraper_uppsala_company_info_v3.py: Futher modification of webscript data got using Uppsala website
* extracted_paragraph_n_grams_edited.xlsx: source excel to match sector with category
* years.txt: support file to call when seraching by date
* months.txt: support file to call when seraching by date
* last_days.txt: support file to call when seraching by date
* output excel files: The remaining excel files are all outputs. The name of an excel file is self-explanatory.

# Notes:
factiva_scraper_uppsala_company_info_v3.py and factiva_scraper_uppsala_company_names_v4.py are preivous work of Stefan in Uppsala University which I referred a lot in creating my own Cornell version of webscript in Factiva.
