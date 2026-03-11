from converter import markdown_to_html_node


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
