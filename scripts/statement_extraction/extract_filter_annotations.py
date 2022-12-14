'''
Script for extracting thematic annotations on secondary literature texts
from INCEpTION with the purpose of transferring them into statements
and feeding into MimoTextBase.
Input: XMI files (export from INCEpTION)
Output: two TSV files with statements: where ending "_drop" 
contains statements that don't belong to the MiMoText domain.
'''

# =======================
# Imports
# =======================
from cassis import *
import pandas as pd
import glob
import os
from os.path import join
import re

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

def get_sentences(cas):
    '''
    Saves sentence information including begin, end and text into a dataframe.
    '''
    rows = []
    counter = 0
    for sentence in cas.select('de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence'):
        #print(sentence.get_covered_text(), sentence.begin, sentence.end)
        rows.append({'id' : counter, 'begin' : sentence.begin, 'end' : sentence.end, 'text' : sentence.get_covered_text()})
        counter += 1 
    sentence_df = pd.DataFrame(rows)
    return sentence_df

def get_snippet(sentence_df, prop):
    '''
    Extracts the associated sentences to an annotated statement.
    '''
    annot_begin = min(prop.Governor.begin, prop.Dependent.begin)
    annot_end = max(prop.Governor.end, prop.Dependent.end)
    snippet = ""
    first_sentence = 0
    # get first sentence of annotation
    for ind in sentence_df.index:
        if annot_begin >= sentence_df['begin'][ind] and annot_begin <= sentence_df['end'][ind]:
            snippet = snippet + sentence_df['text'][ind]
            first_sentence = ind
            break
    
    # check for more sentences
    ind_sent = first_sentence + 1
    if not annot_end <= sentence_df['end'][first_sentence]:   # annotation covers only one sentence
        if annot_end <= sentence_df['end'][ind_sent]: # annotation covers two sentences
            snippet = snippet + " " + sentence_df['text'][ind_sent]
        else: # more than two sentences
            while annot_end > sentence_df['end'][ind_sent]:
                snippet = snippet + " " + sentence_df['text'][ind_sent]
                ind_sent += 1
            snippet = snippet + " " + sentence_df['text'][ind_sent + 1]
    
    snippet = re.sub('\r', '', snippet)
    snippet = re.sub('\n', ' ', snippet)
    return snippet
                
        
        
def extract_infos(cas, mapping_dict, sentence_df):
    '''
    Extracts statement informations from the cas object.
    Returns statements as dataframe.
    All statements whose subject was not assigned to a MiMoText ID 
    or where the object was not mapped to an ID are sorted out.
    '''
    rows_keep = []
    rows_drop = []
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
        text_snippet = get_snippet(sentence_df, prop)
        if subject_id == None or object_id == None:
            rows_drop.append({'subject_id' : subject_id, 'subject_snippet' : subject_snippet, 'property' : property, 'object_id' : object_id, 'object_label' : object_label, 'object_snippet' : object_snippet, 'snippet': text_snippet})
        elif subject_id.startswith('http://zora.uni-trier.de'):
            rows_keep.append({'subject_id' : subject_id, 'subject_snippet' : subject_snippet, 'property' : property, 'object_id' : object_id, 'object_label' : object_label, 'object_snippet' : object_snippet, 'snippet': text_snippet})
        else:
            rows_drop.append({'subject_id' : subject_id, 'subject_snippet' : subject_snippet, 'property' : property, 'object_id' : object_id, 'object_label' : object_label, 'object_snippet' : object_snippet, 'snippet': text_snippet})
    df_keep = pd.DataFrame(rows_keep)
    df_drop = pd.DataFrame(rows_drop)
    return df_keep, df_drop


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
        sentence_df = get_sentences(cas)
        df_keep, df_drop = extract_infos(cas, mapping_dict, sentence_df)
        df2tsv(df_keep, basename, output_folder)
        df2tsv(df_drop, basename + "_drop", output_folder)

main(theme_file, typesystem_file, input_folder, output_folder)