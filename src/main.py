import os

from copystatic import copystatic

from generate_page import generate_page


def getroot():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(src_dir)


def main():
    copystatic()

    root = getroot()
    from_path = os.path.join(root, "content", "index.md")
    template_path = os.path.join(root, "template.html")

    generate_page()


main()
