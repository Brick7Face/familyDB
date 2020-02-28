import sqlite3
import time
from records import personRecords, marriageRecords
from person import Person

class FamilyDB:

    def __init__(self):
        self.mydb = self.connect()
        self.cur = self.mydb.cursor()

    # Connect to/create the sqlite3 database
    def connect(self):
        sqlDB = sqlite3.connect('family.db')
        return sqlDB

    # Populate the database using the imported lists from records.py
    def populate(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS Marriage")
        cursor.execute("DROP TABLE IF EXISTS Person")
        time.sleep(1)
        cursor.execute("CREATE TABLE IF NOT EXISTS Person ( PersonID INTEGER PRIMARY KEY AUTOINCREMENT, Name TINYTEXT NOT NULL, ParentsMarriageID INT, DOB DATE, DOD DATE, Birthplace TINYTEXT, Deathplace TINYTEXT, FOREIGN KEY(ParentsMarriageID) REFERENCES Marriage(MarriageID) ON DELETE CASCADE )")
        cursor.execute("CREATE TABLE IF NOT EXISTS Marriage ( MarriageID INTEGER PRIMARY KEY AUTOINCREMENT, Partner1 INT, Partner2 INT, Date DATE, FOREIGN KEY(Partner1) REFERENCES Person(PersonID) ON DELETE SET NULL, FOREIGN KEY(Partner2) REFERENCES Person(PersonID) ON DELETE SET NULL )")

        try:
            returnList = []
            sql = "INSERT INTO Person (PersonID, Name, ParentsMarriageID, DOB, DOD, Birthplace, Deathplace) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.executemany(sql, personRecords)
            returnList.append("".join([str(cursor.rowcount), " records were inserted into table Person."]))

            sql2 = "INSERT INTO Marriage (MarriageID, Partner1, Partner2, Date) VALUES (?, ?, ?, ?)"
            cursor.executemany(sql2, marriageRecords)
            returnList.append("".join([str(cursor.rowcount), " records were inserted into table Marriage."]))
            return returnList
        except ValueError as error:
            return(["ValueError:", error])

    # Search the database by name, birthdate, birthplace or deathplace
    def searchDB(self, cursor, filter, record):
        if filter=="":
            filter = "Name"
        query = ""
        if filter=="Name":
            query = "SELECT * FROM Person WHERE Name LIKE ? ORDER BY PersonID ASC"
        elif filter=="Birthday":
            query = "SELECT * FROM Person WHERE DOB LIKE ?"
        elif filter=="Birthplace":
            query = "SELECT * FROM Person WHERE Birthplace LIKE ? ORDER BY DOB ASC"
        elif filter=="Deathplace":
            query = "SELECT * FROM Person WHERE Deathplace LIKE ? ORDER BY DOD ASC"
        elif filter=="Return":
            return

        cursor.execute(query, [ "%" + record + "%" ])
        result = cursor.fetchall()
        personList = []
        if len(result)==0:
            return
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            personList.append(person.toString())
        return personList

    # Send back family information for a person given Name
    def relate(self, name):
        cursor = self.cur
        mydb = self.mydb

        cursor.execute("SELECT * FROM Person WHERE Name = ?", [ name ])
        result = cursor.fetchall()
        personList = []
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            personList.append(person.toString())
        parentsList = self.getParents(cursor, name)
        grandparentsList = []
        for parent in parentsList:
            if (len(parent) > 0):
                gpa = self.getParents(cursor, parent[1])
                for p in gpa:
                    grandparentsList.append(p)
        return [ personList, grandparentsList, parentsList, self.getSiblings(cursor, name), self.getSpouse(cursor, name), self.getChildren(cursor, name) ]

    # Send back parents
    def getParents(self, cursor, name):
        cursor.execute("SELECT * FROM \
            (SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2)) WHERE MarriageID = \
                (SELECT ParentsMarriageID FROM Person where Name = ?)", [ name ])
        result = cursor.fetchall()
        parentsList = []
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            parentsList.append(person.toString())
        if (len(parentsList) < 2):
            for i in range(2 - len(parentsList)):
                parentsList.append([None, "Unknown", "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"])
        return parentsList

    # Send back siblings
    def getSiblings(self, cursor, name):
        cursor.execute("SELECT * FROM Person WHERE ParentsMarriageID IN \
            (SELECT MarriageID FROM Marriage WHERE Partner1 IN \
                (SELECT PersonID FROM \
                    (SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2)) WHERE MarriageID = \
                        (SELECT ParentsMarriageID FROM Person WHERE Name = ?)) OR Partner2 IN \
                            (SELECT PersonID FROM \
                                (SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2)) WHERE MarriageID = \
                                    (SELECT ParentsMarriageID FROM Person WHERE Name = ?)))", [ name, name ]) #AND Name != ?", [ name, name, name ])
        result = cursor.fetchall()

        siblingsList = []
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            siblingsList.append(person.toString())
        return siblingsList

    # Send back spouse(s)
    def getSpouse(self, cursor, name):
        cursor.execute("SELECT * FROM Person INNER JOIN Marriage ON (PersonID = Partner1 OR PersonID = Partner2) WHERE (Partner1 = \
            (SELECT PersonID FROM Person WHERE Name = ?) OR Partner2 = \
                (SELECT PersonID FROM Person WHERE Name = ?)) AND Name != ?", [ name, name, name ])
        result = cursor.fetchall()

        spouseList = []
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            spouseList.append(person.toString())
        return spouseList

    # Send back children
    def getChildren(self, cursor, name):
        cursor.execute("SELECT * FROM Person WHERE ParentsMarriageID in \
            (SELECT MarriageID FROM Marriage WHERE Partner1 = \
                (SELECT PersonID FROM Person WHERE Name = ?) OR Partner2 = \
                    (SELECT PersonID FROM Person WHERE Name = ?))", [ name, name ])
        result = cursor.fetchall()

        childList = []
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            childList.append(person.toString())
        return childList

        # Aunts/uncles - select * from Person where ParentsMarriageID in (select parentsMarriageID from (select * from Person inner join Marriage on (PersonID=Partner1 or PersonID=Partner2)) where MarriageID = (select parentsMarriageID from Person where Name = \'" + person1 + "\'));

    # Create a record in either Person or Marriage
    def create(self, table, entry):
        cursor = self.cur
        mydb = self.mydb

        for i, attr in enumerate(entry):
            if (attr == "None"):
                entry[i] = None

        if (table == "Person"):
            cursor.execute("SELECT MarriageID FROM Marriage WHERE Partner1 = (SELECT PersonID FROM Person WHERE Name = ?) AND Partner2 = (SELECT PersonID FROM Person WHERE Name = ?)", [ entry[1], entry[2] ])
            parentsID = cursor.fetchall()
            if (len(parentsID) == 0):
                cursor.execute("INSERT INTO Person (Name, ParentsMarriageID, DOB, DOD, Birthplace, Deathplace) VALUES (?, ?, ?, ?, ?, ?)", [ entry[0], None, entry[3], entry[4], entry[5], entry[6] ])
            else:
                cursor.execute("INSERT INTO Person (Name, ParentsMarriageID, DOB, DOD, Birthplace, Deathplace) VALUES (?, ?, ?, ?, ?, ?)", [ entry[0], parentsID[0][0], entry[3], entry[4], entry[5], entry[6] ])
            mydb.commit()
            cursor.execute("SELECT * FROM Person WHERE Name = ?", [ entry[0] ])
            record = cursor.fetchall()
            person = Person(record[0][0], record[0][1], record[0][2], record[0][3], record[0][4], record[0][5], record[0][6])
            return [ person.toString() ]
        else:
            cursor.execute("SELECT * FROM Person WHERE Name = ?", [ entry[1] ])
            parent1 = cursor.fetchall()
            cursor.execute("SELECT * FROM Person WHERE Name = ?", [ entry[2] ])
            parent2 = cursor.fetchall()
            cursor.execute("INSERT INTO Marriage (Partner1, Partner2, Date) VALUES (?, ?, ?)", [ parent1[0][0], parent2[0][0], entry[2] ])
            mydb.commit()
            returnList = []
            for parent in [parent1, parent2]:
                person = Person(parent[0][0], parent[0][1], parent[0][2], parent[0][3], parent[0][4], parent[0][5], parent[0][6])
                returnList.append(person.toString())
            return returnList

    # Delete a Person record; will cascade to marriage if necessary
    def delete(self, name):
        cursor = self.cur
        mydb = self.mydb

        cursor.execute("SELECT * FROM Person WHERE Name = ?", [ name ])
        result = cursor.fetchall()
        if (len(result) > 0):
            person = Person(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6])
            cursor.execute("DELETE FROM Person WHERE Name = ?", [ name ])
            return [ person.toString() ]
        else:
            return []

    # Routes requests from GUI
    def choice(self, choice, filter, entry):
        cur = self.cur
        mydb = self.mydb

        entry = entry.strip()

        if choice=="Search":
            if (entry==""):
                return
            return self.searchDB(cur, filter, entry)
        elif choice=="Populate":
            returnStr = self.populate(cur)
            mydb.commit()
            return returnStr
