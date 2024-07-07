class Highlight(object):

    def __init__(self, title, author, page, location_start, location_end, date_added, text):
        self.title = title
        self.author = author
        self.page = int(page)
        self.location_start = int(location_start)
        self.location_end = int(location_end)
        self.added_date = date_added
        self.highlight = text
        self.note = ""
    
    def __str__(self):
        return f"{self.title} ({self.author})\npage: {self.page} ({self.location_start} - {self.location_end}), added: {self.added_date}\ntext: {self.highlight}note: {self.note}\n" 