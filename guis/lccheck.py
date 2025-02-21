import os
import sys

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))

import io
import csv
import glob
import base64
from nicegui import ui

from pipeline.lightcurves import load_lc
from pipeline.plotting import plot_lc

targets = []
for file in glob.glob("./lightcurves/*.csv"):
    tic, sector = file.split("/")[2].strip(".csv").split("_")
    targets.append((f"TIC {tic}", sector))

current_index = 0  # Global index for the current target.
results_file = 'results.csv'

# Write CSV header (overwrites any existing file).
with open(results_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['TIC', 'Sector', 'Complex'])

# --- Functions ---
def load_plot():
    global current_index
    if current_index < len(targets):
        tic, sector = targets[current_index]
        lc = load_lc(tic, sector)
        fig = plot_lc(lc)
        # Update plot title with TIC and Sector info.
        fig.axes[0].set_title(f"Lightcurve for TIC {tic}, Sector {sector}")
        # Convert the figure to a PNG image.
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        img_data = buf.read()
        img_base64 = base64.b64encode(img_data).decode("utf-8")
        data_uri = f"data:image/png;base64,{img_base64}"
        plot_image.set_source(data_uri)
        # ui.notify(f"Loaded TIC {tic} Sector {sector}")
    else:
        ui.notify("All targets have been labeled.", color="positive")
        complex_button.disable()
        not_complex_button.disable()

def label_current(is_complex: bool):
    global current_index
    if current_index < len(targets):
        tic, sector = targets[current_index]
        # Append the label to the CSV.
        with open(results_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([tic, sector, is_complex])
        # ui.notify(f"Labeled TIC {tic}, Sector {sector} as {'Complex' if is_complex else 'Not Complex'}")
        current_index += 1
        load_plot()
    else:
        ui.notify("No more targets to label.", color="negative")

# --- UI Layout ---
with ui.column().classes('items-center w-full h-full'):
    ui.label("Lightcurve Labeling Tool")
    # Image widget to display the plot; styled to fill most of the area.
    plot_image = ui.image().style('max-width: 80%; height: auto; margin-bottom: 20px;')
    # Row for labeling controls.
    with ui.row():
        # Buttons with keyboard shortcuts ("c" for Complex, "n" for Not Complex).
        complex_button = ui.button("Complex", on_click=lambda: label_current(True))
        not_complex_button = ui.button("Not Complex", on_click=lambda: label_current(False))

# Load the first plot when the app starts.
load_plot()

ui.run()