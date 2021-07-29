from flask import request, Response, json
from faker import Faker

from database.db.MySqlDB import MySqlDB


def update_pseudonym():
    try:
        vendor_names = get_vendor_platform_name()

        alias, pseudonym = generate_pseudonyms(vendor_names)
        insert_data(list(zip(alias, pseudonym)))
    except:
        return False

    return True


def delete_pseudonym():
    mysql_db = MySqlDB("anita")

    query = "DELETE FROM anita.`pseudonymized_vendors`"
    mysql_db.delete(query)

    return True


def get_vendor_platform_name():
    mysql_db = MySqlDB("anita")
    query = "SELECT DISTINCT(name) FROM anita.`vendor-analysis`;"
    header, results = mysql_db.search(query)

    return results


def generate_pseudonyms(data):
    fake = Faker()

    # Loop through the nested list and store the real alias together with the fake one
    real_alias_fake_alias = {}
    for real_alias in data:
        real_alias_fake_alias[real_alias[0]] = fake.name()

    alias = list(real_alias_fake_alias.keys())
    pseudonym = list(real_alias_fake_alias.values())

    return alias, pseudonym


def insert_data(data):
    mysql_db = MySqlDB("anita")
    query = "INSERT INTO anita.pseudonymized_vendors (`alias`, `pseudonym`) VALUES (%s,%s)"

    mysql_db.insert(query, data)