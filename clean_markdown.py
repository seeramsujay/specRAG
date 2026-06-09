from bs4 import BeautifulSoup, Comment
import markdownify


class RegisterMarkdownConverter(markdownify.MarkdownConverter):
    """
    Custom markdownify converter tailored for hardware datasheets.
    Preserves underscores in register names and formats headings/tables cleanly.
    """

    class Options(markdownify.MarkdownConverter.Options):
        heading_style = "atx"
        escape_underscores = False
        escape_asterisks = False
        table_infer_header = True


def sanitize_to_markdown(raw_html: str) -> str:
    """
    Converts raw HTML input to clean Markdown.

    Strips out raw HTML artifacts, scripts, styles, metadata, and other non-content tags.
    Strictly preserves and formats standard HTML tables as Markdown tables.
    """
    if not raw_html:
        return ""

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(raw_html, "html.parser")

    # Decompose script, style, head, metadata, and interactive/form elements completely
    unwanted_tags = [
        "script",
        "style",
        "head",
        "link",
        "meta",
        "title",
        "iframe",
        "noscript",
        "svg",
        "button",
        "form",
        "input",
        "select",
        "textarea",
    ]
    for tag in soup(unwanted_tags):
        tag.decompose()

    # Remove HTML comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Strip styling and other raw HTML attributes to prevent them leaking into the Markdown
    # We preserve colspan and rowspan as they are critical for table structural parsing
    allowed_attributes = {"colspan", "rowspan"}
    for tag in soup.find_all(True):
        attributes_to_remove = [
            attr for attr in tag.attrs if attr not in allowed_attributes
        ]
        for attr in attributes_to_remove:
            del tag.attrs[attr]

    # Convert clean HTML structure to Markdown using the custom register-aware converter
    converter = RegisterMarkdownConverter()
    markdown_output = converter.convert(str(soup))

    return markdown_output
