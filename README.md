# Geohash Chloropleth
A python library for visualizing files of the form 

```geohash | metric1 | metric2 | ... | metricN```

as a collection of chloropleth maps, one per metric.

Super barebones and straightforward, most of the work is handled by the
dependencies.

## Installation
```$ pip install -r requirements.txt```

## Usage
```$ python geohash_chloropleth.py input_data.tsv output_map.html```
