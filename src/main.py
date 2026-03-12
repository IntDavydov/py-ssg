import os

from copystatic import copystatic

from generate_page import generate_pages_recursive


def getroot():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(src_dir)


def main():
    # copu from static to public
    copystatic()

    # from markdown to html
    root = getroot()
    dir_path_content = os.path.join(root, "content")
    template_path = os.path.join(root, "template.html")
    dest_dir_path = os.path.join(root, "public")
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)


main()
