import pandas as pd
import os

# Try to import plotting libraries. If they are not found, disable plotting.
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_ENABLED = True
except ImportError:
    PLOTTING_ENABLED = False

def analyze_giveaway_results(cleaned_filepath, winner_usernames):
    """
    Analyzes the results of a giveaway by providing detailed stats for a
    pre-defined list of winners, summary stats for non-winners, and visualizations.

    Args:
        cleaned_filepath (str): The path to the cleaned CSV file.
        winner_usernames (list): A list of the usernames that have already won.
    """
    # --- 1. Load and Process the Data ---
    try:
        df = pd.read_csv(cleaned_filepath)
        print(f"Successfully loaded '{cleaned_filepath}'.")
    except FileNotFoundError:
        print(f"Error: The file '{cleaned_filepath}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    if 'action_type' in df.columns:
        df['comment_likes'] = df['action_type'].str.extract('(\d+)').fillna(0).astype(int)
    else:
        df['comment_likes'] = 0

    valid_entries = df[
        df['mentioned_user_1_username'].notna() &
        df['mentioned_user_2_username'].notna() &
        df['mentioned_user_3_username'].notna()
    ].copy()

    if valid_entries.empty:
        print("\nCould not find any valid entries in the file.")
        return

    valid_entries['weight'] = valid_entries['comment_likes'] + 1
    user_total_weights = valid_entries.groupby('username')['weight'].sum()

    # --- 2. Separate Winners from Non-Winners ---
    all_participants = user_total_weights.index.tolist()
    valid_winners = [user for user in winner_usernames if user in all_participants]
    non_winners = [user for user in all_participants if user not in winner_usernames]

    # --- 3. Display Detailed Statistics for the Winners ---
    print("\n" + "="*50)
    print("--- Detailed Statistics for PRE-SELECTED Winners ---")
    
    winner_profiles = df[df['username'].isin(valid_winners)].drop_duplicates(subset=['username']).set_index('username')['profile_url']

    for i, username in enumerate(valid_winners):
        winner_stats = valid_entries[valid_entries['username'] == username]
        total_valid_comments = len(winner_stats)
        total_likes = winner_stats['comment_likes'].sum()
        total_score = user_total_weights.get(username, 0)
        profile_url = winner_profiles.get(username, "Profile URL not found")

        print(f"\n--- Winner #{i+1} ---")
        print(f"Username: {username}")
        print(f"Profile: {profile_url}")
        print(f"  - Total Valid Entries: {total_valid_comments}")
        print(f"  - Total Likes on Entries: {total_likes}")
        print(f"  - Final Winning Score: {total_score}")

    if len(valid_winners) < len(winner_usernames):
        print("\nNote: Some usernames from the provided winner list did not have valid entries and were excluded.")

    # --- 4. Display Summary Statistics for Non-Winners ---
    print("\n" + "="*50)
    print("--- Summary Statistics for Non-Winning Participants ---")
    
    non_winner_stats = valid_entries[valid_entries['username'].isin(non_winners)]
    if not non_winners:
        print("There were no other participants with valid entries.")
    else:
        total_non_winners = len(non_winners)
        total_entries = len(non_winner_stats)
        total_likes = non_winner_stats['comment_likes'].sum()

        print(f"Total non-winning participants with valid entries: {total_non_winners}")
        print(f"Total valid entries from non-winners: {total_entries}")
        print(f"Total likes on non-winners' entries: {total_likes}")
        if total_non_winners > 0:
            print(f"Average valid entries per non-winner: {total_entries / total_non_winners:.2f}")
            print(f"Average likes per non-winner: {total_likes / total_non_winners:.2f}")

    print("="*50)

    # --- 5. Generate and Save Visualizations ---
    if not PLOTTING_ENABLED:
        print("\n--- Visualizations ---")
        print("Plotting libraries (matplotlib, seaborn) not found.")
        print("To generate graphs, please install them by running: pip install matplotlib seaborn")
        print("="*50)
        return

    print("\n--- Generating Visualizations ---")
    sns.set_style("whitegrid")

    # Graph 1: Bar chart of winners' final scores
    winner_scores = user_total_weights[valid_winners].sort_values(ascending=False)
    plt.figure(figsize=(12, 7))
    sns.barplot(x=winner_scores.index, y=winner_scores.values, palette="viridis")
    plt.ylabel("Final Winning Score (Entries + Likes)")
    plt.xlabel("Winner Username")
    plt.title("Engagement Score of Each Winner")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("winner_scores.png")
    print("Saved winner scores graph to 'winner_scores.png'")

    # Graph 2: Comparison of Winners vs. Non-Winners
    winner_avg_entries = len(valid_entries[valid_entries['username'].isin(valid_winners)]) / len(valid_winners)
    winner_avg_likes = valid_entries[valid_entries['username'].isin(valid_winners)]['comment_likes'].sum() / len(valid_winners)

    non_winner_avg_entries = len(non_winner_stats) / len(non_winners) if non_winners else 0
    non_winner_avg_likes = non_winner_stats['comment_likes'].sum() / len(non_winners) if non_winners else 0

    plot_data = pd.DataFrame({
        'Group': ['Winners', 'Non-Winners', 'Winners', 'Non-Winners'],
        'Metric': ['Avg Entries', 'Avg Entries', 'Avg Likes', 'Avg Likes'],
        'Value': [winner_avg_entries, non_winner_avg_entries, winner_avg_likes, non_winner_avg_likes]
    })

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Metric', y='Value', hue='Group', data=plot_data, palette="mako")
    plt.ylabel("Average Count")
    plt.xlabel("")
    plt.title("Average Engagement: Winners vs. Non-Winners")
    plt.tight_layout()
    plt.savefig("group_comparison.png")
    print("Saved group comparison graph to 'group_comparison.png'")
    
    print("\nDisplaying graphs...")
    plt.show()


if __name__ == '__main__':
    pre_selected_winners = [
        "winner1", "winner2", "winner3", "winner4",
        "winner5", "winner6", "winner7", "winner8",
        "winner9", "winner10"
    ]
    cleaned_csv_file = 'instagram_advanced_cleaned.csv'

    if os.path.exists(cleaned_csv_file):
        analyze_giveaway_results(cleaned_csv_file, pre_selected_winners)
    else:
        print(f"Error: The required input file '{cleaned_csv_file}' was not found.")
        print("Please run the 'advanced_cleaner.py' script first.")

