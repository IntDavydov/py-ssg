import re

from enum import Enum
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType


class MarkdownSymbol(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"


symbol_map = {
    MarkdownSymbol.BOLD: TextType.BOLD,
    MarkdownSymbol.ITALIC: TextType.ITALIC,
    MarkdownSymbol.CODE: TextType.CODE,
}


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if len(old_nodes) == 0:
        return []

    splited = []
    current = old_nodes[0]

    if current.text_type != TextType.TEXT:
        return [current] + split_nodes_delimiter(old_nodes[1:], delimiter, text_type)

    if delimiter not in [s.value for s in MarkdownSymbol]:
        raise Exception(f"Not such delimiter for inline element: {delimiter}")

    parts = current.text.split(delimiter)
    if len(parts) % 2 == 0:
        raise ValueError("Invalid markdown, formatted section not closed")

    for i in range(len(parts)):
        if parts[i] == "":
            continue

        if i % 2 == 0:
            splited.append(TextNode(parts[i], TextType.TEXT))
        else:
            splited.append(TextNode(parts[i], text_type))

    return splited + split_nodes_delimiter(old_nodes[1:], delimiter, text_type)


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    if len(old_nodes) == 0:
        return []

    splited = []
    current = old_nodes[0]

    if current.text_type != TextType.TEXT:
        return [current] + split_nodes_image(old_nodes[1:])

    parts = re.split(r"(!\[.*?\))", current.text)
    if len(parts) % 2 == 0:
        raise ValueError("Invalid markdown, formatted section not closed")

    images = extract_markdown_images(current.text)
    image_iter = iter(images)

    for i in range(len(parts)):
        if parts[i] == "":
            continue

        if i % 2 == 0:
            splited.append(TextNode(parts[i], TextType.TEXT))
        else:
            image = next(image_iter)
            splited.append(TextNode(image[0], TextType.IMAGE, image[1]))

    return splited + split_nodes_image(old_nodes[1:])


def split_nodes_link(old_nodes):
    if len(old_nodes) == 0:
        return []

    splited = []
    current = old_nodes[0]

    if current.text_type != TextType.TEXT:
        return [current] + split_nodes_link(old_nodes[1:])

    parts = re.split(r"(\[.*?\))", current.text)
    if len(parts) % 2 == 0:
        raise ValueError("Invalid markdown, formatted section not closed")

    links = extract_markdown_links(current.text)
    link_iter = iter(links)

    for i in range(len(parts)):
        if parts[i] == "":
            continue

        if i % 2 == 0:
            splited.append(TextNode(parts[i], TextType.TEXT))
        else:
            link = next(link_iter)
            splited.append(TextNode(link[0], TextType.LINK, link[1]))

    return splited + split_nodes_link(old_nodes[1:])


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    for symbol in MarkdownSymbol:
        nodes = split_nodes_delimiter(nodes, symbol.value, symbol_map[symbol])

    return nodes


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")


def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []

    for block in raw_blocks:
        stripped = block.strip()

        if stripped:
            lines = stripped.split("\n")
            stripped_lines = [line.strip() for line in lines]
            blocks.append("\n".join(stripped_lines))

    return blocks


def block_to_block_type(block):
    lines = block.split("\n")

    match block:
        case b if re.match(r"^#{1,6}\s", b):
            return BlockType.HEADING
        case b if (
            len(lines) > 1
            and lines[0].startswith("```")
            and lines[-1].startswith("```")
        ):
            return BlockType.CODE
        case b if b.startswith(">"):
            for line in lines:
                if not line.startswith(">"):
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        case b if b.startswith("- "):
            for line in lines:
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        case b if re.match(r"^\d+\.\s", b):
            for i in range(len(lines)):
                if not lines[i].startswith(f"{i + 1}. "):
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST

        case _:
            return BlockType.PARAGRAPH


def block_to_html_nodes(block, node_type):
    text_nodes = text_to_textnodes(block)
    if len(text_nodes) == 1:
        return LeafNode(node_type, block)
    else:
        html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
        return ParentNode(node_type, html_nodes)


def block_to_heading_nodes(block):
    lines = block.split("\n")
    processed_lines = []
    for line in lines:
        heading_lvl = len(line) - len(line.lstrip("#"))
        node_type = f"h{heading_lvl}"
        processed_lines.append(block_to_html_nodes(line.lstrip("#").strip(), node_type))

    return processed_lines


def block_to_paragraph_node(block):
    lines = block.split("\n")
    processed_block = " ".join(lines)
    nodes = block_to_html_nodes(processed_block, "p")
    return nodes


def block_to_code_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def block_to_quote_nodes(block):
    items = block.split("\n")
    processed_lines = []
    for item in items:
        if not item.startswith("> "):
            raise ValueError("Invalid quote block")
        processed_lines.append(item.lstrip(">").strip())

    processed_block = " ".join(processed_lines)
    return block_to_html_nodes(processed_block, "blockquote")


def block_to_ulist_nodes(block):
    lis = []
    items = block.split("\n")
    for item in items:
        lis.append(LeafNode("li", item.lstrip("- ")))

    return ParentNode("ul", lis)


def block_to_olist_nodes(block):
    lis = []
    items = block.split("\n")
    for item in items:
        cleaned_text = re.sub(r"^\d+\. ", "", item)
        lis.append(LeafNode("li", cleaned_text))

    return ParentNode("ol", lis)


def block_type_to_html_node(block, block_type):
    match block_type:
        case block_type.PARAGRAPH:
            return block_to_paragraph_node(block)
        case block_type.HEADING:
            return block_to_heading_nodes(block)
        case block_type.CODE:
            return block_to_code_node(block)
        case block_type.QUOTE:
            return block_to_quote_nodes(block)
        case block_type.UNORDERED_LIST:
            return block_to_ulist_nodes(block)
        case block_type.ORDERED_LIST:
            return block_to_olist_nodes(block)


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_type_to_html_node(block, block_type)
        if isinstance(html_node, list):
            children.extend(html_node)
        else:
            children.append(html_node)

    return ParentNode("div", children)
