import logging
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import Buddy
from typing import List
from pydantic import BaseModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a Pydantic model for the buddy search request
class BuddySearchRequest(BaseModel):
    destination: str
    language: str
    keywords: str
    event: str
    package: str

# Function to match buddies based on user criteria
def match_buddies(db: Session, request: BuddySearchRequest) -> List[Buddy]:
    logger.info("Starting the matching process for request: %s", request)

    # Initial query: Filter by destination and language first (top priority)
    query = db.query(Buddy).filter(
        Buddy.destination.ilike(f"%{request.destination}%"),
        Buddy.language.ilike(f"%{request.language}%")
    )
    logger.info("Filtered by destination and language: %s", query)

    # If keywords are provided, add a filter for partial matches
    if request.keywords:
        keywords = request.keywords.lower().split(",")
        keyword_filters = [Buddy.keywords.ilike(f"%{keyword.strip()}%") for keyword in keywords]
        query = query.filter(or_(*keyword_filters))
        logger.info("Added keyword filters: %s", keyword_filters)

    # If event is provided, add a filter for partial match (case insensitive)
    if request.event:
        query = query.filter(Buddy.event.ilike(f"%{request.event}%"))
        logger.info("Added event filter for: %s", request.event)

    # If package is provided, add a filter for partial match (case insensitive)
    if request.package:
        query = query.filter(Buddy.package.ilike(f"%{request.package}%"))
        logger.info("Added package filter for: %s", request.package)

    # Execute the query and fetch all results
    results = query.all()
    logger.info("Query executed. Number of results found: %d", len(results))

    # Apply scoring based on prioritization criteria
    scored_buddies = []
    for buddy in results:
        score = 0
        # Priority 1: Destination match
        if request.destination.lower() in buddy.destination.lower():
            score += 50
        # Priority 2: Language match
        if request.language.lower() in buddy.language.lower():
            score += 30
        # Priority 3: Keyword match (if applicable)
        if request.keywords:
            for keyword in keywords:
                if keyword.strip() in buddy.keywords.lower():
                    score += 10
                    break  # Stop after the first matching keyword
        # Priority 4: Event match (if applicable)
        if request.event and request.event.lower() in buddy.event.lower():
            score += 5
        # Priority 5: Package match (if applicable)
        if request.package and request.package.lower() in buddy.package.lower():
            score += 5

        scored_buddies.append((buddy, score))
        logger.debug("Buddy: %s scored %d", buddy.name, score)

    # Sort the buddies by score in descending order
    scored_buddies.sort(key=lambda x: x[1], reverse=True)
    logger.info("Buddies sorted by score. Top match: %s", scored_buddies[0][0].name if scored_buddies else "None")

    # Return the sorted buddy objects (ignoring the score)
    return [buddy for buddy, score in scored_buddies]
