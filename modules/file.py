import re
from modules.highlight import Highlight

class KindleFile(object):
    
    def parse_file(self, file):
        """
            Attributes: 
                file: filename with highlights
            
            Returns: 
                lists of highlights with notes, sorted by book, start_loacation
        """
        content = file.readlines()
        content = [line.decode('utf-8-sig') for line in content]

        highlights = []
        note = None
        is_highlight = is_bookmark = False
        text = ""
        for line in content:            
            line_clean = line.strip().replace('\ufeff', '')
            # Title and Author
            if re.search(r"^(.*?)\s*\(([^)]+)\)$", line_clean):
                match = re.search(r"^(.*?)\s*\(([^)]+)\)$", line_clean)
                title = match.group(1)
                author = match.group(2)

            # Highlight
            elif re.search(r"^- Your Highlight on page (\d+) \| location (\d+)-(\d+) \| Added on (.+)$", line_clean):
                is_highlight = True # highlight
                match = re.search(r"^- Your Highlight on page (\d+) \| location (\d+)-(\d+) \| Added on (.+)$", line_clean)
                page, location_start, location_end, date_added = match.groups()

            # Note
            elif re.search(r"^- Your Note on page (\d+) \| location (\d+) \| Added on (.+)$", line_clean):
                match = re.search(r"^- Your Note on page (\d+) \| location (\d+) \| Added on (.+)$", line_clean)
                location = match.group(2)

            # Bookmark
            elif re.search(r"^- Your Bookmark on page (\d+) \| location (\d+) \| Added on (.+)$", line_clean):
                is_bookmark = True

            # Entry end
            elif line_clean == "==========":
                if is_highlight:
                    highlight = Highlight(title, author, page, location_start, location_end, date_added, text.strip())
                    if note and note[0] == title and note[1] == author and note[2] >= location_start and note[2] <= location_end:
                        highlight.note = note[3]
                        note = None
                    highlights.append(highlight)
                    is_highlight = False
                elif is_bookmark:
                    is_bookmark = False
                else: 
                    note = (title, author, location, text.strip())
                text = ""
            else:
                text += line_clean

        # sort highlights by title, location_start
        highlights_sorted = sorted(highlights, key = lambda x: (x.title, x.location_start))

        return highlights_sorted
