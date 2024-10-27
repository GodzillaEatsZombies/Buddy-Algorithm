import pandas as pd
import logging
from sklearn.model_selection import train_test_split

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load buddy profiles and test scenarios
def load_data():
    try:
        buddy_profiles = pd.read_excel("Dummy-Buddy-Profiles-Batch1.xlsx")
        test_scenarios = pd.read_excel("Buddy-Matching-Test-Scenarios.xlsx")
        logger.info("Loaded buddy profiles and test scenarios successfully.")
        return buddy_profiles, test_scenarios
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise

# Data Transformation
def preprocess_data(buddy_profiles):
    buddy_profiles_expanded = buddy_profiles.copy()
    return buddy_profiles_expanded

# Split dataset into training and testing sets (80/20 split)
def split_data(buddy_profiles_expanded):
    return train_test_split(buddy_profiles_expanded, test_size=0.2, random_state=42)

# Helper function to retrieve synonyms (simplified example)
def get_synonyms(keyword):
    synonyms = {
        "weed": ["420 friendly", "cannabis"],
        "music": ["nightlife", "concert"]
        # Add more synonym mappings here if needed
    }
    return synonyms.get(keyword, [keyword])

# Define the matching function
def find_best_buddies(request, profiles):
    matching_scores = []
    for idx, profile in profiles.iterrows():
        score = 0
        
        # Scoring based on each field in the request (simplified)
        if request['destination'] == profile.get('Destination'):
            score += 20
        if request['language'] == profile.get('User Language'):
            score += 20
        if request['local_language'] == profile.get('Local Language'):
            score += 20
        
        # Handling NaN values in 'Keywords' and scoring based on keywords
        request_keywords = str(request['keywords']).split(',') if pd.notna(request['keywords']) else []
        profile_keywords = str(profile.get('Keywords', '')).split(',') if pd.notna(profile.get('Keywords')) else []
        
        for keyword in request_keywords:
            if keyword in profile_keywords:
                score += 20
        
        if request['event'] == profile.get('Event'):
            score += 10
        if request['package'] == profile.get('Package'):
            score += 10
        
        matching_scores.append((idx, score))

    # Sort by score in descending order and pick the top matches
    top_matches = sorted(matching_scores, key=lambda x: x[1], reverse=True)[:5]
    return [idx for idx, score in top_matches]

# Main function to process each scenario and log results
def evaluate_metrics(test_scenarios, profiles):
    metrics_log = []
    for i, request in test_scenarios.iterrows():
        try:
            logger.info(f"Processing scenario {i + 1} with request: {request.to_dict()}")
            top_buddies_indices = find_best_buddies(request, profiles)
            detailed_top_buddies = profiles.loc[top_buddies_indices]

            # Log the scenario results for metrics tracking
            top_buddy_scores = [score for idx, score in enumerate(top_buddies_indices)]
            metrics_log.append({
                "Scenario": i + 1,
                "Data Size": len(top_buddies_indices),
                "Top Buddy Scores": top_buddy_scores,
            })
            
            # Display top matching buddies for each scenario
            display_columns = ["Buddy_id", "Destination", "User Language", "Local Language", "Keywords", "Event", "Package"]
            print(f"\nTop Matching Buddies for Scenario {i + 1} (Detailed View):")
            try:
                print(detailed_top_buddies[display_columns])
            except KeyError as e:
                logger.warning(f"Error displaying detailed columns: {e}")
                print("Available columns in buddy profiles:", detailed_top_buddies.columns.tolist())

        except Exception as e:
            logger.error(f"Error processing scenario {i + 1}: {e}")

    # Convert metrics log to DataFrame for review
    metrics_df = pd.DataFrame(metrics_log)
    print("\nPerformance Metrics for Test Scenarios:")
    print(metrics_df)
    return metrics_df

# Save metrics to CSV
def save_metrics_to_csv(metrics_df, output_file="buddy_matching_metrics.csv"):
    try:
        if not os.path.exists(output_file):
            metrics_df.to_csv(output_file, index=False)
        else:
            metrics_df.to_csv(output_file, mode='a', header=False, index=False)
        logger.info(f"Metrics successfully saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving metrics: {e}")

# Main function to run the entire process
def main():
    buddy_profiles, test_scenarios = load_data()
    buddy_profiles_expanded = preprocess_data(buddy_profiles)
    
    # Split into train and test set
    train_profiles, test_profiles = split_data(buddy_profiles_expanded)
    
    # Process scenarios and log metrics cumulatively
    metrics_log = evaluate_metrics(test_scenarios, train_profiles)
    
    # Save cumulative metrics to CSV
    save_metrics_to_csv(metrics_log)

# Run the main function
if __name__ == "__main__":
    main()

    