# statement_extraction

## About

Script for extracting thematic annotations on secondary literature texts from INCEpTION with the purpose of feeding them into MimoTextBase (https://data.mimotext.uni-trier.de/wiki/Main_Page).

Two variants:
* extract_annotations.py extracts all statements contained in the XMI files
* extract_filter_annotations.py filters statements according to the MiMoText domain and produces a second output file with the discarded statements


## Usage

### Prerequisites

The following packages need to be installed:
* dkpro-cassis
* pandas
* glob
* os
* re

Make sure that the input files are stored in a folder called "input" and create an empty folder "output".


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

Using the script extract_filter_annotations.py a second file "_drop" is created with the discarded statements.
