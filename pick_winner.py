import pandas as pd
import os
import random

def pick_giveaway_winners(cleaned_filepath):
    """
    Picks 10 random winners from a cleaned Instagram comments CSV.

    The criteria for winning are:
    1. Each entry must tag at least 3 other users to be valid.
    2. A user's total chance of winning is the sum of the weights of all their valid comments.
    3. The weight for a single comment is (1 + number of likes).
    4. A user can only win once.

    Args:
        cleaned_filepath (str): The path to the cleaned CSV file.
    """
    # --- 1. Load the Cleaned CSV File ---
    try:
        df = pd.read_csv(cleaned_filepath)
        print(f"Successfully loaded '{cleaned_filepath}'.")
    except FileNotFoundError:
        print(f"Error: The file '{cleaned_filepath}' was not found.")
        print("Please run the 'advanced_cleaner.py' script first to generate this file.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    # --- 2. Process Comment Likes from 'action_type' Column ---
    if 'action_type' in df.columns:
        print("\nFound 'action_type' column. Processing it for comment likes...")
        df['comment_likes'] = df['action_type'].str.extract('(\d+)').fillna(0).astype(int)
        print("Successfully extracted like counts.")
    else:
        print("\nWarning: 'action_type' column not found. Defaulting likes to 0.")
        df['comment_likes'] = 0

    print(f"\nTotal comments to analyze: {len(df)}")

    # --- 3. Filter for Valid Entries ---
    # A valid entry must tag at least three users.
    valid_entries = df[
        df['mentioned_user_1_username'].notna() &
        df['mentioned_user_2_username'].notna() &
        df['mentioned_user_3_username'].notna()
    ].copy()

    if valid_entries.empty:
        print("\nCould not find any valid entries that meet the criteria (at least 3 tags).")
        print("Winner selection cannot proceed.")
        return

    # --- 4. Calculate Weights and Aggregate by User ---
    print("\nCalculating total winning chance for each participant...")
    # Calculate the weight for each individual entry.
    valid_entries['weight'] = valid_entries['comment_likes'] + 1

    # Group by username and sum their weights to get a total score for each person.
    user_total_weights = valid_entries.groupby('username')['weight'].sum()

    print(f"Total unique participants with valid entries: {len(user_total_weights)}")

    # --- 5. Pick 10 Winners ---
    num_winners_to_pick = 10
    if len(user_total_weights) < num_winners_to_pick:
        print(f"\nWarning: There are fewer than {num_winners_to_pick} participants ({len(user_total_weights)}).")
        print(f"Picking all {len(user_total_weights)} participants as winners.")
        num_winners_to_pick = len(user_total_weights)

    if num_winners_to_pick == 0:
        print("No eligible participants to pick from.")
        return

    print(f"\nPicking {num_winners_to_pick} winners based on their total entries and likes...")

    # Sample from the user list, weighted by their total score.
    # `replace=False` ensures a user cannot be picked more than once.
    winning_users_series = user_total_weights.sample(
        n=num_winners_to_pick, weights=user_total_weights, replace=False
    )
    winning_usernames = winning_users_series.index.tolist()

    # --- 6. Announce the Winners ---
    print("\n" + "="*50)
    print(f"AND THE {num_winners_to_pick} WINNERS ARE...")

    # Get profile URLs for the winners for easy reference
    winner_profiles = df[df['username'].isin(winning_usernames)].drop_duplicates(subset=['username']).set_index('username')['profile_url']

    for i, username in enumerate(winning_usernames):
        profile_url = winner_profiles.get(username, "Profile URL not found")
        print(f"\n--- Winner #{i+1} ---")
        print(f"Username: {username}")
        print(f"Profile: {profile_url}")

    print("\n\nCongratulations to all the winners!")
    print("="*50)


if __name__ == '__main__':
    # This script uses the output from the cleaner script.
    cleaned_csv_file = 'instagram_advanced_cleaned.csv'

    if os.path.exists(cleaned_csv_file):
        pick_giveaway_winners(cleaned_csv_file)
    else:
        print(f"Error: The required input file '{cleaned_csv_file}' was not found.")
        print("Please run the 'advanced_cleaner.py' script first.")

