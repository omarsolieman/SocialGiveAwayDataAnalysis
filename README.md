# SocialGiveAwayDataAnalysis
# 📊 Project: Instagram Giveaway Analysis & Winner Selection Automation

## 🚀 Project Overview
This project involved cleaning, analyzing, and processing data from an Instagram giveaway to ensure a fair and data-driven winner selection process. The primary goal was to **automate the process of identifying valid entries, weighting them based on engagement (likes and multiple entries), and performing a post-giveaway analysis** to understand participant engagement.

---

## 🤯 The Challenge: Dirty Data
The initial dataset, exported from an Instagram scraping tool (`instagram.csv`), presented several challenges:

- **Cryptic Column Headers:** Columns were labeled with non-descriptive names (e.g., `x1i10hfl href`, `_ap3a`), making it difficult to understand the data.
- **Ambiguous "Likes" Data:** The number of likes on a comment was embedded in a text string like `"1 like"` or `"15 likes"` within an `action_type` column.
- **Defining a "Valid Entry":** The rules for winning (tagging at least 3 people) needed to be programmatically verified. Entries with only tags and no comment text were at risk of being incorrectly discarded.
- **Duplicate Entries:** The raw data contained numerous duplicate rows. A simple duplicate removal could unfairly penalize users who made multiple, legitimate entries.
- **Potential for Spam/Bot Activity:** Some users had an unusually high number of entries (e.g., over 150), requiring investigation to ensure they were not automated spam.

---

## 💡 My Solution: A Multi-Stage Python Scripting Process
I developed a series of **Python scripts** to create a repeatable and transparent workflow.

### 1. **Advanced Data Cleaning** (`advanced_cleaner.py`)
- **Relabeled Columns:** Renamed cryptic column names to descriptive ones like `username`, `comment_text`, and `mentioned_user_1_username`.
- **Intelligent Duplicate Removal:** Only removed rows that were 100% identical, preserving all legitimate multiple entries.
- **Handled Empty Comments:** Added logic to ensure comments containing only tags were considered valid.

### 2. **Fair Winner Selection** (`pick_winner.py`)
- **Identified Valid Entries:** Filtered the dataset to find all comments where at least **three unique users** were mentioned.
- **Weighted Chance System:** Calculated a *winning score* for each participant based on the sum of `1 + likes` for all their valid entries.
- **Multi-Winner Selection:** Configured the script to select **10 unique winners**.

### 3. **Post-Giveaway Analysis** (`analyze_giveaway.py`)
- **Generated Detailed Statistics:** Provided a breakdown of engagement metrics after winners were chosen.
- **Created Summary Tables:** Exported a clean summary of the 10 winners to a `.csv` file.
- **Spam/Bot Investigation:** Added a feature to flag users with exceptionally high entries and generate a report with comment samples for manual review.

---

## 💪 Key Challenges & How I Overcame Them
- **Challenge:** Incorrectly removing valid entries.  
  **Solution:** Iterated on the duplicate removal logic to only remove true scraping errors.
  
- **Challenge:** Extracting numerical "likes" from text.  
  **Solution:** Used Pandas `.str.extract()` with a regex to parse like counts.

- **Challenge:** Verifying a user with 160+ entries.  
  **Solution:** Built a high-volume analysis tool to create a report with timestamps and samples.

- **Challenge:** `UnicodeEncodeError` on some systems.  
  **Solution:** Removed emoji characters from print statements for script portability.

---

## ✨ Results & Visualizations
The scripts successfully:
- Cleaned the dataset.
- Selected **10 winners** based on a fair and weighted system.
- Generated a comprehensive analysis report.

### **Winner Engagement Comparison**
A chart was generated to visualize the final *winning score* for each of the 10 winners, highlighting engagement differences.

### **Winner Summary Table (Usernames Censored)**

| Username    | Total Valid Entries | Total Likes on Entries | Final Winning Score |
|-------------|----------------------|-------------------------|----------------------|
| Winner 1    | 162                 | 0                       | 162                 |
| Winner 2    | 129                 | 0                       | 129                 |
| Winner 3    | 75                  | 0                       | 75                  |
| Winner 4    | 10                  | 0                       | 10                  |
| Winner 5    | 10                  | 0                       | 10                  |
| Winner 6    | 4                   | 0                       | 4                   |
| Winner 7    | 3                   | 0                       | 3                   |
| Winner 8    | 2                   | 0                       | 2                   |
| Winner 9    | 2                   | 0                       | 2                   |
| Winner 10   | 1                   | 0                       | 1                   |

---

## 💻 Technologies Used
- **Python**
  - **Pandas:** For data manipulation, cleaning, and analysis.
  - **Matplotlib & Seaborn:** For data visualization and generating graphs.


