import json
import os
import uuid
import logging

PATH_TO_BLOGS = "/Users/vicky/Repository/Blog-Scratch/blogs"
METADATA_FILE_NAME = "metadata.json"


def main():
    blog_id = uuid.uuid4()

    blogs_data_path = os.path.join(PATH_TO_BLOGS, METADATA_FILE_NAME)
    with (open(blogs_data_path, "rw") as blogs_data_file):
        blogs_data = json.load(blogs_data_file)

        logging.info("creating new blog with id {}".format(blog_id))
        title = input("blog title : ")
        author = input("blog author : ")
        summary = input("blog summary : ")
        slug = input("blog slug : ")

        os.makedirs(os.path.join(PATH_TO_BLOGS, str(blog_id)))

        # creat the blog file
        open(os.path.join(PATH_TO_BLOGS, str(blog_id), "blog.mdx"), 'w')

        # creat the metadata file
        metadata = {"id": str(blog_id), "publish": False, "blogNumber": blogs_data["nextBlogNumber"], "title": title,
                    "tags": [], "previewImageSrc": "",
                    "author": author, "summary": summary, "slug": slug, "demo": {"live": False,
                                                                                 "preview": None,
                                                                                 "repository": None}}

        processed_metadata_file_path = os.path.join(PATH_TO_BLOGS, str(blog_id), "metadata.json")
        print("customize the {}".format(processed_metadata_file_path))

        json.dump(metadata, open(processed_metadata_file_path, "w"), ensure_ascii=False, indent=4, sort_keys=True)

        # update the blogs data
        blogs_data["blogs"].append(str(blog_id))
        blogs_data["nextBlogNumber"] = blogs_data["nextBlogNumber"] + 1
        json.dump(metadata, blogs_data_file, ensure_ascii=False, indent=4, sort_keys=True)


main()
