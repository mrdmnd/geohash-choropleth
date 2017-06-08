import pandas as pd
import folium
import click
import os


__base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
__decodemap = { }
for i in range(len(__base32)):
    __decodemap[__base32[i]] = i

def decode_exactly(geohash):
    """
    Decode the geohash to its exact values, including the error
    margins of the result.  Returns four float values: latitude,
    longitude, the plus/minus error for latitude (as a positive
    number) and the plus/minus error for longitude (as a positive
    number).
    """
    lat_interval, lon_interval = (-90.0, 90.0), (-180.0, 180.0)
    lat_err, lon_err = 90.0, 180.0
    is_even = True
    for c in geohash:
        cd = __decodemap[c]
        for mask in [16, 8, 4, 2, 1]:
            if is_even: # adds longitude info
                lon_err /= 2
                if cd & mask:
                    lon_interval = ((lon_interval[0]+lon_interval[1])/2, lon_interval[1])
                else:
                    lon_interval = (lon_interval[0], (lon_interval[0]+lon_interval[1])/2)
            else:      # adds latitude info
                lat_err /= 2
                if cd & mask:
                    lat_interval = ((lat_interval[0]+lat_interval[1])/2, lat_interval[1])
                else:
                    lat_interval = (lat_interval[0], (lat_interval[0]+lat_interval[1])/2)
            is_even = not is_even
    lat = (lat_interval[0] + lat_interval[1]) / 2
    lon = (lon_interval[0] + lon_interval[1]) / 2
    return lat, lon, lat_err, lon_err

def generate_feature(geohash):
    """
    Turn a geohash into a geojson Feature object.
    """
    (lat, lon, lat_err, lon_err) = decode_exactly(geohash)
    lat_min = lat - lat_err
    lat_max = lat + lat_err
    lon_min = lon - lon_err
    lon_max = lon + lon_err
    a = "{1}, {0}".format(lat_min, lon_min)
    b = "{1}, {0}".format(lat_min, lon_max)
    c = "{1}, {0}".format(lat_max, lon_max)
    d = "{1}, {0}".format(lat_max, lon_min)

    return """\t{{
    \t\t"type": "Feature",
    \t\t"id": "{0}",
    \t\t"properties": {{ "name": "{0}" }},
    \t\t"geometry": {{ "type": "Polygon", "coordinates": [[ [{1}], [{2}], [{3}], [{4}], [{1}] ]] }}
\t}}""".format(geohash, a, b, c, d)

def construct_geojson(geohashes):

    """
    Turn a sequence of geohash tiles into a geojson FeatureCollection object.
    """
    return """{{
    "type": "FeatureCollection",
    "features": [
{0}
    ]
}}""".format( str(',\n'.join(map(generate_feature, geohashes))) )


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('output', default='./output', type=click.Path())
def main(input, output):

    if not os.path.exists(output):
        os.makedirs(output)

    # Load dataset in memory, then build a representation of the geojson features.
    df = pd.read_csv(input)
    geojson = construct_geojson(df['geohash'])

    # The choropleth method on the folium map requires a PATH, not an in-memory representation.
    # Write out in-memory representation to `$output_dir/geohashes.json`
    with open(os.path.join(output, 'geohashes.json'), 'w') as geojson_file:
        geojson_file.write(geojson)

    # For each metric column that isn't "geohash" in the input file,
    # Render a choropleth diagram for that metric.
    for column in df.columns.values.tolist():
        if column == "geohash":
            continue
        folium_map = folium.Map(
                location=decode_exactly(df['geohash'][0])[0:2],
                zoom_start=8,
                tiles='Stamen Terrain')
        folium_map.choropleth(
                geo_path=os.path.join(output, 'geohashes.json'),
                data=df,
                columns=['geohash', column],
                key_on='feature.id',
                fill_color='PuRd', fill_opacity=0.7, line_opacity=0.2,
                legend_name='Geohash Choropleth by {0}'.format(column.to_uppercase()))

        folium_map.save(os.path.join(output, '%s_map.html' % column))



if __name__ == "__main__":
    main()
