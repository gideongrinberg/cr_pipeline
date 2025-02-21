import os
import sys

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))

import io
import base64
from nicegui import ui

from pipeline.plotting import plot_lc as plot_complexity_check
from pipeline.lightcurves import load_lc

# Create a row that splits the screen into a sidebar and a main content area.
with ui.row().classes('w-full h-full'):
    # Sidebar: fixed width (e.g., 16rem) with padding and a background color.
    with ui.column().classes('w-64 p-4 bg-gray-100'):
        ui.label("Load Lightcurve")
        tic_input = ui.input(label="TIC", placeholder="Enter TIC number")
        sector_input = ui.input(label="Sector", placeholder="Enter Sector number")
        
        def load_and_plot():
            tic = tic_input.value
            sector = int(sector_input.value)

            lc = load_lc(tic, sector)
            fig = plot_complexity_check(lc)
            
            # Convert the matplotlib figure to a PNG image and encode it as a data URI.
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            img_data = buf.read()
            img_base64 = base64.b64encode(img_data).decode("utf-8")
            data_uri = f"data:image/png;base64,{img_base64}"
            plot_image.set_source(data_uri)
        
        ui.button("Load", on_click=load_and_plot)
    
    # Main area: expands to take up remaining space.
    with ui.column().classes('flex-grow p-4'):
        # The image widget will display the plot. Its style makes it fill the width.
        plot_image = ui.image().style('width: 100%; height: auto;')

ui.run()