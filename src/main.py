import os
import shutil
from gencontent import copy_static_to_public, generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)
    if os.path.exists(dir_path_static):
        print("Copying files from static to public...\n")
        copy_static_to_public(dir_path_static, dir_path_public)
    else:
        print("Directory static/ not found...\nExiting...")
        exit(1)

    generate_page(
        os.path.join(dir_path_content, "index.md"),
        template_path,
        os.path.join(dir_path_public, "index.html"),
    )

if __name__ == "__main__":
    main()