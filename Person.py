class Person:

    def __init__(self, id, name, parentsMarriageID, dob, dod, birthplace, deathplace):
        self.id = id
        self.name = name
        self.parentsMarriageID = parentsMarriageID
        self.dob = dob
        if (dod==None):
            self.dod = "Alive"
        else:
            self.dod = dod
        self.birthplace = birthplace
        if (deathplace==None):
            self.deathplace = ""
        else:
            self.deathplace = deathplace

    def displayPerson(self):
        print("Name:", self.name, "\nBorn:", self.dob, "in", self.birthplace, "\nDied:", self.dod, self.deathplace)
        print("-----------")
