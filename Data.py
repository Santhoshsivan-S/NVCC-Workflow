from pymongo import MongoClient

client = MongoClient("mongodb+srv://santhoshsivanjustice:MSss2926LoVe@cluster0.krygord.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.NVIDIA


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
def list_products():
    collection = db['PRODUCTS']
    products = collection.find({}, {"name": 1})
    product_names = [product["name"] for product in products]
    return product_names

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

def list_questions(product_name):
    collection = db['PRODUCTS']
    """Returns a list of questions for the given product_name."""
    product = collection.find_one({"name": product_name})
    if product and "questions" in product:
        return product["questions"]
    else:
        return []

def add_steps(stepname, template, private):
    collection = db['TROUBLESHOOTING AND TEMPLATES']
    existing_step = collection.find_one({"name": stepname })
    if existing_step:
        return f"Troubleshooting/Template '{stepname}' already exists!"
    else:
        troubleshooting = {
            "name": stepname,
            "template": template,
            "Private": private
        }
        collection.insert_one(troubleshooting)
        return f"Template '{stepname}' added successfully!"

def list_steps():
    collection = db['TROUBLESHOOTING AND TEMPLATES']
    stepnames = collection.find({}, {"name": 1})
    stepnames_names = [stepname["name"] for stepname in stepnames]
    return stepnames_names

def get_steps(steps):
    collection = db['TROUBLESHOOTING AND TEMPLATES']
    templates = []
    for step_name in steps:
        document = collection.find_one({"name": step_name})
        templates.append(f"{document['template']}")
    return ("\n\n".join(templates))

def get_steps_private(steps):
    collection = db['TROUBLESHOOTING AND TEMPLATES']
    templates = []
    for step_name in steps:
        document = collection.find_one({"name": step_name})
        templates.append(f"{document['Private']}")
    return ("\n".join(templates))
def list_info():
    collection = db['INFORMATION']
    info_name = collection.find({}, {"name": 1})
    info_name_names = [info["name"] for info in info_name]
    return info_name_names

def get_info(info):
    collection = db['INFORMATION']
    infot = []
    for info_name in info:
        document = collection.find_one({"name": info_name})
        infot.append(f"{document['Info']}")
    return ("\n\n".join(infot))

def add_info(infoname, infotemplate,private):
    collection = db['INFORMATION']
    existing_step = collection.find_one({"name": infoname })
    if existing_step:
        return f"Information/Template '{infoname}' already exists!"
    else:
        troubleshooting = {
            "name": infoname,
            "Info": infotemplate,
            "private": private
        }
        collection.insert_one(troubleshooting)
        return f"Information '{infoname}' added successfully!"


def get_info_private(info):
    collection = db['INFORMATION']
    infot = []
    for info_name in info:
        document = collection.find_one({"name": info_name})
        infot.append(f"{document['private']}")
    return ("\n".join(infot))