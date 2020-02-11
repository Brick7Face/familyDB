import sqlite3
import os, time
from examples import custom_style_2
from pyfiglet import Figlet
from PyInquirer import style_from_dict, Token, prompt
from records import personRecords, marriageRecords
from questions import menuQuestions, searchQuestions
from Person import Person

# Print the menu using PyInquirer package
def printMenu(options):
    questions = options
    answers = prompt(questions, style=custom_style_2)
    return answers['choice']

def connect():
    sqlDB = sqlite3.connect('family.db')
    return sqlDB

def populate(cursor):
    cursor.execute("DROP TABLE IF EXISTS Marriage")
    cursor.execute("DROP TABLE IF EXISTS Person")
    time.sleep(1)
    cursor.execute("CREATE TABLE IF NOT EXISTS Person ( PersonID INT, Name TINYTEXT NOT NULL, ParentsMarriageID INT, DOB DATE, DOD DATE, Birthplace TINYTEXT, Deathplace TINYTEXT, PRIMARY KEY (PersonID), FOREIGN KEY(ParentsMarriageID) REFERENCES Marriage(MarriageID) )")
    cursor.execute("CREATE TABLE IF NOT EXISTS Marriage ( MarriageID INT, Partner1 INT, Partner2 INT, Date DATE, PRIMARY KEY (MarriageID), FOREIGN KEY(Partner1) REFERENCES Person(PersonID), FOREIGN KEY(Partner2) REFERENCES Person(PersonID) )")

    sql = "INSERT INTO Person (PersonID, Name, ParentsMarriageID, DOB, DOD, Birthplace, Deathplace) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.executemany(sql, personRecords)
    print(cursor.rowcount, " records were inserted into table Person.")

    sql2 = "INSERT INTO Marriage (MarriageID, Partner1, Partner2, Date) VALUES (?, ?, ?, ?)"
    cursor.executemany(sql2, marriageRecords)
    print(cursor.rowcount, " records were inserted into table Marriage.")

def searchDB(cursor, filter):
    print("\n")
    if filter=="":
        filter = printMenu(searchQuestions)
    record = ""
    query = ""
    if filter=="Name":
        record = input("Input name > ")
        query = "SELECT * FROM Person WHERE Name LIKE \'%" + record + "%\'"
    elif filter=="Birthday":
        record = input("Input birthday (YYYY-MM-DD) > ")
        query = "SELECT * FROM Person WHERE DOB = \'" + record + "\'"
    elif filter=="Birthplace":
        record = input("Input birthplace > ")
        query = "SELECT * FROM Person WHERE Birthplace LIKE \'%" + record + "%\'"
    elif filter=="Deathplace":
        record = input("Input deathplace > ")
        query = "SELECT * FROM Person WHERE Deathplace LIKE \'%" + record + "%\'"
    elif filter=="Return":
        return

    cursor.execute(query)
    result = cursor.fetchall()
    print("\n\n===========")
    for record in result:
        person = Person(record[0], record[1], record[2], record[3], record[4], record[5], record[6])
        person.displayPerson()
    print("\n")

def relate(cursor):
    proceed = False
    person1 = ""
    while proceed==False:
        person1 = input("Input full name > ")
        cursor.execute("SELECT * FROM Person WHERE Name = \'" + person1 + "\'")
        result = cursor.fetchall()
        if len(result)==0:
            print("That person does not exist in the database. Try again.")
        else:
            proceed = True

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


def main():
    mydb = connect()
    cur = mydb.cursor()

    print("\n=========================================================================================")
    fig = Figlet(font='small')
    print(fig.renderText('PySQL'))

    choice = printMenu(menuQuestions)

    while choice:

        if choice=="Search":
            searchDB(cur, "")
            choice=printMenu(menuQuestions)

        if choice=="Family":
            relate(cur)
            choice=printMenu(menuQuestions)

        elif choice=="Populate database":
            populate(cur)
            mydb.commit()
            print("\n")
            choice=printMenu(menuQuestions)

        elif choice=='Exit':
            print("\n=========================================================================================\n")
            choice=False



if __name__ == '__main__':
    main()
