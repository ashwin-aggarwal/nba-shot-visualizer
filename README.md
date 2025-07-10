# NBA Shot Visualizer

A Streamlit application that visualizes NBA player shot data with side-by-side comparisons.

## Features

- Select any NBA season from 2010-2023
- Compare two players' shot data side-by-side
- View scatter plots showing makes (green) and misses (red)
- Explore shot density with hexbin heatmaps
- See summary statistics including FG%, 3P%, and average shot distance

## Setup Instructions

1. Clone this repository:
   \`\`\`
   git clone https://github.com/yourusername/nba-shot-visualizer.git
   cd nba-shot-visualizer
   \`\`\`

2. Install the required dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

3. Get an API key from [API-NBA on RapidAPI](https://rapidapi.com/api-sports/api/api-nba)

4. Open `app.py` and replace `YOUR_API_KEY_HERE` with your actual API key:
   ```python
   API_KEY = "your_actual_api_key_here"
   \`\`\`

5. Run the Streamlit app:
   \`\`\`
   streamlit run app.py
   \`\`\`

6. Open your browser and navigate to the URL provided by Streamlit (typically http://localhost:8501)

## Usage

1. Select an NBA season from the dropdown menu
2. Enter the names of two NBA players you want to compare
3. Click the "Compare" button
4. Switch between "Scatter" and "Heatmap" tabs to view different visualizations

## Technical Details

- The application fetches player data from the API-NBA
- Shot data is processed using pandas
- Visualizations are created with matplotlib
- The court drawing function creates a realistic basketball court visualization
- Summary statistics are calculated and displayed below each visualization

## Note

This application requires an API key from RapidAPI to function. The free tier has limited requests, so be mindful of usage.

## License

MIT
