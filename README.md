# USTC Search

## Prerequisites

Install the following dependencies (in a virtual environment, such as Anaconda) for working with 
 [OpenStreetMap](https://www.openstreetmap.org/) (OSM) data, and visualizing maps nicely in the browser.

Recommended: Use Python 3.9 to avoid dependency conflicts.

```bash
pip install -r requirements.txt
```

This command should work out of the box for all platforms (Linux, Mac OS, Windows).


## Visualizing the Map

To visualize a particular map, you can use the following:

```bash
python visualization.py

# You can customize the map and the landmarks
python visualization.py --map-file data/USTC-Main_Campus.pbf --landmark-file data/USTC-landmarks.json

# Visualize a particular solution path (requires running `grader.py` on question 1b/2b first!)
python visualization.py --path-file path.json
```

## Visible Test Cases

### Problem 1
- **1a**
  - 1a-1-basic
  - 1a-2-basic
  - 1a-4-basic
  - 1a-5-basic
  - 1a-6-basic
- **1b**
  - 1b-custom

### Problem 2
- **2a**
  - 2a-1-basic
  - 2a-2-basic
  - 2a-4-basic
  - 2a-5-basic
  - 2a-6-basic
- **2b**
  - 2b-custom

### Problem 3
- **3a**
  - 3a-1-basic
  - 3a-2-basic
- **3c**
  - 3c-heuristic-1-basic
  - 3c-astar-1-basic
  - 3c-astar-2-basic
- **3e**
  - 3e-heuristic-1-basic
  - 3e-astar-1-basic
  - 3e-astar-2-basic
- **3f**
  - 3f-without_Heuristic
  - 3f-with_Heuristic


## Creating a Custom Map [optional]

1. Use `extract.bbbike.org` to select a geographic region.
2. Download a `<name>.pbf` and place it in the `data` directory.

Note: While you are encouraged to explore creating your own maps as an additional exercise, for this assignment, please use the provided map of the University of Science and Technology of China (USTC). This ensures consistency across all submissions.

### Adding Custom Landmarks [optional]

Landmark files have the following format:

```json
[
  {"landmark": "the_original_north_gate", "geo": "31.84269,117.26350"},
  {"landmark": "east_campus_library", "amenity": "library", "geo": "31.83898,117.26387"},
  {"landmark": "statue_of_GuoMoruo", "geo": "31.84042,117.26370"},
  {"landmark": "Ruzi_Niu", "geo": "31.83754,117.26382"},
  {"landmark": "1958", "amenity": "coffee", "geo": "31.84047,117.26321"},
  ...
]
```
See `data/USTC-landmarks.json` for an example. You can add your own to `data/custom-landmarks.json`.

To add a landmark, find it on [OpenStreetMap](https://www.openstreetmap.org/) via [nominatim](https://nominatim.openstreetmap.org/) and 
copy the `Center Point (lat,lon)` from the `nominatim` webpage 
(e.g., [Gates Building](https://nominatim.openstreetmap.org/ui/details.html?osmtype=W&osmid=232841885&class=building),
and set that to be the value of `"geo"`.
