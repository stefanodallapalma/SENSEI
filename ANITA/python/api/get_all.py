from database.anita.AnitaDB import AnViProDB

db_parameters_path = "../resources/db_parameters"

def get_data():
    db = AnViProDB(db_parameters_path)

    products = db.getProducts()
    vendors = db.getVendors()
