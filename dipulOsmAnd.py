import math
import pyproj
import urllib.request
import glob
from PIL import Image
import os
import shutil

urlpart = "https://uas-betrieb.de/geoservices/dipul/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&LAYERS=dipul%3Aflugplaetze%2Cdipul%3Aflughaefen%2Cdipul%3Akontrollzonen%2Cdipul%3Aflugbeschraenkungsgebiete%2Cdipul%3Abundesstrassen%2Cdipul%3Abundesautobahnen%2Cdipul%3Abahnanlagen%2Cdipul%3Abinnenwasserstrassen%2Cdipul%3Aseewasserstrassen%2Cdipul%3Aschifffahrtsanlagen%2Cdipul%3Awohngrundstuecke%2Cdipul%3Afreibaeder%2Cdipul%3Aindustrieanlagen%2Cdipul%3Akraftwerke%2Cdipul%3Aumspannwerke%2Cdipul%3Astromleitungen%2Cdipul%3Awindkraftanlagen%2Cdipul%3Ajustizvollzugsanstalten%2Cdipul%3Amilitaerische_anlagen%2Cdipul%3Alabore%2Cdipul%3Abehoerden%2Cdipul%3Adiplomatische_vertretungen%2Cdipul%3Ainternationale_organisationen%2Cdipul%3Apolizei%2Cdipul%3Asicherheitsbehoerden%2Cdipul%3Akrankenhaeuser%2Cdipul%3Anationalparks%2Cdipul%3Anaturschutzgebiete%2Cdipul%3Avogelschutzgebiete%2Cdipul%3Affh-gebiete&TILED=false&WIDTH=512&HEIGHT=512&CRS=EPSG%3A3857&STYLES=&BBOX="

class Tile:
    def __init__(self, zoom, x, y):
        self.zoom = zoom
        self.x = x
        self.y = y
        self.url = get_url_for_tile(zoom, x, y)
        self.filename = "dipul/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".png.tile"

def num2deg(zoom, xtile, ytile):
  n = 1 << zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return lat_deg, lon_deg

def get_url_for_tile(zoom, xtile, ytile):
  lat_min, lon_min = num2deg(int(zoom), int(xtile), int(ytile))
  lat_max, lon_max = num2deg(int(zoom), int(xtile) + 1, int(ytile) + 1)
  # print(lat_min, lat_max, lon_min, lon_max)

  # Need EPSG 3857 coordinates for bbox parameter, so convert lat, lon to x, y
  wgs84 = pyproj.CRS('EPSG:4326')
  web_mercator = pyproj.CRS('EPSG:3857')
  transformer = pyproj.Transformer.from_crs(wgs84, web_mercator, always_xy=True)
  min_x, max_y = transformer.transform(lon_min, lat_min)
  max_x, min_y = transformer.transform(lon_max, lat_max)
  bbox = str(min_x) + "%2C" + str(min_y) + "%2C" + str(max_x) + "%2C" + str(max_y)
  # print(bbox)
  # print(urlpart + bbox)
  return urlpart + bbox

def lon2tile(lon, zoom):
    return int((lon + 180) / 360 * 2**zoom)

def lat2tile(lat, zoom):
    rad_lat = math.radians(lat)
    return int((1 - math.log(math.tan(rad_lat) + 1 / math.cos(rad_lat)) / math.pi) / 2 * 2**zoom)

def calculate_tiles(min_lat, max_lat, min_lon, max_lon, zoom):
    # Calculate the tile coordinates for the corners of the bounding box
    min_x = lon2tile(min_lon, zoom)
    max_x = lon2tile(max_lon, zoom)
    min_y = lat2tile(max_lat, zoom)  # Note that we use max_lat for min_y and vice versa
    max_y = lat2tile(min_lat, zoom)  # Note that we use min_lat for max_y and vice versa

    # Create a list to store the tile names
    tiles = []

    # Iterate through each tile and calculate its name
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            tile = Tile(zoom, x, y)
            tiles.append(tile)

    return tiles

class Bundesland:
    def __init__(self, name, min_lat, max_lat, min_lon, max_lon):
        self.name = name
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon

baden_wuerttemberg = Bundesland("Baden-Württemberg", 47.5557, 49.7864, 7.4894, 10.4912)
bavaria = Bundesland("Bavaria (Bayern)", 47.2701, 50.5666, 8.2339, 13.8342)
berlin = Bundesland("Berlin", 52.3382, 52.6755, 13.0886, 13.7612)
brandenburg = Bundesland("Brandenburg", 51.3575, 53.5537, 11.2683, 14.7677)
bremen = Bundesland("Bremen", 53.0151, 53.3811, 8.4691, 8.9914)
hamburg = Bundesland("Hamburg", 53.3947, 53.7232, 9.7091, 10.3252)
hessen = Bundesland("Hesse (Hessen)", 49.3961, 51.6671, 7.8785, 10.2363)
lower_saxony = Bundesland("Lower Saxony (Niedersachsen)", 51.3141, 53.9106, 6.8583, 11.5949)
mecklenburg_vorpommern = Bundesland("Mecklenburg-Vorpommern", 53.2738, 54.4372, 11.0175, 14.2646)
north_rhine_westphalia = Bundesland("North Rhine-Westphalia (Nordrhein-Westfalen)", 50.3211, 52.5295, 5.8664, 9.6014)
rheinland_pfalz = Bundesland("Rhineland-Palatinate (Rheinland-Pfalz)", 48.9885, 50.9189, 6.1434, 8.4467)
saarland = Bundesland("Saarland", 49.1903, 49.6227, 6.3794, 7.2178)
sachsen = Bundesland("Saxony (Sachsen)", 50.8575, 51.6723, 11.6368, 15.043)
sachsen_anhalt = Bundesland("Saxony-Anhalt (Sachsen-Anhalt)", 51.3458, 52.1986, 11.5874, 12.2808)
schleswig_holstein = Bundesland("Schleswig-Holstein", 53.3403, 54.926, 8.3756, 11.3004)
thueringen = Bundesland("Thuringia (Thüringen)", 50.2514, 51.6509, 9.2557, 12.6491)

# Ask the user to select a Bundesland
print("Select a Bundesland:")
print("1. Baden-Württemberg")
print("2. Bavaria (Bayern)")
print("3. Berlin")
print("4. Brandenburg")
print("5. Bremen")
print("6. Hamburg")
print("7. Hesse (Hessen)")
print("8. Lower Saxony (Niedersachsen)")
print("9. Mecklenburg-Vorpommern")
print("10. North Rhine-Westphalia (Nordrhein-Westfalen)")
print("11. Rhineland-Palatinate (Rheinland-Pfalz)")
print("12. Saarland")
print("13. Saxony (Sachsen)")
print("14. Saxony-Anhalt (Sachsen-Anhalt)")
print("15. Schleswig-Holstein")
print("16. Thuringia (Thüringen)")
print()

# Get the user's choice
choice = int(input("Enter your choice: "))
print()

# Get the selected Bundesland
if choice == 1:
    bundesland = baden_wuerttemberg
elif choice == 2:
    bundesland = bavaria
elif choice == 3:
    bundesland = berlin
elif choice == 4:
    bundesland = brandenburg
elif choice == 5:
    bundesland = bremen
elif choice == 6:
    bundesland = hamburg
elif choice == 7:
    bundesland = hessen
elif choice == 8:
    bundesland = lower_saxony
elif choice == 9:
    bundesland = mecklenburg_vorpommern
elif choice == 10:
    bundesland = north_rhine_westphalia
elif choice == 11:
    bundesland = rheinland_pfalz
elif choice == 12:
    bundesland = saarland
elif choice == 13:
    bundesland = sachsen
elif choice == 14:
    bundesland = sachsen_anhalt
elif choice == 15:
    bundesland = schleswig_holstein
elif choice == 16:
    bundesland = thueringen
else:
    print("Invalid choice")
    exit()

# Get the bounding box for the selected Bundesland
min_lat = bundesland.min_lat
max_lat = bundesland.max_lat
min_lon = bundesland.min_lon
max_lon = bundesland.max_lon

# Ask the user to select a minimum zoom level and a maximum zoom level,
# the default values are 12 for both (which is the default if the user just presses Enter)
min_zoom = int(input("Enter minimum zoom level (default 12): ") or "12")
max_zoom = int(input("Enter maximum zoom level (default 12): ") or "12")
print()

metainfo = """
[url_template]
https://uas-betrieb.de/geoservices/dipul/ows?bbox={bbox}&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&LAYERS=dipul:flugplaetze,dipul:flughaefen,dipul:kontrollzonen,dipul:flugbeschraenkungsgebiete,dipul:bundesstrassen,dipul:bundesautobahnen,dipul:bahnanlagen,dipul:binnenwasserstrassen,dipul:seewasserstrassen,dipul:schifffahrtsanlagen,dipul:wohngrundstuecke,dipul:freibaeder,dipul:industrieanlagen,dipul:kraftwerke,dipul:umspannwerke,dipul:stromleitungen,dipul:windkraftanlagen,dipul:justizvollzugsanstalten,dipul:militaerische_anlagen,dipul:labore,dipul:behoerden,dipul:diplomatische_vertretungen,dipul:internationale_organisationen,dipul:polizei,dipul:sicherheitsbehoerden,dipul:krankenhaeuser,dipul:nationalparks,dipul:naturschutzgebiete,dipul:vogelschutzgebiete,dipul:ffh-gebiete&TILED=false&WIDTH=512&HEIGHT=512&CRS=CRS:84&STYLES=
[ext]
.png
[min_zoom]
""" + str(min_zoom) + """
[max_zoom]
""" + str(max_zoom) + """
[tile_size]
512
[img_density]
16
[avg_img_size]
512000
"""

# Array "tiles" should hold Tile objects
tiles = []

if min_zoom == max_zoom:
    tiles = calculate_tiles(min_lat, max_lat, min_lon, max_lon, min_zoom)
else:
    for zoom in range(min_zoom, max_zoom + 1):
        more_tiles = calculate_tiles(min_lat, max_lat, min_lon, max_lon, zoom)
        tiles.extend(more_tiles)

# print(tiles)

def download_tile(tile):
    # Return the filename if the file already exists
    if os.path.exists(tile.filename):
        return tile.filename
    try:
        print(tile.filename)
        os.makedirs(os.path.dirname(tile.filename), exist_ok=True)
        urllib.request.urlretrieve(tile.url, tile.filename)
        return tile.filename
    except Exception as e:
        return str(e)


i = 0
for tile in tiles:
    i += 1
    print("Tile", i, "of", len(tiles))
    download_tile(tile)

print("Number of tiles:", len(tiles))

# Create the file dipul/.metainfo
with open("dipul/.metainfo", "w") as f:
    f.write(metainfo)
