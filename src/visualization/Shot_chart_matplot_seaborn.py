############################### IMPORTS ###############################

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.express as px
import plotly.io as pio
import ipywidgets as widgets
from IPython.display import display
from ipywidgets import interact
from ipywidgets import Dropdown


############################### LOAD DATAFRAME ###############################

df = pd.read_csv(
    "../../data/raw/NBA_Shot_Locations_1997-2020/NBA_Shot_Locations_1997-2020.csv"
)
df = df[df["Player Name"] == "Stephen Curry"]

df.head()
###################### DRAW PLAYER SHOT CHART ######################

#################### Draw Court #####################


def add_court_shapes(fig):
    """Adds a basketball court to a Plotly graph.

    Args:
      fig: A Plotly graph object.

    Returns:
      A Plotly graph object with the basketball court added.
    """

    # Cercle 1
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=-3,
        y0=-3,
        x1=3,
        y1=3,
        line=dict(color="White", width=1),
    )

    # Cercle 2
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=-60,
        y0=77,
        x1=60,
        y1=197,
        line=dict(color="White", width=1),
    )

    # Cercle center
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=-60,
        y0=357,
        x1=60,
        y1=477,
        line=dict(color="White", width=1),
    )

    # Backboard
    fig.add_shape(
        type="line",
        xref="x",
        yref="y",
        x0=-30,
        y0=-7.5,
        x1=30,
        y1=-7.5,
        line=dict(color="White", width=1),
    )

    # Court width=50ft, height=47ft
    fig.add_shape(
        type="rect",
        x0=-250,
        y0=-53,
        x1=250,
        y1=417,
        line=dict(color="White", width=1),
    )

    # intern width=16ft, height=19ft
    fig.add_shape(
        type="rect",
        x0=-80,
        y0=-53,
        x1=80,
        y1=137,
        line=dict(color="White", width=1),
    )

    # Add the 3-point line
    fig.add_shape(
        type="path", path="M-220, 87 Q 0,390 220,87", line=dict(color="White", width=1)
    )

    fig.add_shape(
        type="path", path="M -40,0 Q 0,40 40,0", line=dict(color="White", width=1)
    )

    fig.add_shape(
        type="line",
        xref="x",
        yref="y",
        x0=-220,
        y0=-53,
        x1=-220,
        y1=87,
        line=dict(color="White", width=1),
    )

    fig.add_shape(
        type="line",
        xref="x",
        yref="y",
        x0=220,
        y0=-53,
        x1=220,
        y1=87,
        line=dict(color="White", width=1),
    )
    fig.update_layout(
        width=635,  # Largeur en pixels
        height=675,  # Hauteur en pixels
        xaxis_range=[-300, 300],  # Ajustez les limites de l'axe X
        yaxis_range=[-100, 500],  # Ajustez les limites de l'axe Y
        showlegend=False,  # Masquez la légende
        xaxis_fixedrange=True,  # Désactive le zoom sur l'axe X
        yaxis_fixedrange=True,  # Désactive le zoom sur l'axe Y
        xaxis_autorange=False,  # Désactive l'autoscale sur l'axe X
        yaxis_autorange=False,  # Désactive l'autoscale sur l'axe Y
    )
    # Supprimez les lignes des axes
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    # Supprimez les valeurs des axes
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    # Supprimez la légende
    fig.update_layout(showlegend=False)
    # Inversez les valeurs y de la figure
    fig.update_yaxes(autorange=False, range=[500, -100])


fig = go.Figure()
add_court_shapes(fig)


#################### PLAYER SHOT LOCATION #####################

fig = go.Figure()
add_court_shapes(fig)
fig.add_trace(
    go.Scatter(
        x=df[df["Shot Made Flag"] == 1]["X Location"],
        y=df[df["Shot Made Flag"] == 1]["Y Location"],
        mode="markers",
        marker=dict(color="blue", size=5),  # Utilisez le bleu pour "Shot Made Flag" = 1
        text=df[df["Shot Made Flag"] == 1]["Action Type"],
        hoverinfo="text",
        showlegend=True,
        name="Made Shots",
    )
)

fig.add_trace(
    go.Scatter(
        x=df[df["Shot Made Flag"] == 0]["X Location"],
        y=df[df["Shot Made Flag"] == 0]["Y Location"],
        mode="markers",
        marker=dict(color="gray", size=5),  # Utilisez le gris pour "Shot Made Flag" = 0
        text=df[df["Shot Made Flag"] == 1]["Action Type"],
        hoverinfo="text",
        showlegend=True,
        name="Missed Shots",
    )
)

fig.show()


################################

fig = go.Figure()
add_court_shapes(fig)

# Filtrez le DataFrame pour les tirs réussis uniquement
made_shots = df[df["Shot Made Flag"] == 1]

# Créez un histogramme 2D (hexbin plot)
hexbin = go.Histogram2d(
    x=made_shots["X Location"],
    y=made_shots["Y Location"],
    colorscale="Viridis",
    nbinsx=30,
    nbinsy=20,
)

fig.add_trace(hexbin)

fig.show()
