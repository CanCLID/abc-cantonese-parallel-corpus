# Cantonese-English Parallel Corpus (extracted from the ABC Dictionary)

This project is a Cantonese-English Parallel Corpus extracted from the ABC Cantonese-English Comprehensive Dictionary. It consists of around 14,000 sentences. The aim of this project is to provide high quality parallel data for developing Cantonese-English translation models, in order to facilitate the advancement of Cantonese NLP research.

## Data

The parallel datat can be found in `yue.txt` and `en.txt`.

## Build

1. Register an account on the [Wenlin Dictionaries Wiki](https://wenlin.co/);
1. Edit `scrape.py` to add your credentials on the Wenlin Dictionaries Wiki;
1. Run `scrape.py` to get a list of the titles of all pages under the `Jyut` category;
1. Go to the [export page](https://wenlin.co/wow/Special:Export) to export all the data to an XML file;
1. Run `extract.py` to build the corpus;
1. Manually validate the build results.

## Main difference from the original data

TODO
