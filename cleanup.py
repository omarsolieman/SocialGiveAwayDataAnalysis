import pandas as pd
import os

def advanced_clean_instagram_csv(input_filepath):
    """
    Performs an advanced cleaning on an Instagram data CSV.

    This script:
    1. Relabels columns to be human-readable.
    2. Removes true duplicate rows (where all columns are identical),
       keeping all unique entries, including comments with only tags.
    3. Reports detailed statistics on the cleaning process.

    Args:
        input_filepath (str): The path to the original, raw input CSV file.
    """
    # --- 1. Load the CSV File ---
    try:
        df = pd.read_csv(input_filepath)
        print(f"Successfully loaded '{input_filepath}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_filepath}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    # --- 2. Gather Initial Statistics ---
    original_rows = len(df)
    print("\n--- Initial Data Stats ---")
    print(f"Total rows before cleaning: {original_rows}")

    # --- 3. Rename Columns ---
    new_column_names = [
        'profile_url', 'profile_picture_url', 'username', 'post_comment_url',
        'time_elapsed', 'comment_text', 'mentioned_user_1_username', 'mentioned_user_1_url',
        'mentioned_user_2_username', 'mentioned_user_2_url', 'mentioned_user_3_username',
        'mentioned_user_3_url', 'action_type', 'extra_empty_column'
    ]
    if len(df.columns) == len(new_column_names):
        df.columns = new_column_names
        print("Columns successfully relabeled.")
    else:
        print("Warning: Column count mismatch. Renaming may be incorrect.")
        df.columns = new_column_names[:len(df.columns)]


    # --- 4. Advanced Duplicate Removal ---
    # A "duplicate" is defined as a row where every single column is
    # identical to another row. This safely removes scraping errors
    # without deleting legitimate multiple entries from the same user.
    print("\n--- Advanced Duplicate Removal ---")

    # Identify duplicates based on the entire row being identical.
    duplicates_mask = df.duplicated(keep='first')
    num_duplicates = duplicates_mask.sum()
    
    print(f"Found and removed {num_duplicates} identical duplicate rows.")
    
    # Keep only the first instance of each completely identical row
    df_cleaned = df[~duplicates_mask]
    
    # --- 5. Final Statistics ---
    cleaned_rows = len(df_cleaned)
    total_rows_removed = original_rows - cleaned_rows
    unique_participants = df_cleaned['username'].nunique()

    print(f"Total rows removed: {total_rows_removed}")
    print("\n--- Final Data Stats ---")
    print(f"Final number of valid entries: {cleaned_rows}")
    print(f"Total unique participants: {unique_participants}")

    # --- 6. Save the Cleaned Data ---
    output_filename = 'instagram_advanced_cleaned.csv'
    df_cleaned.to_csv(output_filename, index=False)
    print(f"\nAdvanced cleaned data has been saved to '{output_filename}'.")
    print("You can now use this file with the 'pick_winner.py' script.")


if __name__ == '__main__':
    # Use the original raw CSV file as input for this script.
    raw_csv_file = 'instagram.csv'

    if os.path.exists(raw_csv_file):
        advanced_clean_instagram_csv(raw_csv_file)
    else:
        print(f"Error: Could not find the input file '{raw_csv_file}'.")
        print("Please ensure the original CSV file is in the same folder.")

