# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username="aacuser", password="HardcoreColtsFan$", host="localhost", port=27017, db="aac", col="animals"): 
        # Initializing the MongoClient. This helps to access the MongoDB
        try:
            self.client = MongoClient(f"mongodb://{username}:{password}@{host}:{port}")
            self.database = self.client[db]
            self.collection = self.database[col]
        except Exception as e:
            raise Exception(f"Failed to connect to MongoDB: {e}")
    
    # Create a method to return the next available record number for use in the create method
    def get_next_record_number(self):
        try:
            last_record = self.collection.find_one(sort=[("record_number", -1)]
                                                  )
            if last_record and "record_number" in last_record:
                return last_record["record_number"] + 1
            else:
                return 1
        except Exception as e:
            print(f"Error generating next record number: {e}")
            return 1
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        if data is not None and isinstance(data, dict): 
            try:
                data["record_number"] = self.get_next_record_number()
                self.collection.insert_one(data)  
                return True
            except Exception as e:
                print(f"Error inserting document: {e}")
                return False
        else:
            raise ValueError("Data must be a non-empty dictionary.")

    # Create method to implement the R in CRUD.
    def read(self, query):
        if query is not None and isinstance(query, dict):
            try:
                cursor = self.collection.find(query)
                return list(cursor) 
            except Exception as e:
                print(f"Error reading documents: {e}")
                return []
        else:
            raise ValueError("Query must be a non-empty dictionary.")
    
    # Create method to implement the U in CRUD.
    def update(self, query, new_values):
        if query is not None and isinstance(query, dict) and isinstance(new_values, dict):
            try: 
                result = self.collection.update_many(query, {"$set": new_values})
                return result.modified_count
            except Exception as e:
                print(f"Error updating documents: {e}") 
                return 0
        else: 
            raise ValueError("Query and new_values must be non-empty dictionaries.")
    
    # Create method to implement the D in CRUD.
    def delete(self, query):
        if query is not None and isinstance(query, dict):
            try: 
                result = self.collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                print(f"Error deleting documents: {e}")
                return 0
        else: 
            raise ValueError("Query must be a non-empty dictionary.")
        