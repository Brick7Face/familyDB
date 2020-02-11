from PyInquirer import Separator

menuQuestions = [
{
    'type': 'list',
    'name': 'choice',
    'message': 'Select an option:',
    'choices': [
        'Search',
        'Family',
        'Populate database',
        Separator(),
        'Exit'
    ]
},
]

searchQuestions = [
{
    'type': 'list',
    'name': 'choice',
    'message': 'Select search criteria:',
    'choices': [
        'Name',
        'Birthday',
        'Birthplace',
        'Deathplace',
        Separator(),
        'Return'
    ]
},
]
