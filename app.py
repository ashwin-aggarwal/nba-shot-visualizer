import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Arc
import os

# Set page configuration
st.set_page_config(
    page_title="NBA Shot Visualizer",
    page_icon="🏀",
    layout="wide"
)

# API Configuration
API_KEY = os.getenv("API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "https://stats.nba.com/stats"

def get_player_id(player_name):
    """Get player ID from NBA API"""
    url = f"{BASE_URL}/commonallplayers"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://stats.nba.com/',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true'
    }
    
    params = {
        'IsOnlyCurrentSeason': '0',
        'LeagueID': '00',
        'Season': '2024-25'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        players = data['resultSets'][0]['rowSet']
        for player in players:
            if player_name.lower() in player[2].lower():
                return player[0]
        return None
    except Exception as e:
        st.error(f"Error fetching player ID for {player_name}: {str(e)}")
        return None

def get_shot_data(player_id, season):
    """Fetch shot data for a player from NBA API"""
    url = f"{BASE_URL}/shotchartdetail"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://stats.nba.com/',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true'
    }
    
    params = {
        'PlayerID': player_id,
        'Season': season,
        'SeasonType': 'Regular Season',
        'TeamID': '0',
        'GameID': '',
        'Outcome': '',
        'Location': '',
        'Month': '0',
        'SeasonSegment': '',
        'DateFrom': '',
        'DateTo': '',
        'OpponentTeamID': '0',
        'VsConference': '',
        'VsDivision': '',
        'Position': '',
        'RookieYear': '',
        'GameSegment': '',
        'Period': '0',
        'LastNGames': '0',
        'ClutchTime': '',
        'AheadBehind': '',
        'PointDiff': '',
        'RangeType': '',
        'StartPeriod': '',
        'EndPeriod': '',
        'StartRange': '',
        'EndRange': '',
        'ContextFilter': '',
        'ContextMeasure': 'FGA'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data['resultSets'] and len(data['resultSets']) > 0:
            headers_list = data['resultSets'][0]['headers']
            shots = data['resultSets'][0]['rowSet']
            
            if shots:
                df = pd.DataFrame(shots, columns=headers_list)
                return df
            else:
                return pd.DataFrame()
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching shot data: {str(e)}")
        return pd.DataFrame()

def draw_court(ax):
    """Draw basketball court on matplotlib axis"""
    # Court dimensions (in feet, converted to NBA API coordinates)
    # NBA court is 94 feet long, 50 feet wide
    # API coordinates: center at (0,0), range roughly -250 to +250 for x, -50 to +420 for y
    
    # Clear the axis
    ax.clear()
    
    # Set court boundaries
    ax.set_xlim(-250, 250)
    ax.set_ylim(-50, 420)
    
    # Draw court outline
    court_outline = patches.Rectangle((-250, -50), 500, 470, 
                                    linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(court_outline)
    
    # Draw center court circle
    center_circle = patches.Circle((0, 420), 60, linewidth=2, 
                                 edgecolor='black', facecolor='none')
    ax.add_patch(center_circle)
    
    # Draw three-point arc (23.75 feet = ~237.5 units in API coordinates)
    three_point_arc = Arc((0, 0), 474, 474, theta1=0, theta2=180, 
                         linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(three_point_arc)
    
    # Draw three-point line sides
    ax.plot([-220, -220], [0, 140], 'k-', linewidth=2)
    ax.plot([220, 220], [0, 140], 'k-', linewidth=2)
    
    # Draw free throw circle
    free_throw_circle = patches.Circle((0, 140), 60, linewidth=2, 
                                     edgecolor='black', facecolor='none')
    ax.add_patch(free_throw_circle)
    
    # Draw lane
    lane = patches.Rectangle((-80, 0), 160, 140, linewidth=2, 
                           edgecolor='black', facecolor='none')
    ax.add_patch(lane)
    
    # Draw basket
    basket = patches.Circle((0, 0), 7.5, linewidth=2, 
                          edgecolor='black', facecolor='none')
    ax.add_patch(basket)
    
    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

def plot_shots_scatter(df, ax, player_name):
    """Plot shots as scatter plot"""
    if df.empty:
        ax.text(0, 200, f"No shot data available for {player_name}", 
                ha='center', va='center', fontsize=12)
        return
    
    # Filter shots with valid coordinates
    valid_shots = df[(df['LOC_X'].notna()) & (df['LOC_Y'].notna())]
    
    if valid_shots.empty:
        ax.text(0, 200, f"No valid shot coordinates for {player_name}", 
                ha='center', va='center', fontsize=12)
        return
    
    # Plot made shots in green
    made_shots = valid_shots[valid_shots['SHOT_MADE_FLAG'] == 1]
    if not made_shots.empty:
        ax.scatter(made_shots['LOC_X'], made_shots['LOC_Y'], 
                  c='green', s=20, alpha=0.6, label='Made')
    
    # Plot missed shots in red
    missed_shots = valid_shots[valid_shots['SHOT_MADE_FLAG'] == 0]
    if not missed_shots.empty:
        ax.scatter(missed_shots['LOC_X'], missed_shots['LOC_Y'], 
                  c='red', s=20, alpha=0.6, label='Missed')
    
    ax.set_title(f"{player_name} - Shot Chart", fontsize=14)
    ax.legend()

def plot_shots_heatmap(df, ax, player_name):
    """Plot shots as hexbin heatmap"""
    if df.empty:
        ax.text(0, 200, f"No shot data available for {player_name}", 
                ha='center', va='center', fontsize=12)
        return
    
    # Filter shots with valid coordinates
    valid_shots = df[(df['LOC_X'].notna()) & (df['LOC_Y'].notna())]
    
    if valid_shots.empty:
        ax.text(0, 200, f"No valid shot coordinates for {player_name}", 
                ha='center', va='center', fontsize=12)
        return
    
    # Create hexbin plot
    hb = ax.hexbin(valid_shots['LOC_X'], valid_shots['LOC_Y'], 
                   gridsize=25, bins='log', mincnt=1, cmap='YlOrRd')
    
    ax.set_title(f"{player_name} - Shot Density", fontsize=14)
    
    # Add colorbar
    plt.colorbar(hb, ax=ax, label='Log(Shot Attempts)')

def calculate_stats(df):
    """Calculate shooting statistics"""
    if df.empty:
        return {
            'total_shots': 0,
            'made_shots': 0,
            'fg_percentage': 0,
            'three_point_attempts': 0,
            'three_point_made': 0,
            'three_point_percentage': 0
        }
    
    total_shots = len(df)
    made_shots = len(df[df['SHOT_MADE_FLAG'] == 1])
    fg_percentage = (made_shots / total_shots * 100) if total_shots > 0 else 0
    
    # Three-point shots (assuming SHOT_TYPE contains '3PT')
    three_point_shots = df[df['SHOT_TYPE'].str.contains('3PT', na=False)]
    three_point_attempts = len(three_point_shots)
    three_point_made = len(three_point_shots[three_point_shots['SHOT_MADE_FLAG'] == 1])
    three_point_percentage = (three_point_made / three_point_attempts * 100) if three_point_attempts > 0 else 0
    
    return {
        'total_shots': total_shots,
        'made_shots': made_shots,
        'fg_percentage': fg_percentage,
        'three_point_attempts': three_point_attempts,
        'three_point_made': three_point_made,
        'three_point_percentage': three_point_percentage
    }

# Main App
st.title("🏀 NBA Shot Visualizer")

# Input controls
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

with col1:
    season = st.selectbox(
        "NBA Season",
        ["2024-25", "2023-24", "2022-23", "2021-22", "2020-21"],
        index=0
    )

with col2:
    player1_name = st.text_input("Player 1 Name", value="LeBron James")

with col3:
    player2_name = st.text_input("Player 2 Name", value="Stephen Curry")

with col4:
    compare_button = st.button("Compare", type="primary")

# Process comparison when button is clicked
if compare_button:
    if not player1_name or not player2_name:
        st.error("Please enter both player names.")
    else:
        with st.spinner("Fetching player data..."):
            # Get player IDs
            player1_id = get_player_id(player1_name)
            player2_id = get_player_id(player2_name)
            
            if not player1_id:
                st.error(f"Could not find player: {player1_name}")
            elif not player2_id:
                st.error(f"Could not find player: {player2_name}")
            else:
                # Fetch shot data
                with st.spinner("Fetching shot data..."):
                    player1_shots = get_shot_data(player1_id, season)
                    player2_shots = get_shot_data(player2_id, season)
                
                # Create tabs for different visualizations
                tab1, tab2 = st.tabs(["Scatter", "Heatmap"])
                
                with tab1:
                    # Create scatter plot
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
                    
                    # Draw courts
                    draw_court(ax1)
                    draw_court(ax2)
                    
                    # Plot shots
                    plot_shots_scatter(player1_shots, ax1, player1_name)
                    plot_shots_scatter(player2_shots, ax2, player2_name)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                
                with tab2:
                    # Create heatmap
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
                    
                    # Draw courts
                    draw_court(ax1)
                    draw_court(ax2)
                    
                    # Plot heatmaps
                    plot_shots_heatmap(player1_shots, ax1, player1_name)
                    plot_shots_heatmap(player2_shots, ax2, player2_name)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                
                # Display statistics
                st.subheader("📊 Shooting Statistics")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**{player1_name}**")
                    stats1 = calculate_stats(player1_shots)
                    st.write(f"Total Shots: {stats1['total_shots']}")
                    st.write(f"Made Shots: {stats1['made_shots']}")
                    st.write(f"FG%: {stats1['fg_percentage']:.1f}%")
                    st.write(f"3P Attempts: {stats1['three_point_attempts']}")
                    st.write(f"3P Made: {stats1['three_point_made']}")
                    st.write(f"3P%: {stats1['three_point_percentage']:.1f}%")
                
                with col2:
                    st.write(f"**{player2_name}**")
                    stats2 = calculate_stats(player2_shots)
                    st.write(f"Total Shots: {stats2['total_shots']}")
                    st.write(f"Made Shots: {stats2['made_shots']}")
                    st.write(f"FG%: {stats2['fg_percentage']:.1f}%")
                    st.write(f"3P Attempts: {stats2['three_point_attempts']}")
                    st.write(f"3P Made: {stats2['three_point_made']}")
                    st.write(f"3P%: {stats2['three_point_percentage']:.1f}%")

# Instructions
st.sidebar.markdown("## Instructions")
st.sidebar.markdown("1. Select an NBA season from the dropdown")
st.sidebar.markdown("2. Enter two player names to compare")
st.sidebar.markdown("3. Click 'Compare' to fetch and visualize shot data")
st.sidebar.markdown("4. Use the tabs to switch between scatter plot and heatmap views")

st.sidebar.markdown("## About")
st.sidebar.markdown("This app visualizes NBA player shooting patterns using real NBA API data. " \
"The scatter plot shows individual shots (green for made, red for missed), while the heatmap shows shot density using logarithmic scaling.")
