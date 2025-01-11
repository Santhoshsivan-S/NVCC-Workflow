from pymongo import MongoClient

client = MongoClient("mongodb+srv://santhoshsivanjustice:MSss2926LoVe@cluster0.krygord.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.NVIDIA

#To add the Questions
def add_question(product_name, question):
    collection = db['PRODUCTS']
    """Inserts a question into the product document with the given product_name."""
    product = collection.find_one({"name": product_name})
    if product and "questions" in product and question not in product["questions"]:
        result = collection.update_one(
            {"name": product_name},
            {"$push": {"questions": question}}
        )
        if result.modified_count > 0:
            return f"Inserted question into product '{product_name}'"
        else:
            return f"Failed to insert question into product '{product_name}'"
    elif product and "questions" in product and question in product["questions"]:
        return f"Question '{question}' already exists for product '{product_name}'"
    else:
        return f"Product '{product_name}' not found"

# To List the Questions
def list_questions(product_name):
    collection = db['PRODUCTS']
    """Returns a list of questions for the given product_name."""
    product = collection.find_one({"name": product_name})
    if product and "questions" in product:
        return product["questions"]
    else:
        return []