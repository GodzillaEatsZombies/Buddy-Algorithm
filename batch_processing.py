# Import necessary libraries
import pandas as pd
import logging
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the buddy-matching function
def find_best_buddies(request, df):
    logger.info("Starting buddy matching with request: %s", request)
    
    scored_buddies = []
    for index, buddy in df.iterrows():
        score = 0
        if buddy.get(f'Dest_{request["destination"]}', False):
            score += 50
        if buddy.get(f'UserLang_{request["language"]}', False):
            score += 30
        if buddy.get(f'LocalLang_{request["local_language"]}', False):
            score += 20
        if any(buddy.get(f'Event_{event.strip()}', False) for event in request["keywords"].split(',')):
            score += 10
        if buddy.get(f'Package_{request["package"]}', False):
            score += 5
        if score > 0:
            scored_buddies.append((index, score))
    
    scored_buddies.sort(key=lambda x: x[1], reverse=True)
    top_buddies = scored_buddies[:5]
    
    logger.info("Top 5 matching buddies found.")
    for idx, (buddy_index, score) in enumerate(top_buddies, start=1):
        logger.info("Buddy index: %d, Score: %d", buddy_index, score)
    
    return [index for index, _ in top_buddies]

# Function to process each batch and save results
def process_batch(df, request, y_true=None):
    # Find top buddies based on the request
    top_buddies_indices = find_best_buddies(request, df)
    detailed_top_buddies = df.loc[top_buddies_indices]
    
    # Dynamically select relevant columns to display
    display_columns = [
        f'Dest_{request["destination"]}',
        f'UserLang_{request["language"]}',
        f'LocalLang_{request["local_language"]}',
        f'Event_{request["event"]}',
        f'Package_{request["package"]}'
    ]
    display_columns = [col for col in display_columns if col in detailed_top_buddies.columns]
    
    # Save the top matching buddies to a CSV
    try:
        detailed_top_buddies[display_columns].to_csv("top_matching_buddies.csv", index=False)
        logger.info("Top matching buddies have been saved to 'top_matching_buddies.csv'.")
    except Exception as e:
        print("Error saving top buddies to CSV:", e)

    # If there is a ground truth provided, calculate metrics
    if y_true is not None:
        y_pred = [1 if i in top_buddies_indices else 0 for i in range(len(df))]
        
        # Compute metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=1)
        recall = recall_score(y_true, y_pred, zero_division=1)
        f1 = f1_score(y_true, y_pred, zero_division=1)
        
        logger.info("Batch Metrics - Accuracy: %.2f, Precision: %.2f, Recall: %.2f, F1 Score: %.2f",
                    accuracy, precision, recall, f1)

# Sample request
request = {
    "destination": "Paris",
    "language": "English",
    "local_language": "French",
    "keywords": "food,history",
    "event": "Art Exhibit",
    "package": "Shopping Enthusiast"
}

# Load the entire dataset
file_path = 'ML_Training_Dataset_500.xlsx'
full_df = pd.read_excel(file_path)

# 80/20 train-test split
train_df, test_df = train_test_split(full_df, test_size=0.2, random_state=42)

# Example ground truth (replace with actual labels if available)
y_true_train = [1 if i < len(train_df) // 2 else 0 for i in range(len(train_df))]  # Dummy example
y_true_test = [1 if i < len(test_df) // 2 else 0 for i in range(len(test_df))]    # Dummy example

# Process the training and test sets
logger.info("Processing training set:")
process_batch(train_df, request, y_true_train)

logger.info("Processing test set:")
process_batch(test_df, request, y_true_test)
