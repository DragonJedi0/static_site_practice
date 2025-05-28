from textnode import TextType, TextNode

def main():
    text_object = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(text_object.__repr__())


if __name__ == "__main__":
    main()