from pymongo import MongoClient
from datetime import datetime
from pprint import pprint

class LinkedInProfileManager:
    def __init__(self, database_url="mongodb://localhost:27017/"):
        # Connect to MongoDB
        self.client = MongoClient(database_url)
        self.db = self.client.linkedin_db
        self.profiles = self.db.profiles

    def create_profile(self, profile_data):
        """Create a new LinkedIn profile"""
        profile_data["created_at"] = datetime.now()
        profile_data["updated_at"] = datetime.now()
        
        result = self.profiles.insert_one(profile_data)
        return result.inserted_id

    def get_profile(self, profile_id):
        """Retrieve a profile by ID"""
        return self.profiles.find_one({"_id": profile_id})

    def update_profile(self, profile_id, updates):
        """Update an existing profile"""
        updates["updated_at"] = datetime.now()
        
        result = self.profiles.update_one(
            {"_id": profile_id},
            {"$set": updates}
        )
        return result.modified_count > 0

    def delete_profile(self, profile_id):
        """Delete a profile"""
        result = self.profiles.delete_one({"_id": profile_id})
        return result.deleted_count > 0

    def search_profiles(self, criteria):
        """Search profiles based on criteria"""
        return list(self.profiles.find(criteria))

# Example usage
def main():
    # Initialize the profile manager
    profile_manager = LinkedInProfileManager()

    # Example profile data
    sample_profile = {
        "first_name": "John",
        "last_name": "Doe",
        "headline": "Senior Software Engineer",
        "current_company": "Tech Corp",
        "location": {
            "city": "San Francisco",
            "country": "USA"
        },
        "skills": ["Python", "MongoDB", "AWS"],
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "start_date": "2020-01",
                "end_date": None,  # Current position
                "description": "Leading backend development team"
            }
        ],
        "education": [
            {
                "school": "University of California",
                "degree": "BS Computer Science",
                "graduation_year": 2015
            }
        ]
    }

    # Create a profile
    profile_id = profile_manager.create_profile(sample_profile)
    print(f"Created profile with ID: {profile_id}")

    # Retrieve the profile
    profile = profile_manager.get_profile(profile_id)
    print("\nRetrieved profile:")
    pprint(profile)

    # Update the profile
    updates = {
        "headline": "Lead Software Engineer",
        "skills": ["Python", "MongoDB", "AWS", "Docker"]
    }
    profile_manager.update_profile(profile_id, updates)
    print("\nProfile updated")

    # Search for profiles
    search_results = profile_manager.search_profiles({"location.city": "San Francisco"})
    print(f"\nFound {len(search_results)} profiles in San Francisco")

if __name__ == "__main__":
    main()