import re
import html
from html.parser import HTMLParser
from urllib.request import Request, urlopen


class TableParser(HTMLParser):
    """Extract text from every table cell in document order."""

    def __init__(self):
        super().__init__()
        self.in_cell = False
        self.current_cell = []
        self.rows = []
        self.current_row = []

    def handle_starttag(self, tag, attrs):
        if tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = []
        elif tag == "tr":
            self.current_row = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.in_cell:
            text = "".join(self.current_cell).strip()
            self.current_row.append(text)
            self.in_cell = False

        elif tag == "tr" and self.current_row:
            self.rows.append(self.current_row)

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell.append(data)


def fetch_document(url):
    # Download the published Google Doc.
    request = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urlopen(request, timeout=30) as response:
        content_type = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(content_type, errors="replace")


def parse_table_data(document):
    # Parse HTML tables when the published document contains a table.
    parser = TableParser()
    parser.feed(document)

    points = []

    for row in parser.rows:
        if len(row) < 3:
            continue

        # Try both common column orders:
        # character, x-coordinate, y-coordinate
        # x-coordinate, character, y-coordinate
        candidates = [
            (row[0], row[1], row[2]),
            (row[1], row[0], row[2]),
            (row[0], row[2], row[1]),
            (row[2], row[0], row[1]),
            (row[2], row[1], row[0]),
        ]

        for character, x_text, y_text in candidates:
            try:
                x = int(x_text.strip())
                y = int(y_text.strip())

                if x >= 0 and y >= 0 and character:
                    points.append((x, y, character))
                    break
            except ValueError:
                continue

    return points


def parse_text_data(document):
    # Decode HTML entities and remove simple HTML tags.
    text = html.unescape(document)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)

    points = []

    # Match rows where the three values are separated by whitespace,
    # commas, tabs, or vertical bars.
    pattern = re.compile(
        r"([^\s,|]+)\s*[,|;\t ]\s*"
        r"(\d+)\s*[,|;\t ]\s*(\d+)"
    )

    for match in pattern.finditer(text):
        character, x_text, y_text = match.groups()
        points.append((int(x_text), int(y_text), character))

    return points


def print_secret_grid(url):
    document = fetch_document(url)

    points = parse_table_data(document)

    # Fall back to text parsing if no usable table rows were found.
    if not points:
        points = parse_text_data(document)

    if not points:
        raise ValueError("No character coordinates were found in the document.")

    # Store characters by their coordinate.
    grid = {}
    max_x = 0
    max_y = 0

    for x, y, character in points:
        grid[(x, y)] = character
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    # The example defines y = 0 as the bottom row,
    # so print from the largest y down to zero.
    for y in range(max_y, -1, -1):
        row = "".join(
            grid.get((x, y), " ")
            for x in range(max_x + 1)
        )
        print(row.rstrip())


# Example:
# print_secret_grid("https://docs.google.com/document/d/...")

if __name__ == "__main__":
    url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
    print_secret_grid(url)