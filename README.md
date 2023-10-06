# dipulOsmAnd

All important information on the current NOTAMs, RMZs and TMZs for UAS in German airspace as offline tiles for OsmAnd

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

Put the directory "DIPUL" into the directory `Android/data/net.osmand.plus/files/tiles` on the Android device.

Then it can be selected as an overlay map in the [OsmAnd](https://osmand.net/) app.
