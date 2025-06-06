import os
import shutil
from markdown_convert import markdown_to_blocks
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
    blocks = markdown_to_blocks(markdown)
    node = markdown_to_html_node(blocks[0])
    header = node.children[0]
    if header.tag == "h1":
        return header.value
    else:
        raise Exception("No Title found in markdown provided")

def generate_page(from_path, template_path, dest_path):
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
    # Write a new html file at dest_path
    if os.path.exists(dest_path):
        new_html_file = open(dest_path)
        new_html_file.write(new_html)
    else:
        new_html_file = open(dest_path, "x")
        new_html_file.write(new_html)
        new_html_file.close()

def main():
    if os.path.exists("public/"):
        shutil.rmtree("public/")
    os.mkdir("public/")
    if os.path.exists("static/"):
        print("Copying files from static to public...\n")
        copy_static_to_public("static/", "public/")
    else:
        print("Directory static/ not found...\nExiting...")
        exit(1)

    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()