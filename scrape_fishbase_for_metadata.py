#!/usr/bin/env python3
'''
Author: Maya Bose
Date: 2/18/2021
This program retrieves average depth and ecosystem (saltwater vs freshwater) 
metadata from the Fishbase database usign its API for a list of fish species
'''

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re

def main():
    line_num = 0
    df = pd.DataFrame(columns = ['species', 'max depth', 'ecosystem'])
    with open("combined_fish_df.csv", "r") as in_file:
        
        for line in in_file:
            if line_num != 0:
                
                # Clean the name of the species (Some had artifacts)
                species = line.strip().strip("?")
                species = species.replace("?", " ")
                species = species.split(" ")
                if (len(species) > 2):
                    species = species[0:2]
                elif (len(species) < 2):
                    species.append("")
                species[0] = species[0].title()
                species[1] = species[1].lower()
                species = " ".join(species).strip().strip("*")
                
                
                # define URL for current species
                url = "https://www.fishbase.se/summary/" + \
                        species.replace(" ", "-") + ".html"
                # get request
                html_content = requests.get(url).text
                # Parse HTML
                soup = BeautifulSoup(html_content, "lxml")
                
                # Retrieve the datatable from the webpage
                gdp = soup.find_all("div", class_ = "smallSpace")
                # Check that the species has the info available
                try:
                    entry = str(gdp[1].find_all("span")[0])
                except:
                    continue
                    
                # clean the entry
                entry = entry.strip("</span>").strip()
                entry = re.sub("(\xa0)|(\n)|,", "", entry)
                entry = entry.split(";")
                entry = [el.strip() for el in entry]

                # define the environment of the fish species
                eco = np.nan
                if ("Freshwater" in entry and "Brackish" not in entry):
                    eco = "Freshwater"
                elif ("Marine" in entry):
                    eco = "Saltwater"

                # identify the minimum depth of the fish
                depth = id_min_depth(entry)
                
                # Add the entry to the datatable
                df = df.append({'species' : species, 'max depth' : depth,
                                'ecosystem' : eco}, ignore_index = True)
            else:
                line_num += 1
    # Write the final datatable
    df.to_csv("fish_with_metadata.csv", index = False, encoding="utf-8")

    
""" 
This function takes an information entry for a fish and returns the minimum 
depth that is reported for that fish. 
"""
def id_min_depth(info):
    # identify if the fish species has depth info available
    target_index = -1
    for i in range(len(info)):
        if ("depth range" in info[i]):
            target_index = i
            break
    # if the fish has depth info:
    if target_index != -1:
        
        # ID the depth range from the info string
        target = info[target_index]
        start = target.find("depth range")
        end = target.find("m", start + 11)
        depth_range = target[start + 11 : end].split("-")
        # identify the low and high end of the depth range based on where they 
        # SHOULD be in the info string. If the low end isn't there, return the 
        # high end. Otherwsie, print the string so I can look at it, and set the
        # depth range to NA
        low = depth_range[1].strip()
        high = depth_range[0].strip()
        if (is_int(low)):
            return int(low)
        elif (is_int(high)):
            return int(high)
        else:
            print(depth_range)
            return np.nan
        
    else:
        return np.nan
    
    
""" 
This function takes a variable, and returns whether or not that variable is an 
integer.
"""
def is_int(num):
    try: 
        int(num)
        return True
    except ValueError:
        return False

if __name__ == "__main__":    
    main()