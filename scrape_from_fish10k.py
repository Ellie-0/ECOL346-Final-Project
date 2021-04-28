#!/usr/bin/env python3
'''
Author: Maya Bose
Date: 2/18/2021
This program downloads the table of Fish species, genome accessions, and related 
information from Fish10K
'''
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


def progress_table(table_num):    
    
    # define URL
    url = "http://fish10k.genomics.cn/progress/" 
    # get request
    html_content = requests.get(url).text
    # Parse HTML
    soup = BeautifulSoup(html_content, "lxml")

    # Retrieve the datatable from the webpage
    gdp = soup.findAll("table", attrs={"class": "wp-block-table"})
    
    fish_table = gdp[table_num - 1]

    # Parse the header row
    body = fish_table.findAll("tr")
    head = body[0] # 0th item is the header row
    body_rows = body[1:] # All other items becomes the rest of the rows
    
    # Collect column names
    headings = []
    for item in head.find_all("td"): # loop through all td elements
        # convert the th elements to text and strip "\n"
        item = (item.text).strip("\n")
        # append the clean column name to headings
        headings.append(item.lower())

    # Collect rows
    all_rows = []
    for row_num in range(len(body_rows)): # A row at a time
        row = [] 
        for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
            # Regex to remove flags OR newlines OR commas from entry
            entry = re.sub("(\xa0)|(\n)|,", "", row_item.text)
            # append entry to row - note one row entry is being appended
            row.append(entry.strip())
            

        # append one row to all_rows
        all_rows.append(row)
    
    df = pd.DataFrame(data = all_rows, columns = headings)
    df.to_csv("fish10k_genomes_summary_" + str(table_num) + ".csv", index = False)

def species_table():
    # define URL
    url = "http://fish10k.genomics.cn/species/" 
    # get request
    html_content = requests.get(url).text
    # Parse HTML
    soup = BeautifulSoup(html_content, "lxml")

    # Retrieve the datatable from the webpage
    gdp = soup.findAll("table", attrs={"class": "display dataTable no-footer"})
    
    fish_table_1 = gdp[0]

    # Parse the header row
    body_1 = fish_table_1.findAll("tr")
    head = body_1[0] # 0th item is the header row
    
    # Collect column names
    headings = []
    for item in head.find_all("th"): # loop through all td elements
        # convert the th elements to text and strip "\n"
        item = (item.text).strip("\n")
        # append the clean column name to headings
        headings.append(item.lower())


    fish_table_2 = gdp[1]

    # Parse the header row
    body_2 = fish_table_2.findAll("tr")
    
    # Collect rows
    all_rows = []
    # all_rows.append(headings)
    for row_num in range(len(body_2)): # A row at a time
        row = [] 
        for row_item in body_2[row_num].find_all("td"): #loop through all row entries
            # Regex to remove flags OR newlines OR commas from entry
            entry = re.sub("(\xa0)|(\n)|,", "", row_item.text)
            # append entry to row - note one row entry is being appended
            row.append(entry.strip())
        # append one row to all_rows
        all_rows.append(row)

    df = pd.DataFrame(data = all_rows, columns = headings)
    df.to_csv("fish10k_genomes_summary_species_page.csv", index = False, encoding="utf-8")

def main():
    progress_table(1)
    progress_table(2)
    species_table()


if __name__ == "__main__":    
    main()