import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc

# Replace with your API key
API_KEY = "1915c6c481mshaa390fe9db9d4dfp1d942ejsnee7efcefdb82"

st.set_page_config(page_title="NBA Shot Visualizer", layout="wide")
st.title("NBA Shot Visualizer")

# Function to draw basketball court
def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    if ax is None:
        ax = plt.gca()

    # Create the basketball hoop
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, 0, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # Create the inner box of the paint, width=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bounds lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

# Function to fetch player shots
def fetch_player_shots(player_name, season):
    # First, get the player ID
    url = "https://api-nba-v1.p.rapidapi.com/players"
    querystring = {"search": player_name}
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        st.error(f"Error fetching player data: {response.status_code}")
        return None
    
    data = response.json()
    if not data.get('results', 0) or not data.get('response', []):
        st.error(f"No player found with name: {player_name}")
        return None
    
    player_id = data['response'][0]['id']
    
    # Now fetch the shots data
    url = "https://api-nba-v1.p.rapidapi.com/players/statistics"
    querystring = {"id": player_id, "season": season}
    
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        st.error(f"Error fetching shot data: {response.status_code}")
        return None
    
    data = response.json()
    
    # Process the data into a DataFrame
    # Note: This is a simplified version as the actual API response structure may vary
    shots = []
    for game in data.get('response', []):
        # Extract shot data from each game
        # This is a placeholder - you'll need to adapt this to the actual API response structure
        if 'fgm' in game and 'fga' in game:
            for _ in range(game['fga']):
                made = _ < game['fgm']
                # Generate random court positions for demonstration
                # In a real app, you'd use actual shot location data
                x = np.random.uniform(-250, 250)
                y = np.random.uniform(-47.5, 422.5)
                distance = np.sqrt(x**2 + y**2)
                shot_type = '3PT Field Goal' if distance > 237.5 else '2PT Field Goal'
                shots.append({
                    'locX': x,
                    'locY': y,
                    'shot_made_flag': 1 if made else 0,
                    'shot_distance': distance,
                    'shot_type': shot_type
                })
    
    if not shots:
        st.warning(f"No shot data available for {player_name} in {season} season")
        return None
    
    return pd.DataFrame(shots)

# Function to plot scatter
def plot_scatter(df, ax, title):
    if df is None or df.empty:
        ax.text(0, 0, "No data available", ha='center', va='center', fontsize=12)
        return
    
    # Draw the court
    draw_court(ax, color='black', lw=1)
    
    # Plot shots
    made_shots = df[df['shot_made_flag'] == 1]
    missed_shots = df[df['shot_made_flag'] == 0]
    
    ax.scatter(made_shots['locX'], made_shots['locY'], c='green', s=20, alpha=0.7, label='Made')
    ax.scatter(missed_shots['locX'], missed_shots['locY'], c='red', s=20, alpha=0.7, label='Missed')
    
    # Set the limits of the court
    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 422.5)
    
    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Add title and legend
    ax.set_title(title, fontsize=14)
    ax.legend(loc='upper right')
    
    # Calculate statistics
    total_shots = len(df)
    fg_pct = made_shots.shape[0] / total_shots * 100 if total_shots > 0 else 0
    three_pt_attempts = df[df['shot_type'] == '3PT Field Goal'].shape[0]
    three_pt_made = df[(df['shot_type'] == '3PT Field Goal') & (df['shot_made_flag'] == 1)].shape[0]
    three_pt_pct = three_pt_made / three_pt_attempts * 100 if three_pt_attempts > 0 else 0
    avg_distance = df['shot_distance'].mean()
    
    # Add statistics text box
    stats_text = (
        f"Total Attempts: {total_shots}\n"
        f"FG%: {fg_pct:.1f}%\n"
        f"3P%: {three_pt_pct:.1f}%\n"
        f"Avg Distance: {avg_distance:.1f} ft"
    )
    ax.text(0, -100, stats_text, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))

# Function to plot heatmap
def plot_heatmap(df, ax, title):
    if df is None or df.empty:
        ax.text(0, 0, "No data available", ha='center', va='center', fontsize=12)
        return
    
    # Draw the court
    draw_court(ax, color='black', lw=1)
    
    # Create hexbin plot
    hb = ax.hexbin(df['locX'], df['locY'], gridsize=25, cmap='plasma', bins='log')
    
    # Set the limits of the court
    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 422.5)
    
    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Add title
    ax.set_title(title, fontsize=14)
    
    # Add colorbar
    plt.colorbar(hb, ax=ax, label='Shot Frequency (log scale)')
    
    # Calculate statistics
    total_shots = len(df)
    made_shots = df[df['shot_made_flag'] == 1]
    fg_pct = made_shots.shape[0] / total_shots * 100 if total_shots > 0 else 0
    three_pt_attempts = df[df['shot_type'] == '3PT Field Goal'].shape[0]
    three_pt_made = df[(df['shot_type'] == '3PT Field Goal') & (df['shot_made_flag'] == 1)].shape[0]
    three_pt_pct = three_pt_made / three_pt_attempts * 100 if three_pt_attempts > 0 else 0
    avg_distance = df['shot_distance'].mean()
    
    # Add statistics text box
    stats_text = (
        f"Total Attempts: {total_shots}\n"
        f"FG%: {fg_pct:.1f}%\n"
        f"3P%: {three_pt_pct:.1f}%\n"
        f"Avg Distance: {avg_distance:.1f} ft"
    )
    ax.text(0, -100, stats_text, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7))

# Streamlit UI
st.sidebar.header("Select Parameters")

# Season selection
seasons = [str(year) + "-" + str(year + 1)[-2:] for year in range(2010, 2024)]
season = st.sidebar.selectbox("Select Season", seasons, index=len(seasons)-1)

# Player inputs
player1 = st.sidebar.text_input("Player 1", "LeBron James")
player2 = st.sidebar.text_input("Player 2", "Stephen Curry")

# Compare button
if st.sidebar.button("Compare"):
    with st.spinner("Fetching shot data..."):
        # Fetch data for both players
        df1 = fetch_player_shots(player1, season)
        df2 = fetch_player_shots(player2, season)
        
        # Create tabs for different visualizations
        tab1, tab2 = st.tabs(["Scatter", "Heatmap"])
        
        with tab1:
            st.header("Shot Scatter Plots")
            
            # Create a figure with two subplots side by side
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
            
            # Plot scatter for each player
            plot_scatter(df1, ax1, f"{player1} - {season}")
            plot_scatter(df2, ax2, f"{player2} - {season}")
            
            # Adjust layout and display
            plt.tight_layout()
            st.pyplot(fig)
        
        with tab2:
            st.header("Shot Heatmaps")
            
            # Create a figure with two subplots side by side
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
            
            # Plot heatmap for each player
            plot_heatmap(df1, ax1, f"{player1} - {season}")
            plot_heatmap(df2, ax2, f"{player2} - {season}")
            
            # Adjust layout and display
            plt.tight_layout()
            st.pyplot(fig)

# Initial instructions
if not st.session_state.get('button_clicked', False):
    st.info("Select a season and enter two player names, then click 'Compare' to visualize their shots.")
