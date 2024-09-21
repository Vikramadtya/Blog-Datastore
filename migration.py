import datetime
import hashlib
import json
import os
import uuid

PATH_TO_BLOGS = "/Users/vicky/Repository/Blog-Scratch/blogs"
PATH_TO_STATIC = "/Users/vicky/Repository/Blog-Scratch/_static"

METADATA_FILE_NAME = "metadata.json"

BLOG_FILE_NAME = "blog.mdx"

# read the blog and update metadata

directory_with_blogs = os.fsencode(PATH_TO_BLOGS)


def hashfile(file):
    # A arbitrary (but fixed) buffer
    # size (change accordingly)
    # 65536 = 65536 bytes = 64 kilobytes
    BUF_SIZE = 65536

    # Initializing the sha256() method
    sha256 = hashlib.sha256()

    # Opening the file provided as
    # the first commandline argument
    with open(file, 'rb') as f:

        while True:

            # reading data = BUF_SIZE from
            # the file and saving it in a
            # variable
            data = f.read(BUF_SIZE)

            # True if eof = 1
            if not data:
                break

            # Passing that data to that sh256 hash
            # function (updating the function with
            # that data)
            sha256.update(data)

    # sha256.hexdigest() hashes all the input
    # data passed to the sha256() via sha256.update()
    # Acts as a finalize method, after which
    # all the input data gets hashed hexdigest()
    # hashes the data, and returns the output
    # in hexadecimal format
    return sha256.hexdigest()


# create the static data post processing
for directory in os.listdir(directory_with_blogs):
    blog_dir_name = os.fsdecode(directory)

    current_time = datetime.datetime.now()

    if len(blog_dir_name.split(":")) == 2:
        blog_number = blog_dir_name.split(":")[0]
        blog_name = blog_dir_name.split(":")[1]
        blog_metadata_path = os.path.join(PATH_TO_BLOGS, blog_dir_name, METADATA_FILE_NAME)
        with (open(blog_metadata_path) as metadata_json_file):
            metadata = json.load(metadata_json_file)

            if ("publish" not in metadata) or ("blogNumber" not in metadata) or ("previewImageSrc" not in metadata) or (
                    "author" not in metadata) or ("tags" not in metadata) or ("title" not in metadata) or (
                    "summary" not in metadata) or ("slug" not in metadata) or ("demo" not in metadata):
                print('missing mandatory data in blog {}'.format(blog_dir_name))
                break

            blog_content_path = os.path.join(PATH_TO_BLOGS, blog_dir_name, BLOG_FILE_NAME)
            blog_content_file_hash = hashfile(blog_content_path)
            metadata_content_file_hash = hashfile(blog_metadata_path)

            if "id" in metadata:
                if blog_content_file_hash == metadata["hash"]:
                    print(
                        'Blog metadata has no changes from {} so skipping update of {} {}'.format(metadata["updatedAt"],
                                                                                                  blog_name, blog_number))
                else:
                    print('Blog content changed from {} so updating {} {}'.format(metadata["updatedAt"], blog_name,
                                                                                  blog_number))
                    metadata["updatedAt"] = str(current_time)
                    metadata["hash"] = blog_content_file_hash
                    metadata["version"] = metadata["version"] + 1

                    with open(blog_content_path, 'r') as blog_content_file:
                        blog_content = blog_content_file.read()
                        processed_blog_content_file_path = os.path.join(PATH_TO_STATIC, metadata["id"],
                                                                        metadata["id"] + ".mdx")
                        with open(processed_blog_content_file_path, 'w') as processed_blog_content_file:
                            processed_blog_content_file.write(blog_content)

                json.dump(metadata, open(blog_metadata_path, "w"), ensure_ascii=False, indent=4, sort_keys=True)
                processed_metadata_file_path = os.path.join(PATH_TO_STATIC, metadata["id"], metadata["id"] + ".json")
                json.dump(metadata, open(processed_metadata_file_path, "w"), ensure_ascii=False, indent=4, sort_keys=True)
            else:
                print('No hash so processing the new blog {} {} by {}'.format(blog_name, blog_number, metadata["author"]))
                metadata["version"] = 1
                metadata["updatedAt"] = str(current_time)
                metadata["createdAt"] = str(current_time)
                metadata["hash"] = blog_content_file_hash
                metadata["id"] = str(uuid.uuid4())

                os.makedirs(os.path.join(PATH_TO_STATIC, metadata["id"]))

                with open(blog_content_path, 'r') as blog_content_file:
                    blog_content = blog_content_file.read()
                    processed_blog_content_file_path = os.path.join(PATH_TO_STATIC, metadata["id"],
                                                                    str(metadata["id"]) + ".mdx")
                    with open(processed_blog_content_file_path, 'w') as processed_blog_content_file:
                        processed_blog_content_file.write(blog_content)

                json.dump(metadata, open(blog_metadata_path, "w"), ensure_ascii=False, indent=4, sort_keys=True)
                processed_metadata_file_path = os.path.join(PATH_TO_STATIC, metadata["id"], metadata["id"] + ".json")

                json.dump(metadata, open(processed_metadata_file_path, "w"), ensure_ascii=False, indent=4, sort_keys=True)
