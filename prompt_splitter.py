import re
from typing import Dict


def split_pages(text: str) -> Dict[str, str]:
    """
    Split the text into blocks based on headings like "[Page 1]", "[Page 2]", etc.,
    and store each full block (including the heading) in a dictionary.
    The heading and body are kept together — the entire block is stored as-is.
    Keys are normalized to lowercase without spaces, e.g., "page1", "page2", etc.
    """
    # Split right before each [Page X] (positive lookahead)
    blocks = re.split(r"(?=\[Page\s+\d+\])", text)

    pages = {}
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Extract the page number from the heading like [Page 1]
        m = re.match(r"\[Page\s+(\d+)\]", block)
        if m:
            num = m.group(1)  # "1", "2", ...
            key = f"page{num}"  # "page1", "page2", etc.
            pages[key] = block  # Store the entire block (heading + content)

    return pages
