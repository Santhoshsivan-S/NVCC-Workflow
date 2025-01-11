from pymongo import MongoClient

client = MongoClient("mongodb+srv://santhoshsivanjustice:MSss2926LoVe@cluster0.krygord.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.NVIDIA

# to add information
def add_info(infoname, infotemplate):
    collection = db['INFORMATION']
    existing_step = collection.find_one({"name": infoname })
    if existing_step:
        return f"Information/Template '{infoname}' already exists!"
    else:
        troubleshooting = {
            "name": infoname,
            "Info": infotemplate,
        }
        collection.insert_one(troubleshooting)
        return f"Information '{infoname}' added successfully!"
# To get information names
def list_info_names():
    collection = db['INFORMATION']
    info_name = collection.find({}, {"name": 1})
    info_name_names = [info["name"] for info in info_name]
    return info_name_names

# To get the info itself
def get_info(info):
    collection = db['INFORMATION']
    infot = []
    for info_name in info:
        document = collection.find_one({"name": info_name})
        infot.append(f"{document['Info']}")
    return ("\n\n".join(infot))