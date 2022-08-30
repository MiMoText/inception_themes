'''
Script for extracting thematic annotations on secondary literature texts
from INCEpTION with the purpose of transferring them into statements
and feeding into MimoTextBase.
'''

# =======================
# Imports
# =======================
from cassis import *
import pandas as pd
import glob
import os
from os.path import join

# =======================
# Files and folders
# =======================

datadir = ""
input_folder = join("input", "*.xmi")
output_folder = join("output", "")
typesystem_file = join("TypeSystem.xml")
theme_file = join("themes_wikibase.tsv")


# =======================
# Functions
# =======================

def get_theme_mapping(theme_file):
    '''
    Takes file with theme labels and MiMoTextBase IDs.
    Returns it as a dictionary.
    '''
    with open(theme_file, "r", encoding="utf8") as infile:
        mapping = pd.read_csv(infile, sep="\t")
        mapping_dict = {}
        for index, row in mapping.iterrows():
            mapping_dict[row['theme']] = row['themeLabel']
        return mapping_dict


def load_cas(typesystem_file, xmi_file):
    '''
    Loads Typesystem file and xmi_file.
    Returns it as a cas object.
    '''
    with open(typesystem_file, 'rb') as f:
        typesystem = load_typesystem(f)
    with open(xmi_file, 'rb') as f:
       cas = load_cas_from_xmi(f, typesystem=typesystem)
    return cas


def extract_infos(cas, mapping_dict):
    '''
    Extracts statement informations from the cas object.
    Returns statements as dataframe.
    '''
    rows = []
    for prop in cas.select('webanno.custom.Property'):    # runs over all statements (property elements in xmi)
        # extract governor information = subject
        subject_id =  prop.Governor.identifier
        subject_snippet = prop.Governor.get_covered_text()
        # get property ID
        property = prop.propertyID
        # extract dependent information = object
        object_id =  prop.Dependent.identifier
        try:
            object_label = mapping_dict[object_id]        # get French theme label
        except:
            object_label = None
        object_snippet = prop.Dependent.get_covered_text()
        
        rows.append({'subject_id' : subject_id, 'subject_snippet' : subject_snippet, 'property' : property, 'object_id' : object_id, 'object_label' : object_label, 'object_snippet' : object_snippet})
    
    df = pd.DataFrame(rows)
    return df


def df2tsv(df, basename, output_folder):
    '''
    Saves dataframe to tsv.
    '''
    filename = join(output_folder, basename + ".tsv") 
    with open(filename, "w", encoding="utf8") as outfile: 
        df.to_csv(outfile, sep="\t", line_terminator='\n')
        
        
def main(theme_file, typesystem_file, input_folder, output_folder):
    mapping_dict = get_theme_mapping(theme_file)
    
    for file in glob.glob(input_folder):
        basename,ext = os.path.basename(file).split(".")
        print(basename)
        cas = load_cas(typesystem_file, file)
        df = extract_infos(cas, mapping_dict)
        df2tsv(df, basename, output_folder)
    

main(theme_file, typesystem_file, input_folder, output_folder)