'''
Script for mapping the IDs of the thematic concepts
of the MiMoTextBase instance 11000 to the current instance.
Takes statements files and mapping file.
Returns statement files with replaced IDs.
'''
# =======================
# Imports
# =======================
import pandas as pd
import glob
import os
from os.path import join
import re

# =======================
# Files and folders
# =======================

datadir = ""
input_folder = join("input", "*.tsv")
output_folder = join("output", "")
theme_file = join("themes_mapping_instances.tsv")


# =======================
# Functions
# =======================

def get_theme_mapping(theme_file):
    '''
    Takes file with old theme IDs and new MiMoTextBase IDs.
    Returns it as a dictionary.
    '''
    with open(theme_file, "r", encoding="utf8") as infile:
        mapping = pd.read_csv(infile, sep="\t")
        mapping_dict = {}
        for index, row in mapping.iterrows():
            mapping_dict[row['ID_alt']] = row['ID_neu']
        print(mapping_dict)    
        return mapping_dict
    

def replace_ID(file, mapping_dict):
    with open(file, "r", encoding="utf8") as infile:
        statements = pd.read_csv(infile, sep="\t")
        for index, row in statements.iterrows():
            try:
                statements.loc[index, 'object_id'] = mapping_dict[row['object_id']]
            except:
                pass
        return statements 
    
    
def df2tsv(df, basename, output_folder):
    filename = join(output_folder, basename + ".tsv") 
    with open(filename, "w", encoding="utf8") as outfile: 
        df.to_csv(outfile, sep="\t", line_terminator='\n')

    
    
def main(theme_file, input_folder, output_folder):
    mapping_dict = get_theme_mapping(theme_file)
    for file in glob.glob(input_folder):
        basename,ext = os.path.basename(file).split(".")
        print(basename)
        statements = replace_ID(file, mapping_dict)
        df2tsv(statements, basename, output_folder)

main(theme_file, input_folder, output_folder)