# Geohash Choropleth
A python library for visualizing data files of the form

`geohash | metric1 | metric2 | ... | metricN`

as a collection of HTML choropleth maps, one per metric column.

Super barebones and straightforward, most of the work is handled by the dependencies.

## Installation
    $ pip install -r requirements.txt

## Usage
    $ cat sample_input.csv
    geohash,foozles,wozzles
    9q8zj,100,0
    9q8zn,29,20
    9q8yv,101,30
    9q8yy,51,40
    9q8yt,85,50
    9q8yw,28,100
    $ python geohash_choropleth.py sample_input.csv
    $ cd output
    $ open foozles_map.html wozzles_map.html

[Example Choropleth](https://dl.dropbox.com/s/ngketn518fzz9sw/Screenshot%202017-06-08%2014.13.54.png?dl=0)

## Output
By default, this script outputs maps to an `output/` directory it creates in the working directory.
