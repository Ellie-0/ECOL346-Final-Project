#!/usr/bin/env python3
'''
Author: Maya Bose
Date: 2/10/2021
This program downloads the table of Fish species, genome accessions, and related 
information from FishDB
'''
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def main():
    i = 1
    all_rows = []
    while(True):
       
        # define URL
        url = "http://fishdb.ihb.ac.cn/genome?keywords=&page=" + str(i)
        # get request
        html_content = requests.get(url).text
        # Parse HTML
        soup = BeautifulSoup(html_content, "lxml")

        # Retrieve the datatable from the webpage
        gdp = soup.findAll("table", attrs={"class": "table table-hover"})
        fish_table = gdp[0] # There is only one table o

        # Parse the header row
        body = fish_table.findAll("tr")
        head = body[0] # 0th item is the header row
        head.append("GenBack Assembly Accession")
        
        body_rows = body[1:] # All other items becomes the rest of the rows
        if len(body_rows) == 0:
            break
        # Collect column names
        headings = []
        for item in head.find_all("th"): # loop through all th elements
            # convert the th elements to text and strip "\n"
            item = (item.text).strip("\n").lower()
            # append the clean column name to headings
            if (item == "name"):
                item = "species"
            headings.append(item)
        
        # Collect rows
        for row_num in range(len(body_rows)): # A row at a time
            row = [] 
            
            for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
                # Regex to remove flags OR newlines OR commas from entry
                entry = re.sub("(\xa0)|(\n)|,", "", row_item.text)
                #append entry to row - note one row entry is being appended
                row.append(entry.strip())
                # append one row to all_rows
            all_rows.append(row)

        i += 1
       
    df = pd.DataFrame(data = all_rows, columns = headings)
    df.to_csv("fishDB_genomes_summary.csv", index = False)

if __name__ == "__main__":    
    main()