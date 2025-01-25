import pandas as pd
import re

# Function to parse PGN file and extract game data
def parse_pgn(file_path):
    with open(file_path, 'r') as file:
        pgn_data = file.read()

    # Split the content into individual games
    games = pgn_data.strip().split('\n\n')

    # Lists to store parsed data
    data = []

    # Regex for metadata and moves
    metadata_pattern = re.compile(r'\[(.*?)\s"(.*?)"\]')
    moves_pattern = re.compile(r'(\d+\.\s[^\d\s].*?)(?=\s\d+\.|$)')

    for game in games:
        metadata_matches = metadata_pattern.findall(game)
        moves_match = moves_pattern.findall(game)

        # Create a dictionary for game metadata
        game_data = {key: value for key, value in metadata_matches}

        # Extract and clean the first 5 full move pairs
        for i in range(5):
            if i < len(moves_match):
                move_pair = moves_match[i].strip()
                game_data[f'Move_{i+1}'] = move_pair
            else:
                game_data[f'Move_{i+1}'] = None

        # Add total number of moves
        game_data['Total_Moves'] = len(moves_match)

        data.append(game_data)

    # Create a DataFrame from the parsed data
    df = pd.DataFrame(data)

    # Ensure consistent column naming
    df.columns = [col.strip() for col in df.columns]

    return df


# Path to your PGN file
file_path = '/Users/avishnu/Desktop/chess_ajay.pgn'

# Parse the PGN file and create a dataset
dataset = parse_pgn(file_path)

# Display the dataset
print(dataset.head())

# Save the dataset to a CSV for further analysis
dataset.to_csv('/Users/avishnu/Desktop/chess_ajay_dataset.csv', index=False)