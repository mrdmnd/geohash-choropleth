# Geohash Choropleth
A python library for visualizing data files of the form

`geohash | metric1 | metric2 | ... | metricN`

as a collection of HTML choropleth maps, one per metric column.

Super barebones and straightforward, most of the work is handled by the dependencies.

## Installation
    $ pip install -r requirements.txt

## Usage
    $ python geohash_choropleth.py input_data.csv

## Output
By default, this script outputs maps to an `output/` directory it creates in the working directory.
