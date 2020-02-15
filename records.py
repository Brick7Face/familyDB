# incomplete - dates are not complete, birth and deathplaces need updated

# PersonID INT, Name TINYTEXT NOT NULL, ParentsMarriageID INT, DOB DATE, DOD DATE, Birthplace TINYTEXT, Deathplace TINYTEXT
personRecords = [

    ( 1, 'Queen Victoria', None, '1819-05-24', '1901-01-22', 'Kensington Palace, London', 'Osborne House, Isle of Wight' ),
    ( 2, 'Princess Alexandra of Denmark', None, '1844-00-00', '1925-00-00', 'Unknown', 'Unknown' ),
    ( 3, 'Queen Mary', None, '1867-00-00', '1953-00-00', 'Unknown', 'Unknown' ),
    ( 4, 'Mrs. Simpson', None, '1896-00-00', '1986-00-00', 'Unknown', 'Unknown' ),
    ( 5, 'Lady Elizabeth Bowes-Lyon', None, '1900-00-00', '2002-00-00', 'Unknown', 'Unknown' ),
    ( 6, 'Queen Elizabeth II', 5, '1926-00-00', None, 'Unknown', None ),
    ( 7, 'Princess Margaret', 5, '1930-00-00', '2002-00-00', 'Unknown', 'Unknown' ),
    ( 8, 'Lady Diana Spencer', None, '1961-00-00', '1997-00-00', 'Unknown', 'Unknown' ),
    ( 9, 'Princess Anne', 6, '1950-00-00', None, 'Unknown', None ),
    ( 10, 'Catherine Middleton', None, '1982-00-00', None, 'Unknown', None ),
    ( 11, 'Prince Albert', None, '1819-08-26', '1861-12-14', 'Schloss Rosenau, Coburg, German Confederation', 'Windsor Castle, Endland' ),
    ( 12, 'King Edward VII', 1, '1841-11-09', '1910-05-06', 'Buckingham Palace, London', 'Buckingham Palace, London' ),
    ( 13, 'King George V', 2, '1865-00-00', '1936-00-00', 'Unknown', 'Unknown' ),
    ( 14, 'King Edward VIII', 3, '1894-00-00', '1972-00-00', 'Unknown', 'Unknown' ),
    ( 15, 'King George VI', 3, '1895-00-00', '1952-00-00', 'Unknown', 'Unknown' ),
    ( 16, 'Prince Philip', None, '1921-00-00', None, 'Unknown', None ),
    ( 17, 'Prince Charles', 6, '1948-00-00', None, 'Unknown', None ),
    ( 18, 'Prince Andrew', 6, '1960-00-00', None, 'Unknown', None ),
    ( 19, 'Prince Edward', 6, '1964-00-00', None, 'Unknown', None ),
    ( 20, 'Prince William', 7, '1982-00-00', None, 'Unknown', None ),
    ( 21, 'Prince Henry', 7, '1984-00-00', None, 'Unknown', None ),
    ( 22, 'Prince George', 8, '2013-00-00', None, 'Unknown', None ),
    ( 23, 'Princess Charlotte', 8, '2015-00-00', None, 'Unknown', None ),
    ( 24, 'Viscount Linley', 9, '1961-00-00', None, 'Unknown', None ),
    ( 25, 'Lady Sarah Chatto', 9, '1964-00-00', None, 'Unknown', None ),
    ( 26, 'Antony Armstrong-Jones', None, '1930-00-00', '2017-00-00', 'Unknown', 'Unknown' ),

]

# MarriageID INT, Partner1 INT, Partner2 INT, Date DATE
marriageRecords = [
    ( 1, 11, 1, '1840-02-10' ),     # albert and victoria
    ( 2, 12, 2, None ),             # edward 7 and alexandra
    ( 3, 13, 3, None ),             # george 5 and mary
    ( 4, 14, 4, None ),             # edward 8 and simpson
    ( 5, 15, 5, None ),             # george 6 and liz bowes-lyon
    ( 6, 16, 6, None ),             # philip and liz 2
    ( 7, 17, 8, None ),             # charles and diana
    ( 8, 20, 10, None ),            # william and kate
    ( 9, 26, 7, None )              # antony and margaret
]
