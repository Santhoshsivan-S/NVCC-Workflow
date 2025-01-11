from pymongo import MongoClient

client = MongoClient("mongodb+srv://santhoshsivanjustice:MSss2926LoVe@cluster0.krygord.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.NVIDIA


# To add a new product
def add_product(product_name):
    collection = db['PRODUCTS']
    existing_product = collection.find_one({"name": product_name})
    if existing_product:
        return f"Product '{product_name}' already exists!"
    else:
        product = {
            "name": product_name,
            "questions": []
        }
        collection.insert_one(product)
        return f"Product '{product_name}' added successfully!"

# To List the Products
def list_products():
    collection = db['PRODUCTS']
    products = collection.find({}, {"name": 1})
    product_names = [product["name"] for product in products]
    return product_names