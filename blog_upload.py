import json
import os
import random
import uuid

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

PATH_TO_BLOGS = "/_generated"

FIREBASE_AUTH_JSON = {
    "type": "service_account",
    "project_id": os.environ['PROJECT_ID'],
    "private_key_id": os.environ['PRIVATE_KEY_ID'],
    "private_key": os.environ['PRIVATE_KEY'],
    "client_email": os.environ['CLIENT_EMAIL'],
    "client_id": os.environ['CLIENT_ID'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ['CLIENT_X509_CERT_URL'],
    "universe_domain": "googleapis.com"
}

# Use a service account.
cred = credentials.Certificate(FIREBASE_AUTH_JSON)

app = firebase_admin.initialize_app(cred)
db = firestore.client()

directoryWithBlogs = os.fsencode(PATH_TO_BLOGS)


def get_data_for_collection(collection_name, key):
    collection_reference = db.collection(collection_name)
    key_to_object_map = {}
    for collection_item in collection_reference.stream():
        key_to_object_map[collection_item.get(key)] = collection_item.to_dict()
    return key_to_object_map


# Fetch all existing tags
tag_name_to_object_map = get_data_for_collection("tags", "name")
blog_id_to_metadata_map = get_data_for_collection("blogs", "id")
user_name_to_object_map = get_data_for_collection("users", "username")


def create_new_tag(tag):
    data = {"id": str(uuid.uuid4()), "name": tag, "color": get_random_color(), "blogs": set()}
    tag_name_to_object_map[tag] = data
    return data


def update_exiting_tag(tag, blog_id):
    data = tag_name_to_object_map[tag]
    data["blogs"].add(blog_id)
    tag_name_to_object_map["all"]["blogs"].append(blog_id)
    return data


def get_random_color():
    colors = ["#27ae60", "#e74c3c", "#3498db"]
    return random.choice(colors)


def convert_metadata(metadata):
    resolved_tags = []
    for tag in metadata["tags"]:
        if tag not in tag_name_to_object_map:
            create_new_tag(tag)
        resolved_tags.append(update_exiting_tag(tag, metadata["id"]))

    metadata["tags"] = resolved_tags
    metadata["author"] = user_name_to_object_map[metadata["author"]]
    return metadata


def update_metadata(metadata):
    doc_ref = db.collection("blogs").document(metadata["id"])
    doc_ref.set(metadata)
    return metadata


def add_new_metadata(metadata):
    doc_ref = db.collection("blogs").document(metadata["id"])
    doc_ref.set(metadata)

    doc_ref = db.collection("metadata").document(metadata["id"])
    doc_ref.set({"id": metadata["id"], "likes": 0, "views": 0})

    return metadata


def add_new_tag(tag):
    doc_ref = db.collection("tags").document(tag["name"])
    doc_ref.set(tag)
    return tag


def main():
    for directory in os.listdir(directoryWithBlogs):
        blog_dir_name = os.fsdecode(directory)

        with (open(os.path.join(PATH_TO_BLOGS, blog_dir_name, blog_dir_name + ".json")) as metadataJsonFile):
            metadata = json.load(metadataJsonFile)

            if blog_dir_name in blog_id_to_metadata_map:
                if blog_id_to_metadata_map[blog_dir_name].get("updatedAt") == metadata['updatedAt']:
                    print(
                        "blog {} ({}) is upto date {}".format(metadata['title'], blog_dir_name, metadata['updatedAt']))
                    blog_id_to_metadata_map.__delitem__(blog_dir_name)

                else:
                    print("blog {} ({}) is updated".format(metadata['title'], blog_dir_name))
                    update_metadata(convert_metadata(metadata))
            else:
                print("blog {} ({}) is created".format(metadata['title'], blog_dir_name))
                add_new_metadata(convert_metadata(metadata))

    for tagName in tag_name_to_object_map:
        tag = tag_name_to_object_map[tagName]
        tag["blogs"] = set(tag["blogs"])
        add_new_tag(tag)

        print("created tag {}".format(tagName))


main()
