import sqlite3
import time
from familyDBRecords.records import personRecords, marriageRecords
from Person import Person

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
        cursor.execute("CREATE TABLE IF NOT EXISTS Person ( PersonID INT, Name TINYTEXT NOT NULL, ParentsMarriageID INT, DOB DATE, DOD DATE, Birthplace TINYTEXT, Deathplace TINYTEXT, PRIMARY KEY (PersonID), FOREIGN KEY(ParentsMarriageID) REFERENCES Marriage(MarriageID) )")
        cursor.execute("CREATE TABLE IF NOT EXISTS Marriage ( MarriageID INT, Partner1 INT, Partner2 INT, Date DATE, PRIMARY KEY (MarriageID), FOREIGN KEY(Partner1) REFERENCES Person(PersonID), FOREIGN KEY(Partner2) REFERENCES Person(PersonID) )")

        try:
            sql = "INSERT INTO Person (PersonID, Name, ParentsMarriageID, DOB, DOD, Birthplace, Deathplace) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.executemany(sql, personRecords)
            print(cursor.rowcount, " records were inserted into table Person.")

            sql2 = "INSERT INTO Marriage (MarriageID, Partner1, Partner2, Date) VALUES (?, ?, ?, ?)"
            cursor.executemany(sql2, marriageRecords)
            print(cursor.rowcount, " records were inserted into table Marriage.")
        except (ValueError):
            print("ValueError: check the entries in your records file.")

    # Search the database by name, birthdate, birthplace or deathplace
    def searchDB(self, cursor, filter, record):
        print("\n")
        if filter=="":
            filter = "Name"
        query = ""
        if filter=="Name":
            query = "SELECT * FROM Person WHERE Name LIKE \'%" + record + "%\'"
        elif filter=="Birthday":
            query = "SELECT * FROM Person WHERE DOB = \'" + record + "\'"
        elif filter=="Birthplace":
            query = "SELECT * FROM Person WHERE Birthplace LIKE \'%" + record + "%\'"
        elif filter=="Deathplace":
            query = "SELECT * FROM Person WHERE Deathplace LIKE \'%" + record + "%\'"
        elif filter=="Return":
            return

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result)==0:
                print("No results.")
            for record in result:
                person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
                person.displayPerson()  # return this string for printing to window
        except (ValueError):
            print("ValueError: check the entries in your records file.")
        print("\n")

    # Print the family of an inputted person by name
    def relate(self, cursor, person1):
        cursor.execute("SELECT * FROM Person WHERE Name = \'" + person1 + "\'")
        result = cursor.fetchall()
        if len(result)==0:
            print("That person does not exist in the database. Try again.")
            return

        print("\n====== GRANDPARENTS =====")

        cursor.execute("SELECT * FROM \
            (SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2)) WHERE MarriageID in \
                (SELECT ParentsMarriageID from \
                    (SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2)) WHERE MarriageID = \
                        (SELECT ParentsMarriageID FROM Person where Name = \'" + person1 + "\'))")
        result = cursor.fetchall()

        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            person.displayPerson()

        print("\n====== PARENTS =====")

        cursor.execute("SELECT * FROM \
            (SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2)) WHERE MarriageID = \
                (SELECT ParentsMarriageID FROM Person where Name = \'" + person1 + "\')")
        result = cursor.fetchall()

        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            person.displayPerson()

        print("\n====== SIBLINGS =====")

        cursor.execute("SELECT * FROM Person WHERE ParentsMarriageID IN ( \
            SELECT MarriageID FROM Marriage WHERE Partner1 IN ( \
                SELECT PersonID FROM ( \
                    SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2)) WHERE MarriageID = ( \
                        SELECT ParentsMarriageID FROM Person WHERE Name = \'" + person1 + "\')) OR Partner2 IN ( \
                            SELECT PersonID FROM ( \
                                SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2)) WHERE MarriageID = ( \
                                    SELECT ParentsMarriageID FROM Person WHERE Name = \'" + person1 + "\'))) AND Name != \'" + person1 + "\'")
        result = cursor.fetchall()

        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            person.displayPerson()

        print("\n====== SPOUSE(S) =====")

        cursor.execute("SELECT * FROM Person INNER JOIN Marriage ON (PersonID=Partner1 OR PersonID=Partner2) WHERE (Partner1=( \
            SELECT PersonID FROM Person WHERE Name=\'" + person1 + "\') OR Partner2=( \
                SELECT PersonID FROM Person WHERE Name=\'" + person1 + "\')) AND Name!=\'" + person1 + "\'")
        result = cursor.fetchall()

        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            person.displayPerson()

        print("\n====== CHILDREN =====")

        cursor.execute("SELECT * FROM Person WHERE ParentsMarriageID in ( \
            SELECT MarriageID FROM Marriage WHERE Partner1 = ( \
                SELECT PersonID FROM Person WHERE Name = \'" + person1 + "\') OR Partner2 = ( \
                    SELECT PersonID FROM Person WHERE Name = \'" + person1 + "\'))")
        result = cursor.fetchall()

        for record in result:
            person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
            person.displayPerson()

        print("\n")

        # Aunts/uncles - select * from Person where ParentsMarriageID in (select parentsMarriageID from (select * from Person inner join Marriage on (PersonID=Partner1 or PersonID=Partner2)) where MarriageID = (select parentsMarriageID from Person where Name = \'" + person1 + "\'));


    def choice(self, choice, filter, record):
        cur = self.cur
        mydb = self.mydb

        if choice=="Search":
            self.searchDB(cur, filter, record)

        if choice=="Family":
            self.relate(cur, record)

        elif choice=="Populate":
            self.populate(cur)
            mydb.commit()
            print("\n")
