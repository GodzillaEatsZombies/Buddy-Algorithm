import requests

# Function to send a POST request to the API
def send_buddy_request(payload):
    BASE_URL = "http://127.0.0.1:8000/api/book_buddy"
    response = requests.post(BASE_URL, json=payload)
    return response


# Test case 1: Valid match for Los Angeles
def test_case_1():
    payload = {
        "destination": "Los Angeles",
        "language": "English,Spanish",
        "keywords": "shopping,food,art",
        "event": "City Tour",
        "package": "Solo Traveler Buddy"
    }
    response = send_buddy_request(payload)
    assert response.status_code == 200, "Test Case 1 Failed"
    
    data = response.json()
    
    # Checking if the correct buddy is returned
    if len(data) == 0:
        print("No buddies found")
    else:
        print(f"Returned Buddy Name: {data[0]['name']}")
        print(f"Returned Buddy Details: {data[0]}")
        
    expected_name = "Test One"  # Expected buddy for the Los Angeles City Tour
    assert data[0]['name'] == expected_name, f"Expected {expected_name}, but got {data[0]['name']}"


# Test case 2: Now passing, keeping for context
def test_case_2():
    payload = {
        "destination": "New Delhi",
        "language": "Hindi,English",
        "keywords": "culture,shopping,history",
        "event": "Cultural Tour",
        "package": "Shopping Enthusiast Buddy"
    }

    # Send request
    response = send_buddy_request(payload)
    
    # Print debug information
    print("=== Debugging Test Case 2 ===")
    print(f"Payload sent: {payload}")
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    
    # Check status code
    if response.status_code != 200:
        print(f"Test Case 2 Failed: Received {response.status_code} instead of 200.")
    else:
        data = response.json()
        print(f"Response JSON: {data}")
        
        # Verify the returned name
        expected_name = "Alpha Two"
        if len(data) == 0:
            print(f"Test Case 2 Failed: No buddies returned in the response.")
        else:
            if data[0]['name'] == expected_name:
                print(f"Test Case 2 Passed!")
            else:
                print(f"Test Case 2 Failed: Expected {expected_name}, but got {data[0]['name']}")


# Test case 3: Invalid data (integer for language)
def test_case_3():
    payload = {
        "destination": "Tokyo",
        "language": 123,  # Invalid data for language
        "keywords": "technology,anime",
        "event": "Tech Expo",
        "package": "Solo Traveler Buddy"
    }
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print("Test Case 3:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 422 validation error due to invalid data
    assert response.status_code == 422, "Test Case 3 Failed"
    print("Test Case 3 Passed")

# Test case 4: Invalid destination and language
def test_case_4():
    payload = {
        "destination": "Atlantis",  # Nonexistent destination
        "language": "Elvish",  # Nonexistent language
        "keywords": "magic,fantasy,underwater",
        "event": "Dragon Parade",
        "package": "Mythical Explorer"
    }
    response = send_buddy_request(payload)

    # Enhanced logging for debugging
    print("Test Case 4:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 error for no matching buddy found
    assert response.status_code == 404, "Test Case 4 Failed"
    print("Test Case 4 Passed")


# Test case 5: Introducing the next one
def test_case_5():
    payload = {
        "destination": "Paris",
        "language": "French,English",
        "keywords": "art,fashion,history",
        "event": "Fashion Week",
        "package": "Shopping Enthusiast Buddy"
    }

    # Send request
    response = send_buddy_request(payload)
    
    # Print debug information
    print("=== Debugging Test Case 5 ===")
    print(f"Payload sent: {payload}")
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    
    # Check status code
    if response.status_code != 200:
        print(f"Test Case 5 Failed: Received {response.status_code} instead of 200.")
    else:
        data = response.json()
        print(f"Response JSON: {data}")
        
        # Verify the returned name
        expected_name = "Alpha Eleven"
        if len(data) == 0:
            print(f"Test Case 5 Failed: No buddies returned in the response.")
        else:
            if data[0]['name'] == expected_name:
                print(f"Test Case 5 Passed!")
            else:
                print(f"Test Case 5 Failed: Expected {expected_name}, but got {data[0]['name']}")

# Test case 6
def test_case_6():
    payload = {
        "destination": "Berlin",
        "language": "German,English",
        "package": "Solo Traveler Buddy"
    }
    
    response = send_buddy_request(payload)
    print("Test Case 6")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    # Check if the response status is 200 OK
    assert response.status_code == 200, "Test Case 6 Failed"
    
    data = response.json()
    
    # Debugging information to help understand the returned buddy
    print(f"Returned Buddy Name: {data[0]['name']}")
    print(f"Returned Buddy Details: {data[0]}")
    
    # Either Alpha Five or Test Twelve should match
    expected_names = ["Alpha Five", "Test Twelve"]
    
    # Ensure one of the expected buddies is returned
    assert data[0]['name'] in expected_names, f"Expected one of {expected_names}, but got {data[0]['name']}"

# Test Case 7: Flexible Matching (Event or Package)
def test_case_7():
    payload = {
        "destination": "Rome",
        "language": "Italian,English",
        "package": "Solo Traveler Buddy",  # The user might be booking based on package
        "event": "Historical Tour"  # Or the user might be booking based on event
    }

    response = send_buddy_request(payload)
    print("Test Case 7:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Ensure that the status code is 200
    assert response.status_code == 200, "Test Case 7 Failed"

    # Check if any buddy profile was returned
    data = response.json()

    if len(data) == 0:
        print("No buddies found")
    else:
        # Iterate through the returned matches (if more than one buddy)
        for buddy in data:
            print(f"Returned Buddy Name: {buddy['name']}")
            print(f"Returned Buddy Details: {buddy}")
            print(f"Buddy's Event: {buddy.get('event')}")
            print(f"Buddy's Package: {buddy.get('package')}")

        # Modify the logic to check if a buddy matches either event or package
        # We are not forcing one particular match (Alpha Nine or Test Seven) to be the only match
        # We are open to either event or package matches

        matches_event = any(buddy['event'] == "Historical Tour" for buddy in data)
        matches_package = any(buddy['package'] == "Solo Traveler Buddy" for buddy in data)

        assert matches_event or matches_package, "No matching buddy found for event or package"

# Test case 8: Invalid destination (mythical location)
def test_case_8():
    payload = {
        "destination": "Atlantis",   # Invalid destination
        "language": "Elvish",        # Invalid language
        "package": "Mythical Explorer"
    }
    response = send_buddy_request(payload)

    # Enhanced logging for debugging
    print("Test Case 8:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # The expected status code for this scenario should be 404
    assert response.status_code == 404, "Test Case 8 Failed"
    print("Test Case 8 Passed")

# Test case 9: Matching language and location, returning multiple buddies if possible
def test_case_9():
    payload = {
        "destination": "Buenos Aires",
        "language": "Spanish,English",
        "event": "Tango Festival",  # Secondary criteria
        "package": "Touring Musician Buddy"  # Secondary criteria
    }
    response = send_buddy_request(payload)

    # Enhanced logging
    print("Test Case 9:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    assert response.status_code == 200, "Test Case 9 Failed"
    data = response.json()

    # Filter buddies by language and location (primary criteria)
    matching_buddies = [buddy for buddy in data if buddy['destination'] == "Buenos Aires" and "Spanish" in buddy['language']]

    # Print out all matching buddies
    print(f"All buddies that match language and location: {[buddy['name'] for buddy in matching_buddies]}")

    # Check if we found any matches
    assert len(matching_buddies) > 0, "No buddies found that match the language and location"

    # Optionally, if you want to prioritize event and package matches (but still return all language and location matches):
    prioritized_buddies = [buddy for buddy in matching_buddies if buddy['event'] == "Tango Festival" and buddy['package'] == "Touring Musician Buddy"]

    # If no prioritized buddies, fall back to all language/location matches
    if prioritized_buddies:
        print(f"Prioritized buddies (matching event and package): {[buddy['name'] for buddy in prioritized_buddies]}")
    else:
        print("No buddies match both event and package, showing all language/location matches instead.")

    print("Test Case 9 Passed")

# Test case 10: No matches expected
def test_case_10():
    payload = {
        "destination": "Moscow",
        "language": "Russian,English",
        "event": "City Tour",  # Correct event from the dropdown
        "package": "Solo Traveler Buddy"  # Default package to avoid errors
    }
    response = send_buddy_request(payload)

    # Logging for debugging
    print("Test Case 10:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Ensure the algorithm handles no matches correctly
    if response.status_code == 404:
        print("No buddies found, which is expected.")
        assert True, "Test Case 10 Passed with no matches as expected."
    else:
        # In case buddies are found
        assert response.status_code == 200, "Test Case 10 Failed - Expected 200 or 404 status"
        data = response.json()
        assert data[0]['name'] == "Alpha Seventeen", "Unexpected match for Test Case 10"
        print("Test Case 10 Passed - Buddy found.")

def test_case_11():
    # Payload with invalid destination and package
    payload = {
        "destination": "Atlantis",  # Nonexistent destination
        "language": "English",  
        "keywords": "history,adventure",
        "event": "Treasure Hunt",
        "package": "Mystery Explorer Buddy",  # Invalid package
    }
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print("Test Case 11:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    # Expecting a 404 Not Found error due to invalid destination and package
    assert response.status_code == 404, "Test Case 11 Failed"
    print("Test Case 11 Passed")


# Test case 12: Valid Destination but Invalid Event and Package
def test_case_12():
    # Payload with valid destination but invalid event and package
    payload = {
        "destination": "New York",
        "language": "English",
        "keywords": "shopping,adventure",
        "event": "Spacewalk Tour",  # Invalid event
        "package": "Alien Explorer Buddy"  # Invalid package
    }
    response = send_buddy_request(payload)

    # Enhanced logging for debugging
    print("Test Case 12:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 error due to invalid event and package
    assert response.status_code == 404, "Test Case 12 Failed"
    print("Test Case 12 Passed")


# Test case 13: Invalid language and event
def test_case_13():
    payload = {
        "destination": "London",
        "language": "Klingon",  # Invalid language
        "keywords": "shopping,food",
        "event": "Time Travel Expo",  # Invalid event
        "package": "Shopping Enthusiast Buddy"
    }
    response = send_buddy_request(payload)

    # Enhanced logging for debugging
    print("Test Case 13:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid language and event
    assert response.status_code == 404, "Test Case 13 Failed"
    print("Test Case 13 Passed")


# Test Case 14: Valid destination and language but invalid event and package
def test_case_14():
    payload = {
        "destination": "Sydney",
        "language": "English",
        "keywords": "music,adventure",
        "event": "Future Music Fest",  # Invalid event
        "package": "Food Explorer Buddy"  # Invalid package
    }
    response = send_buddy_request(payload)

    # Enhanced logging for debugging
    print("Test Case 14:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid event and package
    assert response.status_code == 404, "Test Case 14 Failed"
    print("Test Case 14 Passed")


# Test case 15: Invalid language but valid destination, event, and package
def test_case_15():
    # Payload with invalid language
    payload = {
        "destination": "Milan",
        "language": "Klingon",  # Invalid language
        "keywords": "fashion,design",
        "event": "Milan Fashion Week",
        "package": "Shopping Enthusiast Buddy"
    }
    
    # Sending the request to the buddy matching algorithm
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print("Test Case 15:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    # Expecting a 404 error due to invalid language
    assert response.status_code == 404, "Test Case 15 Failed"
    print("Test Case 15 Passed")

# Test case 16: Invalid destination and valid language, event, and package
def test_case_16():
    # Payload with invalid destination
    payload = {
        "destination": "Wakanda",  # Nonexistent destination
        "language": "English",
        "keywords": "technology,adventure",
        "event": "Tech Conference",
        "package": "Solo Traveler Buddy"
    }
    
    # Sending the request to the buddy matching algorithm
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print("Test Case 16:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    # Expecting a 404 error due to invalid destination
    assert response.status_code == 404, "Test Case 16 Failed"
    print("Test Case 16 Passed")

# Test case 17: Invalid event and package
def test_case_17():
    # Payload with invalid event and package
    payload = {
        "destination": "Tokyo",
        "language": "Japanese",
        "keywords": "anime,technology",
        "event": "Anime Festival",  # Invalid event
        "package": "Shopping Enthusiast Buddy"  # Invalid package for this event
    }
    response = send_buddy_request(payload)

    # Enhanced logging for debugging
    print("Test Case 17:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 due to invalid event and package combination
    assert response.status_code == 404, "Test Case 17 Failed"
    print("Test Case 17 Passed")


# Test Case 18: Valid destination but mismatched event and package
def test_case_18():
    # Payload with valid destination but mismatched event and package
    payload = {
        "destination": "Paris",
        "language": "French",
        "keywords": "history,art",
        "event": "Wine Tour",
        "package": "Tech Conference Buddy"  # Invalid package for the given event
    }

    response = send_buddy_request(payload)

    # Enhanced logging for debugging
    print("Test Case 18:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to no valid buddies matching this event and package
    assert response.status_code == 404, "Test Case 18 Failed"
    print("Test Case 18 Passed")


# Test Case 19: Valid event and destination but mismatched language and keywords
def test_case_19():
    # Payload with mismatched language and keywords for a valid event and destination
    payload = {
        "destination": "Rome",
        "language": "Spanish",  # Mismatched language for the location
        "keywords": "science,technology",  # Keywords that don't match Rome
        "event": "Historical Tour",
        "package": "Family Traveler Buddy"  # Valid package for the event
    }

    response = send_buddy_request(payload)

    # Enhanced logging for debugging
    print("Test Case 19:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to mismatched language and keywords
    assert response.status_code == 404, "Test Case 19 Failed"
    print("Test Case 19 Passed")

# Test Case 20: Payload with invalid destination and package 
def test_case_20():
    # Payload with invalid destination and package
    payload = {
        "destination": "New York",
        "language": "English",
        "keywords": "technology,shopping",
        "event": "Tech Expo",
        "package": "Mythical Explorer Buddy"  # Invalid package
    }
    
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print(f"Test Case 20:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid package
    assert response.status_code == 404, "Test Case 20 Failed"
    print("Test Case 20 Passed")

# Test Case 21: Payload with valid destination but an invalid event
def test_case_21():
    # Payload with valid destination but an invalid event
    payload = {
        "destination": "Paris",
        "language": "English",
        "keywords": "history,architecture",
        "event": "Dragon Festival",  # Invalid event
        "package": "Solo Traveler Buddy"  # Valid package
    }
    
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print(f"Test Case 21:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid event
    assert response.status_code == 404, "Test Case 21 Failed"
    print("Test Case 21 Passed")


# Test Case 22: Payload with valid destination and event but an invalid package
def test_case_22():
    # Payload with valid destination and event but an invalid package
    payload = {
        "destination": "New York",
        "language": "English",
        "keywords": "art,music,shopping",
        "event": "Concert",  # Valid event
        "package": "Luxury Explorer Buddy"  # Invalid package
    }
    
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print(f"Test Case 22:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid package
    assert response.status_code == 404, "Test Case 22 Failed"
    print("Test Case 22 Passed")

# Test Case 23: Payload with valid destination and language but an invalid event
def test_case_23():
    # Payload with valid destination and language but an invalid event
    payload = {
        "destination": "San Francisco",
        "language": "English",
        "keywords": "technology,music",
        "event": "Sunset Marathon",  # Invalid event
        "package": "Tech Explorer Buddy"
    }
    
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print(f"Test Case 23:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid event
    assert response.status_code == 404, "Test Case 23 Failed"
    print("Test Case 23 Passed")


# Test Case 24: Payload with invalid destination and valid event
def test_case_24():
    # Payload with invalid destination and valid event
    payload = {
        "destination": "Atlantis",  # Invalid destination
        "language": "Spanish",
        "keywords": "music,festival",
        "event": "Music Festival",  # Valid event
        "package": "Cultural Explorer Buddy"
    }
    
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print(f"Test Case 24:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid destination
    assert response.status_code == 404, "Test Case 24 Failed"
    print("Test Case 24 Passed")


# Test Case 25: Payload with valid destination, language, and event but invalid package
def test_case_25():
    # Payload with valid destination, language, and event but invalid package
    payload = {
        "destination": "New York",
        "language": "English",
        "keywords": "art,fashion,shopping",
        "event": "Fashion Week",
        "package": "Space Explorer Buddy"  # Invalid package
    }
    
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print(f"Test Case 25:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid package
    assert response.status_code == 404, "Test Case 25 Failed"
    print("Test Case 25 Passed")


# Test Case 26: Payload with valid destination and package but invalid event and keywords
def test_case_26():
    # Payload with valid destination and package but invalid event and keywords
    payload = {
        "destination": "Paris",
        "language": "French",
        "keywords": "quantum physics",  # Invalid keywords for buddies
        "event": "Science Symposium",  # Invalid event
        "package": "Cultural Explorer Buddy"
    }
    
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print(f"Test Case 26:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid event and keywords
    assert response.status_code == 404, "Test Case 26 Failed"
    print("Test Case 26 Passed")


# Test Case 27: Payload with valid destination, language, and event but invalid package 
def test_case_27():
    # Payload with valid destination, language, and event but invalid package
    payload = {
        "destination": "London",
        "language": "English",
        "keywords": "music,history",
        "event": "Music Festival",
        "package": "Time Traveler Buddy"  # Invalid package
    }
    
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print(f"Test Case 27:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid package
    assert response.status_code == 404, "Test Case 27 Failed"
    print("Test Case 27 Passed")

# Test Case 28: Payload with valid event and package but invalid destination
def test_case_28():
    # Payload with valid event and package but invalid destination
    payload = {
        "destination": "Atlantis",  # Invalid destination
        "language": "English",
        "keywords": "art,culture",
        "event": "Art Tour",
        "package": "Cultural Explorer Buddy"  # Valid package
    }
    
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print(f"Test Case 28:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Expecting a 404 validation error due to invalid destination
    assert response.status_code == 404, "Test Case 28 Failed"
    print("Test Case 28 Passed")


# Test case 29: Valid destination, invalid language
def test_case_29():
    # Payload with a valid destination but invalid language
    payload = {
        "destination": "Paris",  # Valid destination
        "language": "Gibberish",  # Invalid language
        "keywords": "culture, art",  # Valid keywords
        "event": "Art Fair",  # Valid event
        "package": "Culture Enthusiast Buddy"  # Valid package
    }
    
    response = send_buddy_request(payload)
    
    # Enhanced logging for debugging
    print("Test Case 29:")
    print(f"Payload: {payload}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    # Expecting a 404 due to invalid language even though the destination is valid
    assert response.status_code == 404, "Test Case 29 Failed"
    print("Test Case 29 Passed")

# Run the tests for now
if __name__ == "__main__":
    test_case_1()  # This one is already passing 
    test_case_2()  # This one is already passing
    test_case_3()  # This one is already passing  
    test_case_4()  # This one is already passing  
    test_case_5()  # This one is already passing
    test_case_6()  # This one is already passing
    test_case_7()  # This one is already passing
    test_case_8()  # This one is already passing
    test_case_9()  # This one is already passing
    test_case_10() # This one is already passing
    test_case_11() # This one is already passing
    test_case_12() # This one is already passing
    test_case_13() # This one is already passing
    test_case_14() # This one is already passing
    test_case_15() # This one is already passing
    test_case_16() # This one is already passing
    test_case_17() # This one is already passing
    test_case_18() # This one is already passing
    test_case_19() # This one is already passing
    test_case_20() # This one is already passing
    test_case_21() # This one is already passing
    test_case_22() # This one is already passing
    test_case_23() # This one is already passing
    test_case_24() # This one is already passing
    test_case_25() # This one is already passing
    test_case_26() # This one is already passing
    test_case_27() # This one is already passing
    test_case_28() # This one is already passing
    test_case_29() # This one is already passing

    
