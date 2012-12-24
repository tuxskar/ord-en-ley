import random
import string
import ordenley.tests
import ordenley.models.Models

def random_client():
    name = ordenley.tests.random_string()
    surname = ordenley.tests.random_string()
    dni = ordenley.tests.random_string(9)
    web = ordenley.tests.random_string()
    email = ordenley.tests.random_string()
    client = ordenley.models.Models.Client(
            name = name,
            surname = surname,
            web = web,
            email = email,
            dni = dni)
    return client

def random_string(length=15):
    s = ""
    for n in range(length):
        s += random.choice(string.ascii_letters + string.digits)
    return s
