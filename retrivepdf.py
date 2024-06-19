import pymongo

# Connect to the MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string

# Access the database
db = client["Db"]  # Replace "mydatabase" with your database name

# Access the collection
collection = db["register"]  # Replace "mycollection" with your collection name

# Retrieve data from the collection
query = {}  # This empty query retrieves all documents in the collection
cursor = collection.find(query)

# Process retrieved documents
for document in cursor:
    print(document)  # Replace this with your processing logic

# Close the connection
client.close()
