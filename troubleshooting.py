from pymongo import MongoClient

client = MongoClient("mongodb+srv://santhoshsivanjustice:MSss2926LoVe@cluster0.krygord.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.NVIDIA

# To add a TROUBLESHOOTING
def add_troubleshooting(stepname, template):
    collection = db['TROUBLESHOOTING AND TEMPLATES']
    existing_step = collection.find_one({"name": stepname })
    if existing_step:
        return f"Troubleshooting/Template '{stepname}' already exists!"
    else:
        troubleshooting = {
            "name": stepname,
            "template": template,
        }
        collection.insert_one(troubleshooting)
        return f"Template '{stepname}' added successfully!"

# To list the troubleshooting step names
def list_troubleshooting_names():
    collection = db['TROUBLESHOOTING AND TEMPLATES']
    stepnames = collection.find({}, {"name": 1})
    stepnames_names = [stepname["name"] for stepname in stepnames]
    return stepnames_names
# To get the Troubleshooting steps
def get_troubleshooting_steps(steps):
    collection = db['TROUBLESHOOTING AND TEMPLATES']
    templates = []
    for step_name in steps:
        document = collection.find_one({"name": step_name})
        templates.append(f"{document['template']}")
    return ("\n\n".join(templates))