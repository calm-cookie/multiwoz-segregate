# MultiWOZ Segregator

The python script is used to segregate the [MultiWOZ_2.1](https://github.com/budzianowski/multiwoz/tree/master/data "Available here") dataset after incorporating corrections from [MultiWOZ_2.2](https://github.com/budzianowski/multiwoz/tree/master/data/MultiWOZ_2.2 "Available here").

Steps to incorporate **MultiWOZ_2.2** corrections into **MultiWOZ_2.1** dataset are available [here](https://github.com/budzianowski/multiwoz/tree/master/data/MultiWOZ_2.2#conversion-to-the-data-format-of-multiwoz-21).

It segregates the dataset into **attraction**, **restaurant**, **taxi** and combinations of these domains.

## Requirements
- `python 3.8.5` with `xlsxwriter 1.3.7`

## How to Run
Preliminary Steps
- Install **xlsxwriter** using  `pip3 install xlsxwriter==1.3.7`
- Go to `segregate.py` and set `OUTPUT_DIR` and `DATASET` paths in _line 20, 21_. By default, the directories are set to the current directory.

Final Step
- `python3 segregate.py`

## Output
- `JSON` files separated into different folders
- `stats.xlsx` with count of number of files
- `list.json` in each folder with list of filenames
