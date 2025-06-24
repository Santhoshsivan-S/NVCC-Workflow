# File: Backend/template_manager.py

class TemplateManager:
    def __init__(self, user_name, client):
        safe_user_name = user_name.replace(" ", "_")
        db_template = client[f"NVCC_Templates_{safe_user_name}"]
        self.collections_troubleshooting = db_template["Troubleshooting_Templates"]
        self.collections_information = db_template["Information_Templates"]
        self.collections_probing = db_template["ProbingQuestion_Templates"]
        self.collections_pre_made_template = db_template["Pre_Made_Template"]

    # Products
    def add_new_product(self, name):
        entry = {"name": name, "questions": []}
        self.collections_probing.insert_one(entry)

    def find_questions(self, product):
        result = self.collections_probing.find_one({"name": product})
        return result

    def list_product(self):
        return self.collections_probing.find({}, {"name": 1})

    def delete_product(self, product):
        self.collections_probing.delete_one({"name": product})

    def add_questions_add_to_set(self, product, question):
        self.collections_probing.update_one(
            {"name": product},
            {"$addToSet": {"questions": question}}
        )
    def add_questions_set(self, product, question_list):
        self.collections_probing.update_one(
            {"name": product},
            {"$set": {"questions": question_list}}
        )

    def delete_question(self, product, question):
        self.collections_probing.update_one(
            {"name": product},
            {"$pull": {"questions": question}}
        )

    # Information
    def add_new_information(self, name_info, template):
        self.collections_information.insert_one({"name": name_info, "Info": template})

    def modify_information(self, info_name_ts, template):
        self.collections_information.update_one(
            {"name": info_name_ts}, {"$set": {"template": template}})

    def delete_information(self, info_name):
        self.collections_information.delete_one({"name": info_name})

    def list_info_names(self):
        return self.collections_information.find({}, {"name": 1})

    def get_info_template(self, info_name):
        return self.collections_information.find_one({"name": info_name})

    # Troubleshooting
    def add_new_troubleshooting(self, name_ts, template):
        self.collections_troubleshooting.insert_one({"name": name_ts, "template": template})

    def modify_troubleshooting(self, step_name_ts, template):
        self.collections_troubleshooting.update_one(
            {"name": step_name_ts}, {"$set": {"template": template}})

    def delete_troubleshooting(self, step_name):
        self.collections_troubleshooting.delete_one({"name": step_name})

    def list_ts_names(self):
        return self.collections_troubleshooting.find({}, {"name": 1})

    def get_ts_template(self, step_name_ts):
        return self.collections_troubleshooting.find_one({"name": step_name_ts})

    #Pre-Made Template

    def add_pre_made_template(self, pre_made_template, template):
        self.collections_pre_made_template.insert_one({"name": pre_made_template, "template": template})
    def modify_pre_made_template(self, pre_made_template, template):
        self.collections_pre_made_template.update_one(
            {"name": pre_made_template}, {"$set": {"template": template}})
    def delete_pre_made_template(self, pre_made_template):
        self.collections_pre_made_template.delete_one({"name": pre_made_template})
    def list_pre_made_template(self):
        return self.collections_pre_made_template.find({}, {"name": 1})

    def get_pre_made_template(self, pre_made_template):
        return self.collections_pre_made_template.find_one({"name": pre_made_template})