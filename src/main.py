from textnode import TextNode, TextType

def main():
    tn = TextNode("dummy text", TextType.LINK, "http//:5043/whatdahell")
    print(tn)
    print(tn == tn)


main()
