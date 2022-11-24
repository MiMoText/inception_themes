# themes_mapping

Script for mapping the IDs of the thematic concepts of the MiMoTextBase instance 11000 to the current instance (https://data.mimotext.uni-trier.de/wiki/Main_Page).

## Usage

### Prerequisites

The following packages need to be installed:
* pandas
* glob
* os
* re

Please store the input files in a folder called "input" and create an empty folder "output".


### Input

* Takes statements files in folder "input" and mapping file "themes_mapping_instances.tsv".

### Output

* In the folder "output" the statement files with the replaced IDs are stored.
