from pathlib import Path

from converter import markdown_to_html_node


def getroot():
    current_file = Path(__file__).resolve()
    return current_file.parent


def extract_title(markdown):
    lines = markdown.split("# ")
    if len(lines) == 1:
        raise ValueError("No title found in a markdown. Please add # Title to markdown")
    return lines[1].strip()


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as m:
        markdown = m.read()

    with open(template_path, "r") as t:
        template = t.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    with open(dest_path, "w") as page:
        page.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dest_dir = Path(dest_dir_path)
    dest_dir.mkdir(parents=True, exist_ok=True)

    dir_path = Path(dir_path_content)
    for file in dir_path.iterdir():
        if file.is_dir():
            generate_pages_recursive(file, template_path, dest_dir / file.name)
        elif file.is_file() and file.suffix == ".md":
            print(f"Processing: {file.name}")
            from_path = dir_path / file

            dest_path = dest_dir / file.name
            dest_path = dest_path.with_suffix(".html")
            print(f"Generate from {from_path} -> {dest_path}")

            generate_page(from_path, template_path, dest_path)

    return
