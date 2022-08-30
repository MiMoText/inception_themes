# inception_themes

## About

This repository contains the scripts and files for extracting the thematic statements from the scholarly literature texts annotated in INCEpTION.

## Prerequisites

The following packages need to be installed:
* dkpro-cassis
* pandas
* glob
* os

## Usage

### Input

* The annotated texts are exported from INCEpTION in **UIMA CAS XMI (XML 1.0)** format and passed as input to the script.
* The script requires a **XML typesystem file** which is contained in the INCEpTION exports.
* The script uses a matching file (**themes_wikibase.tsv**) to get the french theme labels

### Output

After running the script the extracted information is stored in the output folder. For each input file a TSV statement file is created. Each row represents a statement and contains the following information:
* the statement subject (author or work): the annotated text snippet and the assigned ID
* the statement object (theme): the annotated text snippet and MiMoTextBase ID and French label of the assigned thematic concept
* the property
* the text snippet (one or more sentences containing the annotated strings)
