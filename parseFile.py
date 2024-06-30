import re

class Highlight(object):

    def __init__(self, title, author, page, location_start, location_end, date_added, text):
        self.title = title
        self.author = author
        self.page = page
        self.location_start = location_start
        self.location_end = location_end
        self.added_date = date_added
        self.highlight = text
        self.note = ""
    
    def __str__(self):
        return f"{self.title} ({self.author})\npage: {self.page} ({self.location_start} - {self.location_end}), added: {self.added_date}\ntext: {self.highlight}note: {self.note}\n" 
    
def parseFile(filename):
    """
        param: file
        return: lists of highlights with notes
    """

    with open(filename) as file:
        content = file.readlines()
        highlights = []
        note = None
        is_highlight = is_bookmark = False
        text = ""
        for line in content:            
            if line.strip():
                # Title and Author
                if re.search(r"^(.*?)\s*\(([^)]+)\)$", line):
                    match = re.search(r"^(.*?)\s*\(([^)]+)\)$", line)
                    title = match.group(1)
                    author = match.group(2)

                # Highlight
                elif re.search(r"^- Your Highlight on page (\d+) \| location (\d+)-(\d+) \| Added on (.+)$", line):
                    is_highlight = True # highlight
                    match = re.search(r"^- Your Highlight on page (\d+) \| location (\d+)-(\d+) \| Added on (.+)$", line)
                    page, location_start, location_end, date_added = match.groups()

                # Note
                elif re.search(r"^- Your Note on page (\d+) \| location (\d+) \| Added on (.+)$", line):
                    match = re.search(r"^- Your Note on page (\d+) \| location (\d+) \| Added on (.+)$", line)
                    location = match.group(2)

                # Bookmark
                elif re.search(r"^- Your Bookmark on page (\d+) \| location (\d+) \| Added on (.+)$", line):
                    is_bookmark = True

                # Entry end
                elif line == "==========\n":
                    if is_highlight:
                        highlight = Highlight(title, author, page, location_start, location_end, date_added, text)
                        if note and note[0] == title and note[1] == author and note[2] >= location_start and note[2] <= location_end:
                            highlight.note = note[3]
                            note = None
                        highlights.append(highlight)
                        is_highlight = False
                    elif is_bookmark:
                        is_bookmark = False
                    else: 
                        note = (title, author, location, text)
                    text = ""
                else:
                    text += line

    return highlights

highlights = parseFile("My Clippings.txt")

for highlight in highlights:
    print(highlight)


