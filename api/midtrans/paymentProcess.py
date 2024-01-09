import midtransclient
import random
import string
from main import app, mysql
import json


# Create Snap API instance
snap = midtransclient.Snap(
    # Set to true if you want Production Environment (accept real transaction).
    is_production=False,
    server_key='SB-Mid-server-MkWPtSUBmoSSOJ4UkdcyilCC'
)
def get_token(customer_data, product_data, subtotal, user_address, seller_data, user_id) : 
    # Build API parameter
    order_id = generate_order_id()

    try:
        for row in product_data:
            print(row['id'])
            for seller_id in seller_data:
                try:
                    cur = mysql.connection.cursor() 
                    cur.execute("INSERT INTO transaksi (order_id, nama_customer, email, phone, items_details, quantity,  user_id, seller_id, subtotal, status_transaksi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (order_id, f"{customer_data[0]} {customer_data[1]}", customer_data[2], user_address[3], row['id'], row['quantity'], user_id, seller_id, subtotal, "diproses"))
                except Exception as e:
                    print(f"Error executing query: {e}")
                finally:
                    cur.close()

        mysql.connection.commit()
    except Exception as e:
        print(f"Error: {e}")

  


    param = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": subtotal
        }, "credit_card":{
            "secure" : True
        }, "item_details": product_data, 
        "billing_address" : {
            "first_name" : customer_data[0],
            "last_name" : customer_data[1],
            "address" : user_address[4],
            "city" : user_address[10],
            "postal_code" : user_address[8],
            "phone" : user_address[3],
            "country_code" : "IDN",
        },
        "shipping_address" : {
            "first_name" : customer_data[0],
            "last_name" : customer_data[1],
            "address" : user_address[4],
            "city" : user_address[10],
            "postal_code" : user_address[8],
            "phone" : user_address[3],
            "country_code" : "IDN",
        },
        "customer_details":{
            "first_name": customer_data[0],
            "last_name": customer_data[1],
            "email": customer_data[2],
            "phone": customer_data[3],
            "billing_address": {
                "first_name": customer_data[0],
                "last_name": customer_data[1],
                "address": user_address[4],
                "city": user_address[10],
                "postal_code": user_address[8],
                "phone": user_address[3],
                "country_code": "IDN",
            },
            "shipping_address": {
                "first_name": customer_data[0],
                "last_name": customer_data[1],
                "address": user_address[4],
                "city": user_address[10],
                "postal_code": user_address[8],
                "phone": user_address[3],
                "country_code": "IDN",
            }
        }
    }

    transaction = snap.create_transaction(param)

    transaction_token = transaction['token']
    
    return transaction_token



def generate_order_id() : 
    huruf = ''.join(random.choices(string.ascii_uppercase, k=2))
    angka = ''.join(random.choices(string.digits, k=9))

    order_id = f"{huruf}-{angka}"
    return order_id