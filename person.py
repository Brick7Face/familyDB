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

    # print a Person's profile
    def displayPerson(self):
        print("Record #", self.id, "\nName:", self.name, "\nBorn:", self.dob, "in", self.birthplace, "\nDied:", self.dod, self.deathplace, "(Age", str(self.age) + ")")
        print("-----------") 

    # calculate the age in years and return it as an int
    def calcAge(self, dob, dod):
        age = None
        dobStr = dob.split("-")
        if (dobStr[0]=='0000'):
            return age
        if (dobStr[1]=='00'):
            dobStr[1] = '01'
        if (dobStr[2]=='00'):
            dobStr[2] = '01'
        if (dod==None):
            ageDT = dt.today() - dt(int(dobStr[0]), int(dobStr[1]), int(dobStr[2]))
            age = int(ageDT.days / 365.25)
        else:
            dodStr = dod.split("-")
            if (dobStr[0]=='0000' or dodStr[0]=='0000'):
                return age
            if (dodStr[1]=='00'):
                dodStr[1] = '01'
            if (dodStr[2]=='00'):
                dodStr[2] = '01'
            ageDT = dt(int(dodStr[0]), int(dodStr[1]), int(dodStr[2])) - dt(int(dobStr[0]), int(dobStr[1]), int(dobStr[2]))
            age = int(ageDT.days / 365.25)
        return age
