import os
import shutil
from markdownblock import markdown_to_html_node

def copy_static_to_public(source_dir_path, dest_dir_path):
    # Get a list of items in the source directory
    contents = os.listdir(source_dir_path)

    for object in contents:
        # Build the full source path for the item
        current_path = os.path.join(source_dir_path, object)
        # Build the corresponding destination path for the item
        dest_object_path = os.path.join(dest_dir_path, object)

        if os.path.isfile(current_path):
            print(f"Copying {current_path} to {dest_object_path}...")
            shutil.copy(current_path, dest_object_path)
        elif os.path.isdir(current_path):
            # Create the corresponding directory in the destination
            os.mkdir(dest_object_path)
            # Recursively call the function for the subdirectory
            copy_static_to_public(current_path, dest_object_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No Title found in markdown provided")

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Load markdown file in from_path
    markdown_file = open(from_path)
    markdown = markdown_file.read()
    markdown_file.close()
    # Load template file in template_path
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()
    # Convert markdown to html
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    # Replace {{ Title }} and {{ Content }}
    new_html = template.replace("{{ Title }}", title)
    new_html = new_html.replace("{{ Content }}", html)
    new_html = new_html.replace('href="/', f'href="{basepath}')
    new_html = new_html.replace('src="/', f'src="{basepath}')
    # Write a new html file at dest_path
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    new_html_file = open(dest_path, "w")
    new_html_file.write(new_html)
    new_html_file.close()

def generate_pages_recursive(basepath, content_path, template_path, dest_path):
    # Get a list of items in the source directory
    contents = os.listdir(content_path)

    for object in contents:
        # Build the full source path for the item
        current_path = os.path.join(content_path, object)
        # Build the corresponding destination path for the item
        dest_object_path = os.path.join(dest_path, object)

        if os.path.isfile(current_path) and object.endswith(".md"):
            dest_html_path = os.path.join(dest_path, object.replace(".md", ".html"))
            generate_page(basepath, current_path, template_path, dest_html_path)
        elif os.path.isfile(current_path):
            shutil.copy(current_path, dest_object_path)
        elif os.path.isdir(current_path):
            # Create the corresponding directory in the destination
            os.mkdir(dest_object_path)
            # Recursively call the function for the subdirectory
            generate_pages_recursive(basepath, current_path, template_path, dest_object_path)
