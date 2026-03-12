import os
import sys

from copystatic import copystatic

from generate_page import generate_pages_recursive


def getroot():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(src_dir)


def main():

    # copu from static to public
    copystatic("docs")

    # from markdown to html
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

    root = getroot()
    dir_path_content = os.path.join(root, "content")
    template_path = os.path.join(root, "template.html")
    dest_dir_path = os.path.join(root, "docs")
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path)


main()
