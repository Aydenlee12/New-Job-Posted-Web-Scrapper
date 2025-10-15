class Job:
    def __init__(self, title, company, location, link):
        self.title = title
        self.company = company
        self.location = location
        self.link = link

    def __str__(self):
        return f"**{self.title}** at {self.company}\n📍 {self.location}\n🔗 {self.link}"
