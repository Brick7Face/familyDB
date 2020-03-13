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

    def clearDB(self, mydb, cursor):
        #cursor.execute("DROP TABLE IF EXISTS Marriage")
        #cursor.execute("DROP TABLE IF EXISTS Person")
        cursor.execute("DELETE FROM Person")
        cursor.execute("DELETE FROM Marriage")
        mydb.commit()

    # Populate the database using the imported lists from records.py
    def populate(self, mydb, cursor):
        cursor.execute("CREATE TABLE IF NOT EXISTS Person ( PersonID INTEGER PRIMARY KEY AUTOINCREMENT, Name TINYTEXT NOT NULL, ParentsMarriageID INT, DOB DATE, DOD DATE, Birthplace TINYTEXT, Deathplace TINYTEXT, FOREIGN KEY(ParentsMarriageID) REFERENCES Marriage(MarriageID) ON DELETE CASCADE )")
        cursor.execute("CREATE TABLE IF NOT EXISTS Marriage ( MarriageID INTEGER PRIMARY KEY AUTOINCREMENT, Partner1 INT, Partner2 INT, Date DATE, FOREIGN KEY(Partner1) REFERENCES Person(PersonID) ON DELETE SET NULL, FOREIGN KEY(Partner2) REFERENCES Person(PersonID) ON DELETE SET NULL )")
        # try inserting records from records.py
        try:
            returnList = []
            sql = "INSERT INTO Person (PersonID, Name, ParentsMarriageID, DOB, DOD, Birthplace, Deathplace) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.executemany(sql, personRecords)
            returnList.append("".join([str(cursor.rowcount), " records were inserted into table Person."]))

            sql2 = "INSERT INTO Marriage (MarriageID, Partner1, Partner2, Date) VALUES (?, ?, ?, ?)"
            cursor.executemany(sql2, marriageRecords)
            returnList.append("".join([str(cursor.rowcount), " records were inserted into table Marriage."]))
            returnList.append("green")
            mydb.commit()
            return returnList
        # catch and print error if insert fails
        except ValueError as error:
            return(["ValueError:", str(error), "red"])
        # catch and print error if records already exist
        except sqlite3.IntegrityError:
            return(["Warning:", "Some records already exist.", "orange"])

    # Search the database by name, birthdate, birthplace or deathplace
    def searchDB(self, cursor, filter, record):
        exact = False
        if filter == "":
            filter = "Name"
        query = ""
        if filter == "Name":
            record = record.strip()
            query = "SELECT * FROM Person WHERE Name LIKE ? ORDER BY PersonID ASC"
        elif filter == "Birthday":
            record = record.strip()
            query = "SELECT * FROM Person WHERE DOB LIKE ?"
        elif filter == "Birthplace":
            record = record.strip()
            query = "SELECT * FROM Person WHERE Birthplace LIKE ? ORDER BY DOB ASC"
        elif filter == "Deathplace":
            record = record.strip()
            query = "SELECT * FROM Person WHERE Deathplace LIKE ? ORDER BY DOD ASC"
        elif filter == "ID":
            record = str(record)
            query = "SELECT * FROM Person WHERE PersonID = ?"
            exact = True
        else:
            return

        result = []
        if exact:
            cursor.execute(query, [ record ] )
            result = cursor.fetchall()
        else:
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
    def relate(self, id_num):
        cursor = self.cur
        mydb = self.mydb

        cursor.execute("SELECT * FROM Person WHERE PersonID = ?", [ id_num ])
        result = cursor.fetchall()
        personList = []
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            personList.append(person.toString())
        parentsList = self.getParents(cursor, id_num)
        grandparentsList = []
        for parent in parentsList:
            if (len(parent) > 0):
                gpa = self.getParents(cursor, parent[0])
                for p in gpa:
                    grandparentsList.append(p)
        return [ personList, grandparentsList, parentsList, self.getSiblings(cursor, id_num), self.getSpouse(cursor, id_num), self.getChildren(cursor, id_num) ]

    # Send back parents
    def getParents(self, cursor, id_num):
        cursor.execute("SELECT * FROM \
            (SELECT * FROM Person INNER JOIN Marriage ON PersonID=Partner1) WHERE MarriageID = \
                (SELECT ParentsMarriageID FROM Person where PersonID = ?)", [ id_num ])
        result = cursor.fetchall()
        cursor.execute("SELECT * FROM \
            (SELECT * FROM Person INNER JOIN Marriage ON PersonID=Partner2) WHERE MarriageID = \
                (SELECT ParentsMarriageID FROM Person where PersonID = ?)", [ id_num ])
        result = result + cursor.fetchall()
        parentsList = []
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            parentsList.append(person.toString())
        if (len(parentsList) < 2):
            for i in range(2 - len(parentsList)):
                parentsList.append([None, "Unknown", "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"])
        return parentsList

    # Send back siblings
    def getSiblings(self, cursor, id_num):
        cursor.execute("SELECT * FROM Person WHERE ParentsMarriageID IN \
            (SELECT MarriageID FROM Marriage WHERE Partner1 IN \
                (SELECT PersonID FROM \
                    (SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2)) WHERE MarriageID = \
                        (SELECT ParentsMarriageID FROM Person WHERE PersonID = ?)) OR Partner2 IN \
                            (SELECT PersonID FROM \
                                (SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2)) WHERE MarriageID = \
                                    (SELECT ParentsMarriageID FROM Person WHERE PersonID = ?)))", [ id_num, id_num ]) #AND PersonID != ?", [ id_num, id_num, id_num ])
        result = cursor.fetchall()

        siblingsList = []
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            siblingsList.append(person.toString())
        return siblingsList

    # Send back spouse(s)
    def getSpouse(self, cursor, id_num):
        cursor.execute("SELECT * FROM Person INNER JOIN Marriage ON (PersonID = Partner1 OR PersonID = Partner2) WHERE (Partner1 = \
            (SELECT PersonID FROM Person WHERE PersonID = ?) OR Partner2 = \
                (SELECT PersonID FROM Person WHERE PersonID = ?)) AND PersonID != ?", [ id_num, id_num, id_num ])
        result = cursor.fetchall()

        spouseList = []
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            spouseList.append(person.toString())
        return spouseList

    # Send back children
    def getChildren(self, cursor, id_num):
        cursor.execute("SELECT * FROM Person WHERE ParentsMarriageID in \
            (SELECT MarriageID FROM Marriage WHERE Partner1 = \
                (SELECT PersonID FROM Person WHERE PersonID = ?) OR Partner2 = \
                    (SELECT PersonID FROM Person WHERE PersonID = ?))", [ id_num, id_num ])
        result = cursor.fetchall()

        childList = []
        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            childList.append(person.toString())
        return childList


    # Create a record in either Person or Marriage
    def createOrUpdate(self, table, entry, create):
        cursor = self.cur
        mydb = self.mydb

        for i, attr in enumerate(entry[0:6]):
            if (attr.strip() == ""):
                entry[i] = None

        if (table == "Person"):
            if (entry[1] == None and entry[2] == None):
                if create:
                    cursor.execute("INSERT INTO Person (Name, ParentsMarriageID, DOB, DOD, Birthplace, Deathplace) VALUES (?, ?, ?, ?, ?, ?)", [ entry[0], None, entry[3], entry[4], entry[5], entry[6] ])
                else:
                    cursor.execute("UPDATE Person SET Name = ?, ParentsMarriageID = ?, DOB = ?, DOD = ?, Birthplace = ?, Deathplace = ? WHERE PersonID = ?", [ entry[0], None, entry[3], entry[4], entry[5], entry[6], entry[7] ])
            elif (entry[1] == None or entry[2] == None):
                return []
            else:
                parent1Int = False
                parent2Int = False
                try:
                    int(entry[1])
                    parent1Int = True
                except ValueError:
                    parent1Int = False
                try:
                    int(entry[2])
                    parent2Int = True
                except ValueError:
                    parent2Int = False

                parentsID = []
                if (parent1Int and parent2Int):
                    cursor.execute("SELECT MarriageID FROM Marriage WHERE Partner1 = ? AND Partner2 = ?", [ int(entry[1]), int(entry[2]) ])
                    parentsID = cursor.fetchall()
                elif (parent1Int and not parent2Int):
                    cursor.execute("SELECT MarriageID FROM Marriage WHERE Partner1 = ? AND Partner2 = (SELECT PersonID FROM Person WHERE Name = ?)", [ int(entry[1]), entry[2] ])
                    parentsID = cursor.fetchall()
                elif (parent2Int and not parent1Int):
                    cursor.execute("SELECT MarriageID FROM Marriage WHERE Partner1 = (SELECT PersonID FROM Person WHERE Name = ?) AND Partner2 = ?", [ entry[1], int(entry[2]) ])
                    parentsID = cursor.fetchall()
                else:
                    cursor.execute("SELECT MarriageID FROM Marriage WHERE Partner1 = (SELECT PersonID FROM Person WHERE Name = ?) AND Partner2 = (SELECT PersonID FROM Person WHERE Name = ?)", [ entry[1], entry[2] ])
                    parentsID = cursor.fetchall()

                if (len(parentsID) == 0):
                    return []
                else:
                    if create:
                        cursor.execute("INSERT INTO Person (Name, ParentsMarriageID, DOB, DOD, Birthplace, Deathplace) VALUES (?, ?, ?, ?, ?, ?)", [ entry[0], parentsID[0][0], entry[3], entry[4], entry[5], entry[6] ])
                    else:
                        cursor.execute("UPDATE Person SET Name = ?, ParentsMarriageID = ?, DOB = ?, DOD = ?, Birthplace = ?, Deathplace = ? WHERE PersonID = ?", [ entry[0], parentsID[0][0], entry[3], entry[4], entry[5], entry[6], entry[7] ])
            mydb.commit()

            record = []
            if create:
                cursor.execute("SELECT * FROM Person WHERE PersonID = ?", [ cursor.lastrowid ])
            else:
                cursor.execute("SELECT * FROM Person WHERE PersonID = ?", [ entry[7] ])
            record = cursor.fetchall()
            person = Person(record[0][0], record[0][1], record[0][2], record[0][3], record[0][4], record[0][5], record[0][6])
            return [ person.toString() ]
        else:
            parent1 = []
            parent2 = []
            try:
                cursor.execute("SELECT * FROM Person WHERE PersonID = ?", [ int(entry[0]) ])
                parent1 = cursor.fetchall()
            except ValueError:
                cursor.execute("SELECT * FROM Person WHERE Name = ?", [ entry[0] ])
                parent1 = cursor.fetchall()
            try:
                cursor.execute("SELECT * FROM Person WHERE PersonID = ?", [ int(entry[1]) ])
                parent2 = cursor.fetchall()
            except ValueError:
                cursor.execute("SELECT * FROM Person WHERE Name = ?", [ entry[1] ])
                parent2 = cursor.fetchall()
            if (len(parent1) == 0 or len(parent2) == 0):
                return []
            cursor.execute("INSERT INTO Marriage (Partner1, Partner2, Date) VALUES (?, ?, ?)", [ parent1[0][0], parent2[0][0], entry[2] ])
            mydb.commit()
            returnList = []
            for parent in [parent1, parent2]:
                person = Person(parent[0][0], parent[0][1], parent[0][2], parent[0][3], parent[0][4], parent[0][5], parent[0][6])
                returnList.append(person.toString())
            return returnList

    # Delete a Person record; will cascade to marriage if necessary
    def delete(self, id_num):
        cursor = self.cur
        mydb = self.mydb

        cursor.execute("SELECT * FROM Person WHERE PersonID = ?", [ id_num ])
        result = cursor.fetchall()
        if (len(result) > 0):
            person = Person(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6])
            cursor.execute("DELETE FROM Person WHERE PersonID = ?", [ id_num ])
            mydb.commit()
            return [ person.toString() ]
        else:
            return []

    # Routes requests from GUI
    def choice(self, choice, filter, entry):
        cur = self.cur
        mydb = self.mydb

        if choice == "Search":
            if (entry == ""):
                return
            return self.searchDB(cur, filter, entry)
        elif choice == "Populate":
            returnStr = self.populate(mydb, cur)
            return returnStr
        elif choice == "ClearDB":
            self.clearDB(mydb, cur)
