# dipulOsmAnd

All important information on RMZs and TMZs for UAS in German airspace as offline tiles for [OsmAnd](https://osmand.net/). Data provided by the [Digital Platform for Unmanned Aviation (dipul)](https://maptool-dipul.dfs.de/?language=en) published by the German Federal Ministry for Digital and Transport (BMDV)

## Motivation

Have functionality similar to the proprietary [Droniq app](https://droniq.de/droniq-app/) but
* Using an open source app, [OsmAnd](https://osmand.net/)
* Offline (no internet connection required while out in the field)

## Usage

Run the Python script like this:

```
% python3 dipulOsmAnd.py

Select a Bundesland:
1. Baden-Württemberg
2. Bavaria (Bayern)
3. Berlin
4. Brandenburg
5. Bremen
6. Hamburg
7. Hesse (Hessen)
8. Lower Saxony (Niedersachsen)
9. Mecklenburg-Vorpommern
10. North Rhine-Westphalia (Nordrhein-Westfalen)
11. Rhineland-Palatinate (Rheinland-Pfalz)
12. Saarland
13. Saxony (Sachsen)
14. Saxony-Anhalt (Sachsen-Anhalt)
15. Schleswig-Holstein
16. Thuringia (Thüringen)

Enter your choice: 1

Enter minimum zoom level (default 12): 12
Enter maximum zoom level (default 12): 12

Tile 1 of 1400
DIPUL/12/2133/1392.png.tile
Tile 2 of 1400
DIPUL/12/2134/1392.png.tile
Tile 3 of 1400
DIPUL/12/2135/1392.png.tile
...
```

Put the directory "dipul" folder to `/storage/emulated/0/Android/media/net.osmand.plus/files/tiles/dipul` on the Android device. Before doing so, set up OsmAnd to use the `/storage/emulated/0/Android/media/net.osmand.plus/files/` folder instead of the default `data` one, which is no longer easily accessible in newer versions of Android.

Create `/storage/emulated/0/Android/media/net.osmand.plus/files/tiles/dipul/.metainfo` with the following content

```
[url_template]
https://uas-betrieb.de/geoservices/dipul/ows?bbox={bbox}&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&LAYERS=dipul:flugplaetze,dipul:flughaefen,dipul:kontrollzonen,dipul:flugbeschraenkungsgebiete,dipul:bundesstrassen,dipul:bundesautobahnen,dipul:bahnanlagen,dipul:binnenwasserstrassen,dipul:seewasserstrassen,dipul:schifffahrtsanlagen,dipul:wohngrundstuecke,dipul:freibaeder,dipul:industrieanlagen,dipul:kraftwerke,dipul:umspannwerke,dipul:stromleitungen,dipul:windkraftanlagen,dipul:justizvollzugsanstalten,dipul:militaerische_anlagen,dipul:labore,dipul:behoerden,dipul:diplomatische_vertretungen,dipul:internationale_organisationen,dipul:polizei,dipul:sicherheitsbehoerden,dipul:krankenhaeuser,dipul:nationalparks,dipul:naturschutzgebiete,dipul:vogelschutzgebiete,dipul:ffh-gebiete&TILED=false&WIDTH=512&HEIGHT=512&CRS=CRS:84&STYLES=
[ext]
.png
[min_zoom]
8
[max_zoom]
20
[tile_size]
512
[img_density]
16
[avg_img_size]
18000
```

Then "dipul" can be selected as an overlay map in the [OsmAnd](https://osmand.net/) app.

Actually, when using this `.metainfo`, then there is no need to copy the pre-downloaded tiles using the script in this repository, as the Android device will download them on the fly and keep them forever (if not configured otherwise).
