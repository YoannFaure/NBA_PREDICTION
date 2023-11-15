import requests
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="NBA Player Stats Explorer",
)
# Création page
st.sidebar.markdown("Dashboard")

st.title("NBA Player Stats Explorer")


# Importation data
@st.cache_data
def load_data():
    data = pd.read_csv(
        "/Users/yoannfaure/Library/CloudStorage/OneDrive-Personnel/2. Yoann Personnel/14. Pro_Perso/1. Formation Data/Datascientest/VsCode/NBA/data/NBA_Shot_Locations_1997-2020/NBA_Shot_Locations_1997-2020.csv"
    )
    return data


# Charger le DataFrame en utilisant la fonction mise en cache
data = load_data()

# Créez un widget multiselect
selected_player = st.multiselect(
    "Sélectionnez un joueur",
    data["Player Name"].unique(),
    default=["LeBron James"],
    max_selections=1,
)

# Filtrer les données en fonction du joueur sélectionné
if selected_player:
    data = data[data["Player Name"].isin(selected_player)]


#################################################
#################################################

# Default parameters for initialisation
# Note that default params should be the first option in widgets
player_id = 202695
season_type = "Regular Season"
season_year = "2018-19"


#########################################
# Side bar interactive widgets
#########################################
# Side bar Header
st.sidebar.header("Configure your player shot chart below!")
st.sidebar.markdown(":sunglasses: :basketball:")

# Player Radio Button
player_name = st.sidebar.radio(
    "Whose shot chart do you want to see?",
    (
        "Kawhi Leonard",
        "James Harden",
        "Kobe Bryant",
        "Lebron James",
        "Steph Curry",
        "Giannis Antetokounmpo",
        "Trae Young",
        "Luka Doncic",
    ),
)
player_id = player_dict[player_name]

# Season Radio Button
season_type_selection = st.sidebar.radio(
    "Which season type do you prefer?", ("Regular Season", "Playoffs")
)

if season_type_selection == "Regular Season":
    season_type = "Regular Season"
else:
    season_type = "Playoffs"

# Season year slider
season_year_slider = st.sidebar.slider(
    "Which season year?", min_value=2008, max_value=2019, value=2018
)

season_year_back_suffix = str(season_year_slider + 1)[-2:]
season_year = str(season_year_slider) + "-" + season_year_back_suffix

response = pull_data(player_id, season_type, season_year)


#########################################
# Plot data
#########################################
def draw_court(ax=None, color="black", lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Create free throw top arc
    top_free_throw = Arc(
        (0, 142.5),
        120,
        120,
        theta1=0,
        theta2=180,
        linewidth=lw,
        color=color,
        fill=False,
    )
    # Create free throw bottom arc
    bottom_free_throw = Arc(
        (0, 142.5),
        120,
        120,
        theta1=180,
        theta2=0,
        linewidth=lw,
        color=color,
        linestyle="dashed",
    )
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc(
        (0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color
    )
    center_inner_arc = Arc(
        (0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color
    )

    # List of the court elements to be plotted onto the axes
    court_elements = [
        hoop,
        backboard,
        outer_box,
        inner_box,
        top_free_throw,
        bottom_free_throw,
        restricted,
        corner_three_a,
        corner_three_b,
        three_arc,
        center_outer_arc,
        center_inner_arc,
    ]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle(
            (-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False
        )
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax


# create our jointplot
# color selection for season_type
if season_type == "Regular Season":
    color_selection = plt.cm.gist_heat_r(0.2)
else:
    color_selection = plt.cm.winter(0.1)
joint_shot_chart = sns.jointplot(
    shot_df.LOC_X,
    shot_df.LOC_Y,
    stat_func=None,
    kind="scatter",
    space=0,
    alpha=0.5,
    color=color_selection,
)

joint_shot_chart.fig.set_size_inches(12, 11)

# A joint plot has 3 Axes, the first one called ax_joint
# is the one we want to draw our court onto and adjust some other settings
ax = joint_shot_chart.ax_joint
draw_court(ax)

# Adjust the axis limits and orientation of the plot in order
# to plot half court, with the hoop by the top of the plot
ax.set_xlim(-250, 250)
ax.set_ylim(422.5, -47.5)

# Get rid of axis labels and tick marks
ax.set_xlabel("")
ax.set_ylabel("")
ax.tick_params(labelbottom="off", labelleft="off")
###########################################

# Plot execution

st.subheader(
    "NBA Shot Chart for "
    + player_name
    + " in "
    + season_year
    + " "
    + season_type_selection
)

st.pyplot()
