import faker
import psycopg2
from datetime import datetime, timezone
import random

fake = faker.Faker()

def generate_transaction():
    user = fake.simple_profile()

    return {
        "transactionId": fake.uuid4(),
        "userId": user['username'],
        "timestamp": datetime.now(timezone.utc).timestamp(), 
        "amount": round(random.uniform(10 , 1000), 2),
        "currency": random.choice(['USD','GBP','RS']),
        "city": fake.city(),
        "country": fake.country(),
        "merchantName": fake.company(),
        "paymentMethod": random.choice(['credit_card','debit_card','online_transfer']),
        "ipAddress": fake.ipv4(),
        "voucherCode": random.choice(['','DISCOUNT10','']),
        "affiliatedId": fake.uuid4()
            }
def create_table(conn):
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions(
            transaction_id VARCHAR(255) PRIMARY KEY,
            userId VARCHAR(255),
            timestamp TIMESTAMP, 
            amount DECIMAL,
            currency VARCHAR(255),
            city VARCHAR(255),
            country VARCHAR(255),
            merchantName VARCHAR(255),
            paymentMethod VARCHAR(255),
            ipAddress VARCHAR(255),
            voucherCode VARCHAR(255),
            affiliatedId VARCHAR(255)
                )
        """)
    cursor.close()
    conn.commit()
    #conn.close()
    
if __name__ =="__main__":
    conn= psycopg2.connect(
        host = 'localhost',
        database = 'financial_db',
        user = 'postgres',
        password = 'postgres',
        port = 5432
    )

    create_table(conn)
    transaction = generate_transaction()
    #print(transaction)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO transactions(transaction_id, userId , timestamp, amount, currency, city, country, merchantName, paymentMethod, ipAddress, voucherCode, affiliatedId)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (transaction["transactionId"], transaction["userId"] , datetime.fromtimestamp(transaction["timestamp"]).strftime('%Y-%m-%d %H:%M:%S'), 
             transaction["amount"], transaction["currency"], transaction["city"], transaction["country"],
             transaction["merchantName"], transaction["paymentMethod"], transaction["ipAddress"], 
             transaction["voucherCode"], transaction["affiliatedId"])


    )

    cur.close()
    conn.commit()
    cury = conn.cursor()
    cury.execute("SELECT * FROM transactions;")
    rows = cury.fetchall()
    #for row in rows:
    print(rows)
    cury.close()
    conn.close()
