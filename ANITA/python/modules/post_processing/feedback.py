from flask import request, Response, json
import re
import pandas as pd

from database.anita.controller.FeedbackController import FeedbackController
from database.db.MySqlDB import MySqlDB

drugs_mapping = {
    'Benzodiazepines': ['benzodiazepines','klonopin', 'aprazolam','alprazolam','xanax','lorazepam', 'flunitrazolam', 'diazepam', 'valium'],
    'Cannabinoids': ['cannabis', 'weed', 'marijuana', 'hash', 'buds', 'bud', 'moonrocks','moonrock','vape','hashish', 'edibles', 'indica','concentrates', 'seeds', 'canned-buds'],
    'Stimulants': ['performance', 'cocaine', 'coke','stimulants', 'flakka', 'mdma', 'ecstacy', 'xtc', 'meth', 'crystalmeth', 'ice','yaba', 'adderall', 'adderal', 'ecstasy','n-formylamphetamine', 'amphetamine', 'iboga'],
    'Opiates/Opioids': ['opiates', 'opioid','heroin', 'herion', 'he-roin', 'he-roine','demerol', 'opana','codeine', 'oxycotin', 'oxy', 'oxycotine', 'oxycontin','fentanyl', 'fentany','hydrocodone','oxycodone', 'norco', 'methadone', 'roxicodone', 'tramadol', 'opiod', 'opium', 'subutex', 'morphine'],
    'Anabolic steroids': ['steroids', 'testosterone'],
    'Psychedelic/Dissociative Hallucinogens': ['psychedelics', 'dissociatives', 'molly', 'lsd', 'lsd-acid', 'ketamine', 'mushrooms', 'mushroom', 'shrooms', '2cb', 'dmt'],
    'Pharmaceuticals': ['phamaceutical', 'novocain', 'ritalin', 'dexedrine', 'viagra', 'percocet', 'flunitrazepam', 'albendazole', 'lyrica', 'lexapro', 'zolpidem', 'temazepam','promethazine','pharmacy', 'sidenafil','nasal', 'modafinil', 'nembutal', 'corona', 'vaccine', 'actavis']
}

no_drugs_mapping = ['passport', 'fake', 'money', 'cash', 'id', 'ids', "id's",'counterfeits','certificate', 'visa',
                    'mastercard', 'dollar', 'dollars', 'euro', 'euros', 'iphone', 'paypal', 'transfers', 'transfer',
                    'counterfeit', 'moneygram', 'bullets', 'bullet', 'hacker', 'hackers', 'bank', 'cards', 'card',
                    'covid', 'debit', 'credit', 'bitcoin', 'ps5','license','falschgeld', "bitcoin's", 'retriever']


def update_feedback():
    try:
        feedback_controller = FeedbackController()
        data = feedback_controller.get_feedback_vendor()

        df = pd.DataFrame(data, columns=['feedback_id', 'id', 'name', 'message', 'product', 'deals', 'market', 'timestamp'])
        df = df.drop_duplicates(subset=['message', 'timestamp', 'market', 'product', 'name', 'deals'])
        df['macro_category'] = None

        # Import product data to map the reviews to the product that is bought
        data_products = get_data_products()

        df_product = pd.DataFrame(data_products, columns=['product', 'macro_category'])
        product_category_dict = df_product.set_index('product').to_dict()['macro_category']

        # Append macro-category to each review
        df = add_macro_category(df, product_category_dict)

        final_data = [tuple(x) for x in df.to_numpy()]
        insert_data(final_data)
    except Exception as e:
        return False

    return True


def delete_feedback():
    mysql_db = MySqlDB("anita")

    query = "DELETE FROM anita.`reviews`"
    mysql_db.delete(query)

    return True


def get_data_products():
    mysql_db = MySqlDB("anita")
    query = "SELECT products_cleaned.name, products_cleaned.macro_category FROM anita.products_cleaned;"

    header, results = mysql_db.search(query)

    return results


def add_macro_category(df, product_category_dict):
    # All right macro-categories are appended to every review
    for i, row in df.iterrows():
        product_found = False
        # If a review is from Cannazon it is known that it is a Cannabis product
        if row[6] == 'cannazon':
            df.at[i, 'macro_category'] = 'Cannabinoids'
            product_found = True
            continue
        else:
            # If there is no product mentioned, the loop can be exited
            if row[4] == None:
                df.at[i, 'macro_category'] = 'Unknown'
                product_found = True
                continue
            else:
                # Check whether the drug name is already present in the drug mapping in the table
                product = row[4]
                for product_name, category in product_category_dict.items():
                    if product == product_name:
                        df.at[i, 'macro_category'] = category
                        product_found = True
                        continue
                if product_found != True:
                    product_lower = row[4].lower().split(' ')
                    drug_title_stripped = [x.strip(',') for x in product_lower]
                    drug_title_split = [x.split(',') for x in drug_title_stripped]
                    drug_title_split = [x for y in drug_title_split for x in y]
                    for key, value in drugs_mapping.items():
                        for word in drug_title_split:
                            if word in value:
                                df.at[i, 'macro_category'] = key
                                product_found = True
                                break
                        else:
                            continue
                        break
                if product_found != True:
                    for word in drug_title_split:
                        if word in no_drugs_mapping:
                            df.at[i, 'macro_category'] = 'No drugs'
                            product_found = True
                            break
                if product_found != True:
                    df.at[i, 'macro_category'] = 'Unknown'

    return df


def insert_data(data):
    mysql_db = MySqlDB("anita")
    query = "INSERT INTO anita.`reviews` (`feedback_id`, `id`, `name`, `message`,`product`, `deals`, `market`, " \
            "`timestamp`, `macro_category`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    mysql_db.insert(query, data)