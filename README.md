# 🏀 NBA Shot Visualizer

A lightweight Streamlit-based web application that visualizes and compares NBA player shooting patterns using real NBA API data. Perfect for basketball analytics, coaching insights, and fan exploration of player performance.

## 🌟 Features

- **Season Selection**: Choose from recent NBA seasons (2024-25, 2023-24, etc.)
- **Player Comparison**: Compare shooting patterns between any two NBA players
- **Dual Visualization Modes**:
  - **Scatter Plot**: Individual shots with color coding (green for made, red for missed)
  - **Heatmap**: Shot density visualization with logarithmic scaling
- **Custom Court Rendering**: Accurate basketball court dimensions and markings
- **Real-time Statistics**: Comprehensive shooting statistics for both players
- **Live Data Integration**: Fresh data from NBA API on each comparison
- **Interactive UI**: Clean, intuitive interface with tabbed visualization modes

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/nba-shot-visualizer.git
   cd nba-shot-visualizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   The app will automatically open in your browser at `http://localhost:8501`

## 🎯 How to Use

1. **Select Season**: Choose an NBA season from the dropdown menu
2. **Enter Players**: Type the names of two NBA players you want to compare
3. **Click Compare**: Hit the "Compare" button to fetch and visualize shot data
4. **Explore Visualizations**: 
   - Switch between "Scatter" and "Heatmap" tabs
   - View detailed shooting statistics below the charts
5. **Analyze Patterns**: Compare shooting zones, accuracy, and shot selection

## 📊 What You'll See

### Scatter Plot View
- **Green dots**: Made shots
- **Red dots**: Missed shots
- **Court overlay**: Accurate NBA court dimensions with three-point lines and key

### Heatmap View
- **Color intensity**: Shot frequency (cool blues to hot yellows)
- **Logarithmic scale**: Better visualization of shooting hotspots
- **Side-by-side comparison**: Easy pattern comparison between players

### Statistics Panel
- Total shots attempted and made
- Field goal percentage (FG%)
- Three-point attempts and percentage (3P%)
- Real-time data from NBA API

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit for interactive web interface
- **Visualization**: Matplotlib for custom court rendering and shot plotting
- **Data Processing**: Pandas and NumPy for data manipulation
- **API Integration**: Direct HTTP requests to NBA Stats API

### Key Components
- `get_player_id()`: Resolves player names to NBA API IDs
- `get_shot_data()`: Fetches shot chart data for specific players/seasons
- `draw_court()`: Renders accurate basketball court with proper dimensions
- `plot_shots_scatter()`: Creates scatter plots with made/missed color coding
- `plot_shots_heatmap()`: Generates density heatmaps using hexagonal binning

## 🛠️ Development

### Project Structure
```
nba-shot-visualizer/
├── app.py              # Main application code
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .streamlit/        # Streamlit configuration
    └── config.toml    # Server settings
```

### Dependencies
- `streamlit>=1.28.0` - Web application framework
- `requests>=2.31.0` - HTTP client for NBA API
- `pandas>=2.0.0` - Data manipulation and analysis
- `numpy>=1.24.0` - Numerical computing
- `matplotlib>=3.7.0` - Plotting and visualization

## 📈 Features in Detail

### Real-time Data Integration
- Connects directly to NBA Stats API
- No caching - always fresh data
- Proper API headers for reliable access
- Comprehensive error handling

### Custom Court Visualization
- Accurate NBA court dimensions (94' x 50')
- Proper three-point line arc (23'9" from center)
- Free throw circle and lane markings
- Basket and center court circle

### Advanced Analytics
- Shot location analysis
- Shooting percentage breakdowns
- Three-point vs. two-point comparisons
- Visual pattern recognition

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NBA Stats API for providing comprehensive basketball data
- Streamlit team for the excellent web framework
- Basketball analytics community for inspiration

## 🐛 Troubleshooting

### Common Issues

**"Could not find player" error**:
- Check spelling of player names
- Try using more complete names (e.g., "LeBron James" instead of "LeBron")
- Ensure the player was active in the selected season

**API errors**:
- The NBA API occasionally experiences high traffic
- Try refreshing the page and attempting again
- Check your internet connection

**No shot data displayed**:
- Some players may have limited data for certain seasons
- Try different seasons or players with more playing time
   