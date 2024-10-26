import pandas as pd
import logging
from sklearn.model_selection import train_test_split

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load buddy profiles and test scenarios
try:
    buddy_profiles = pd.read_excel("Dummy-Buddy-Profiles-Batch1.xlsx")
    test_scenarios = pd.read_excel("Buddy-Matching-Test-Scenarios.xlsx")
    logger.info("Loaded buddy profiles and test scenarios successfully.")
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    raise

# Data Transformation
buddy_profiles_expanded = buddy_profiles.copy()

# Split dataset into training and testing sets (80/20 split)
train_profiles, test_profiles = train_test_split(buddy_profiles_expanded, test_size=0.2, random_state=42)

# Helper function to retrieve synonyms (simplified example)
def get_synonyms(keyword):
    synonyms = {
        "weed": ["420 friendly", "cannabis"],
        "music": ["nightlife", "concert"]
        # Add more synonym mappings here
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
        if any(keyword in profile.get('Keywords', '').split(',') for keyword in request['keywords'].split(',')):
            score += 20
        if request['event'] == profile.get('Event'):
            score += 10
        if request['package'] == profile.get('Package'):
            score += 10
        matching_scores.append((idx, score))
    
    # Sort by score in descending order and pick the top matches
    top_matches = sorted(matching_scores, key=lambda x: x[1], reverse=True)[:5]
    return [idx for idx, score in top_matches]

# Initialize the metrics log
metrics_log = []

# Process each test scenario
for i, request in test_scenarios.iterrows():
    try:
        logger.info(f"Processing scenario {i + 1} with request: {request.to_dict()}")

        # Find matching buddies for the scenario
        top_buddies_indices = find_best_buddies(request, buddy_profiles_expanded)
        detailed_top_buddies = buddy_profiles_expanded.loc[top_buddies_indices]

        # Log the top buddy scores for metrics tracking
        top_buddy_scores = [score for idx, score in enumerate(top_buddies_indices)]
        metrics_log.append({
            "Scenario": i + 1,
            "Data Size": len(top_buddies_indices),
            "Top Buddy Scores": top_buddy_scores
        })

        # Display top matching buddies for each scenario
        print(f"\nTop Matching Buddies for Scenario {i + 1} (Detailed View):")
        display_columns = ["Buddy_id", "Destination", "User Language", "Local Language", "Keywords", "Event", "Package"]
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
