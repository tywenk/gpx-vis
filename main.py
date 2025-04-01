import os
import glob
import folium
import gpxpy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


def parse_gpx_file(gpx_file):
    """Parse a GPX file and extract track points."""
    with open(gpx_file, "r") as f:
        gpx = gpxpy.parse(f)

    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(
                    (point.latitude, point.longitude, point.elevation, point.time)
                )

    return points


def visualize_with_folium(gpx_files, output_file="gpx_tracks.html"):
    """Create an interactive map visualization using folium."""
    # Initialize map
    m = folium.Map()
    bounds = []

    # Color map for multiple tracks
    colors = cm.rainbow(np.linspace(0, 1, len(gpx_files)))

    for i, gpx_file in enumerate(gpx_files):
        points = parse_gpx_file(gpx_file)
        if not points:
            continue

        # Extract coordinates for the map
        coordinates = [(lat, lon) for lat, lon, _, _ in points]
        bounds.extend(coordinates)

        # Create a polyline for this track
        # Fix: Convert float RGB values to hex color string
        r, g, b, _ = colors[i]
        color = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

        track_name = os.path.basename(gpx_file)

        # Add a black outline by creating two polylines
        # First, create a slightly thicker black line
        folium.PolyLine(
            coordinates,
            tooltip=track_name,
            color="black",
            weight=6,  # Thicker line for the outline
            opacity=0.8,
        ).add_to(m)

        # Then overlay the colored line (slightly thinner)
        folium.PolyLine(
            coordinates,
            tooltip=track_name,
            color=color,
            weight=3,  # Main colored line
            opacity=0.9,
        ).add_to(m)

    # Fit the map to the bounds of all tracks
    if bounds:
        m.fit_bounds(bounds)

    # Save the map
    m.save(output_file)
    print(f"Map saved to {output_file}")


def visualize_with_matplotlib(gpx_files, output_file="gpx_tracks.png"):
    """Create a static image visualization using matplotlib."""
    plt.figure(figsize=(12, 8))

    # Color map for multiple tracks
    colors = cm.rainbow(np.linspace(0, 1, len(gpx_files)))

    for i, gpx_file in enumerate(gpx_files):
        points = parse_gpx_file(gpx_file)
        if not points:
            continue

        # Extract coordinates
        lats = [p[0] for p in points]
        lons = [p[1] for p in points]

        # Plot this track
        color = colors[i]
        track_name = os.path.basename(gpx_file)

        # Add black outline effect by plotting a black line underneath
        plt.plot(lons, lats, color="black", linewidth=4, alpha=0.8)
        # Then plot the colored line on top
        plt.plot(lons, lats, color=color, label=track_name, linewidth=2)

    plt.title("GPX Tracks Visualization")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.legend()

    # Save the plot
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Plot saved to {output_file}")


def main():
    # Specify the data folder path
    data_folder = "data"  # Change this to your data folder path

    # Get all GPX files from the data folder
    gpx_files = glob.glob(os.path.join(data_folder, "*.gpx"))

    if not gpx_files:
        print(f"No GPX files found in the {data_folder} directory.")
        return

    print(
        f"Found {len(gpx_files)} GPX files: {', '.join([os.path.basename(f) for f in gpx_files])}"
    )

    # Create both visualizations
    visualize_with_folium(gpx_files)
    visualize_with_matplotlib(gpx_files)

    print("Visualizations complete.")


if __name__ == "__main__":
    main()
