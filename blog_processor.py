import datetime
import hashlib
import json
import os
import uuid
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

PATH_TO_BLOGS = "/Users/vicky/Repository/Blog-Scratch/blogs"

METADATA_FILE_NAME = "metadata.json"

BLOG_FILE_NAME = "blog.mdx"

# read the blog and update metadata

directory_with_blogs = os.fsencode(PATH_TO_BLOGS)


def is_valid_uuid(uuid_to_test, version=4):
    # check for validity of Uuid
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        logging.error('not a valid uuid {}'.format(uuid_to_test))
        return 'false'
    return 'true'


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


def main():
    for directory in os.listdir(directory_with_blogs):
        blog_dir_name = os.fsdecode(directory)

        current_time = datetime.datetime.now()

        if not os.path.isdir(os.path.join(PATH_TO_BLOGS, blog_dir_name)):
            continue

        if is_valid_uuid(blog_dir_name) == 'true':
            logging.info("Processing blog {}".format(blog_dir_name))
            blog_metadata_path = os.path.join(PATH_TO_BLOGS, blog_dir_name, METADATA_FILE_NAME)
            with (open(blog_metadata_path) as metadata_json_file):
                metadata = json.load(metadata_json_file)


                # ensure the metadata structure
                if ("publish" not in metadata) or ("blogNumber" not in metadata) or ("id" not in metadata) or (
                        "previewImageSrc" not in metadata) or (
                        "author" not in metadata) or ("tags" not in metadata) or ("title" not in metadata) or (
                        "summary" not in metadata) or ("slug" not in metadata) or ("demo" not in metadata):
                    logging.warning('missing mandatory data in blog {} so not processing'.format(blog_dir_name))
                    break

                if not metadata["publish"] == True:
                    logging.warning('publish is not true in blog {} so not processing'.format(blog_dir_name))
                    continue

                blog_number = metadata["blogNumber"]
                blog_name = metadata["title"]

                blog_content_path = os.path.join(PATH_TO_BLOGS, blog_dir_name, BLOG_FILE_NAME)
                blog_content_file_hash = hashfile(blog_content_path)

                if "hash" in metadata:
                    if blog_content_file_hash == metadata["hash"]:
                        logging.info(
                            'Blog has no changes from {} so skipping update of {} {}'.format(
                                metadata["updatedAt"],
                                blog_name, blog_number))
                    else:
                        logging.info(
                            'Blog content changed from {} so updating {} {}'.format(metadata["updatedAt"], blog_name,
                                                                                    blog_number))
                        metadata["updatedAt"] = str(current_time)
                        metadata["hash"] = blog_content_file_hash
                        metadata["version"] = metadata["version"] + 1
                        json.dump(metadata, open(blog_metadata_path, "w"), ensure_ascii=False, indent=4, sort_keys=True)

                else:
                    logging.info('No hash so processing the new blog {} {} by {}'.format(blog_name, blog_number,
                                                                                         metadata["author"]))

                    metadata["version"] = 1
                    metadata["updatedAt"] = str(current_time)
                    metadata["createdAt"] = str(current_time)
                    metadata["hash"] = blog_content_file_hash

                    json.dump(metadata, open(blog_metadata_path, "w"), ensure_ascii=False, indent=4, sort_keys=True)
        else:
            logging.info('Blog directory name {} does not have the correct format so skipping'.format(blog_dir_name))


main()
