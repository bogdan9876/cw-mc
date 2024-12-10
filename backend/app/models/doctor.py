class Doctor:
    def __init__(self, id, name, position, experience, location, description=None, image=None):
        self.id = id
        self.name = name
        self.position = position
        self.experience = experience
        self.location = location
        self.description = description
        self.image = image
