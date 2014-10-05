import string
from itertools import permutations

NAMES = ["Smith","Anderson","Clark","Wright","Mitchell","Johnson","Thomas",
"Rodriguez","Lopez","Perez","Williams","Jackson","Lewis","Hill","Roberts","Jones",
"White","Lee","Scott","Turner","Brown","Harris","Walker","Green","Phillips","Davis",
"Martin","Hall","Adams","Campbell","Miller","Thompson","Allen","Baker","Parker",
"Wilson","Garcia","Young","Gonzalez","Evans","Moore","Martinez","Hernandez","Nelson",
"Edwards","Taylor","Robinson","King","Carter","Collin","Minh","Anh"]

ORGANIZATION_NAMES = list(string.ascii_uppercase)

PHONE_TESTING = [''.join(p) for p in permutations(string.digits)][:len(ORGANIZATION_NAMES)]

PROJECT_TESTING = ["".join(x) for x in permutations(string.ascii_uppercase[:15], 2)][:78]