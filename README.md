# GPX-Vis

A simple Python tool for visualizing GPX track files.

## Features

- Parses GPX files to extract track points
- Creates interactive web maps using Folium
- Generates static map visualizations using Matplotlib
- Supports multiple GPX tracks with color coding

## Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for Python package management.

```bash
# Clone the repository
git clone https://github.com/yourusername/gpx-vis.git
cd gpx-vis

# Install dependencies with uv
uv pip install -e .
```

## Usage

1. Place your GPX files in the `data/` directory
2. Run the visualization script:

```bash
# Run with uv
uv run python main.py
```

The script will generate:
- An interactive HTML map (`gpx_tracks.html`)
- A static PNG image (`gpx_tracks.png`)

## Requirements

- Python e 3.13
- Dependencies: colormap, folium, gpxpy, matplotlib, numpy