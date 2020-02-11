from datetime import date as dt

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
        self.age = self.calcAge(dob, dod)

    def displayPerson(self):
        print("Name:", self.name, "\nBorn:", self.dob, "in", self.birthplace, "\nDied:", self.dod, self.deathplace, "(Age", str(self.age) + ")")
        print("-----------")

    def calcAge(self, dob, dod):
        age = None
        if (dod==None):
            dobStr = dob.split("-")
            if (dobStr[0]=='0000'):
                return age
            ageDT = dt.today() - dt(int(dobStr[0]), int(dobStr[1]), int(dobStr[2]))
            age = int(ageDT.days / 365.25)
        else:
            dobStr = dob.split("-")
            dodStr = dod.split("-")
            if (dobStr[0]=='0000' or dodStr[0]=='0000'):
                return age
            ageDT = dt(int(dodStr[0]), int(dodStr[1]), int(dodStr[2])) - dt(int(dobStr[0]), int(dobStr[1]), int(dobStr[2]))
            age = int(ageDT.days / 365.25)
        return age
