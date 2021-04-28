#!/usr/bin/env python3
'''
Author: Maya Bose
Date: 2/18/2021
This program downloads the table of Fish species, genome accessions, and related 
information from a Paper supplement
'''

import pandas as pd
import tabula

def main():

    file = "https://science.sciencemag.org/content/sci/suppl/2019/05/08/364.6440.588.DC1/aav4632_Musilova_SM.pdf"
    table = tabula.read_pdf(file, pages =  "52-55", multiple_tables=False)[0]
    table.rename(columns = {'Species' : 'species' }, inplace = True)
    table.to_csv("Musilova_et_al_2019.csv", index = False, encoding="utf-8")

if __name__ == "__main__":    
    main()