# Stitch_cycles

## About
Stitch_cycles is a Python-based project inspired by the Inria MFX team's research on 3D printing. The goal is to optimize 3D printing paths by solving a constrained variation of the Traveling Salesman Problem (TSP). Instead of printing multiple separate cycles (which requires lifting the printer nozzle repeatedly, potentially leaving stringing artifacts), this algorithm "stitches" non-intersecting cycles together into a single continuous path. 

## Features
- Parses SVG cycles and paths.
- Converts cycles into a mathematical graph.
- Calculates and links the nearest non-intersecting cycles together.

## How to Use

### Install Dependencies
   Ensure you have the required packages, such as `svgpathtools` and `numpy`.
   
   ```bash
   pip install svgpathtools numpy
   ```

### Run the code
You can extract point coordinates and build the cycle graph from an SVG file by running `test_svg.py`. Alternatively, you can use the modules directly in your own script:

```python
import svg_handler as svgh
import stitch_base as sb

path = svgh.pointCoord("svg_entries\svg\simple.svg")

graph = svgh.cyclesToGraph("svg_entries\svg\simple.svg")
```

## Details
For an in-depth analysis of our implementation, please refer to the `Rapport_stitch_edges.pdf` project report.