import mysql.connector
import random
from data.db import get_connection
from datetime import datetime, timedelta

# Connexion à MySQL
conn = get_connection()
cursor = conn.cursor()

# Données exemples
customers = ["Alice Martin", "Bob Dupont", "Chloé Bernard", "David Leroy"]
products = ["Téléphone", "Ordinateur portable", "Imprimante", "Clé USB"]
addresses = [
    "10 rue de Paris, Lyon",
    "25 boulevard Haussmann, Paris",
    "3 avenue Jean Jaurès, Toulouse",
    "8 rue Victor Hugo, Lille"
]
payment_methods = ["Carte bancaire", "Paypal", "Espèces", "Virement"]

# Génération et insertion de plusieurs lignes
for i in range(10):
    data = {
        "customer_name": random.choice(customers),
        "delivery_address": random.choice(addresses),
        "start_address": random.choice(addresses),
        "weight": round(random.uniform(0.5, 10.0), 2),
        "product": random.choice(products),
        "delivery_date": int((datetime.today() + timedelta(days=random.randint(1, 10))).strftime("%Y%m%d")),
        "payment_method": random.choice(payment_methods),
        "price": round(random.uniform(50.0, 1500.0), 2)
    }

    query = """
        INSERT INTO orders (
            customer_name, delivery_address, start_address,
            weight, product, delivery_date, payment_method, price
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = tuple(data.values())
    cursor.execute(query, values)

conn.commit()
cursor.close()
conn.close()

print("✅ 10 commandes insérées avec succès dans la base MySQL.")
