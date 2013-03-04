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

def random_address():
    street      = ordenley.tests.random_string()
    number      = random_number()
    city        = ordenley.tests.random_string()
    state       = ordenley.tests.random_string()
    country     = ordenley.tests.random_string()
    postal_code = random_number(5)
    address = ordenley.models.Models.Addres(
        street      = street,
        number      = number,
        city        = city,
        state       = state,
        country     = country,
        postal_code = postal_code)
    return address

def random_string(length=15):
    s = ""
    for n in range(length):
        s += random.choice(string.ascii_letters + string.digits)
    return s

def random_number(length=3):
    s = 0 
    for n in range(length):
        s += 10 ** n * int(random.choice(string.digits))
    return s
