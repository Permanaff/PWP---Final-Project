from flask import Flask, render_template, session, request , redirect, url_for, flash, jsonify 
from flask_mysqldb import MySQL
from flask_cors import CORS
import requests
from werkzeug.utils import secure_filename
from midtransclient import Snap, CoreApi
from midtrans.paymentProcess import *
from midtrans.notification_handler import notification_handler
import os
import json

app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:5000', 'https://f405-139-195-236-32.ngrok-free.app'])

core = CoreApi(
    is_production=False,
    server_key= ' <Your Server Key>',
    client_key=' <Your Client Key> '
)

app.secret_key = '!@#$%'

app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"]= ''
app.config["MYSQL_DB"] = 'ecommerce2'
app.config["UPLOAD_FOLDER"] = 'static/images/'

mysql = MySQL(app)

@app.route('/login', methods=['POST'])
def login() : 
    # data = request.json
    email = request.form['email']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute(" SELECT * FROM users WHERE users.email = %s AND users.password = %s;", (email, password))
    result = cur.fetchone()

    if result:
        if result[8] == 2 or result[8] == 1 :
            cur.execute("SELECT id FROM sellers WHERE user_id=%s",(result[0],))
            seller_id = cur.fetchone()[0]
            user = [{"user_id": result[0], 'username': result[3], 'level_user': result[8], "seller_id": seller_id}]
            return jsonify(user), 200
        user = [{"user_id" : result[0], 'username' : result[3], 'level_user' : result[8]}]
        return jsonify(user),200
    else : 
        return jsonify({"stauts" : 'Error', "message" : "Login Gagal!"})


@app.route('/daftar-toko', methods=["POST"])
def daftar_toko():
    try:
        nama_toko = request.form['nama_toko']
        user_id = request.form['user_id']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM alamat_user WHERE user_id = %s", (user_id,))
        alamat = cur.fetchone()

        cur.execute("INSERT INTO sellers (user_id, nama, alamat_lengkap, provinsi_id, kota_id, kecamatan_id) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, nama_toko, alamat[4], alamat[7], alamat[5], alamat[6]))
        mysql.connection.commit()

        cur.execute("UPDATE users SET level_user=%s WHERE id=%s", (2, user_id))
        mysql.connection.commit()

        cur.execute("SELECT users.level_user, sellers.id FROM users LEFT JOIN sellers ON users.id = sellers.user_id WHERE users.id = %s", (user_id,))
        hasil = cur.fetchone() 

        return jsonify([{'level_user': hasil[0], "seller_id":hasil[1]}])
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    

#  =========================================================================================================================================

# Untuk Mengambil data semua produk
@app.route('/get_Product') 
def get_Product(): 
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, image, description, price, stok, views, terjual FROM products")
    data = cur.fetchall()

    cur.execute("SELECT id, name, image, description, price, stok, views, terjual FROM products ORDER BY terjual DESC LIMIT 6;")
    data_populer = cur.fetchall()
    cur.close() 

    products = [{'id': row[0], 'name': row[1], 'image': row[2], 'description': row[3], 'price': row[4], 'stok': row[5], 'views': row[6], 'terjual':row[7]} for row in data]

    products_populer = [{'id': row[0], 'name': row[1], 'image': row[2], 'description': row[3], 'price': row[4], 'stok': row[5], 'views': row[6], 'terjual':row[7]} for row in data_populer]
    
    return jsonify({'products': products, 'populer': products_populer})


# Untuk Mengambil Detail Produk 
@app.route('/getDetail/<int:id>', methods=['GET']) 
def get_product_detail(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT
            p.id,
            p.name,
            p.image,
            p.description,
            p.price,
            p.stok,
            p.views,
            p.terjual,
            p.seller_id,
            s.nama AS seller_name,
            s.profile_image AS seller_image,
            ip.image1,
            ip.image2,
            ip.image3,
            ip.image4
        FROM products p
        JOIN sellers s ON p.seller_id = s.id
        LEFT JOIN image_product ip ON p.id = ip.product_id
        WHERE p.id=%s
    """, (id,))
    
    data = cur.fetchall()

    products = [{'id': row[0], 'name': row[1], 'image': row[2], 'description': row[3], 'price': row[4], 'stok': row[5], 'views': row[6], 'terjual':row[7], 'seller_id' : row[8], 'seller_name' : row[9], 'seller_image' : row[10], 'image1' : row[11], 'image2' : row[12], 'image3' : row[13], 'image4' : row[14]} for row in data]

    return jsonify({'products' : products})


@app.route('/update-views/<int:product_id>', methods=["POST"])
def update_views(product_id) :
    cur = mysql.connection.cursor() 
    cur.execute("SELECT views FROM products WHERE id=%s ", (product_id,)) 
    stok = cur.fetchone()[0] + 1
    cur.execute("UPDATE products SET views=%s WHERE id=%s", (stok, product_id))
    mysql.connection.commit() 

    return jsonify({"status" : "Success"})

@app.route('/update-terjual/<string:order_id>', methods=["POST"])
def update_terjual(order_id) :
    cur = mysql.connection.cursor()     
    cur.execute("SELECT items_details FROM transaksi WHERE order_id=%s",(order_id,))
    data = cur.fetchall()

    for product_id in data : 
        cur.execute("SELECT terjual, stok FROM products WHERE id=%s ", (product_id[0],)) 
        result = cur.fetchone()
        terjual = result[0] + 1
        stok = result[1] - 1
        cur.execute("UPDATE products SET terjual=%s, stok=%s WHERE id=%s", (terjual, stok, product_id[0]))
        mysql.connection.commit() 

    return jsonify({"status" : "Success"})

    
# Mengambil data seller dari database
@app.route('/getSeller/<int:user_id>', methods=["GET"])
def getSeller(user_id):
    cur= mysql.connection.cursor()
    cur.execute("""
        SELECT 
            s.*, 
            p.name, 
            k.name, 
            kc.name
        FROM 
            sellers s
        LEFT JOIN 
            provinsi p ON s.provinsi_id = p.id
        LEFT JOIN 
            kota k ON s.kota_id = k.id
        LEFT JOIN 
            kecamatan kc ON s.kecamatan_id = kc.id
        WHERE 
            s.user_id = %s
    """, (user_id,))
    data = cur.fetchall()
    cur.close()

    seller = [{
        'id' : row[0], 
        'name':row[2], 
        'alamat_lengkap':row[3], 
        'provinsi':row[12], 
        'kota': row[13], 
        'kecamatan': row[14],
        "tipeSeller": row[7], 
        "profileImage":row[8],
        'jamBuka' : format_timedelta(row[9]),
        'jamTutup' : format_timedelta(row[10]),
        'waktu_buka': row[11]
        } for row in data]
    return jsonify({'sellerProfil' : seller})



@app.route('/update-seller-data/<int:user_id>', methods=["PUT"])
def update_seller(user_id) : 
    try :
        subfolder = 'profile_image'
        data = request.form
        name = data['seller-name']
        profile_image = request.files.get('profile-image')
        cur = mysql.connection.cursor()

        if profile_image is None or profile_image.filename == '':
                cur.execute("SELECT profile_image FROM sellers WHERE user_id=%s", (user_id,))
                data = cur.fetchone()
                image = data[0]
        else:
            image = save_image(profile_image, subfolder)

        cur.execute("UPDATE sellers SET nama = %s, profile_image = %s WHERE user_id=%s", (name, image, user_id))
        mysql.connection.commit()

        response = {'status': 'success', 'message': 'Berhasil Mengubah Profil!'}
        return jsonify(response), 200  
    except Exception as e:
            error_message = str(e)
            response = {'status': 'error', 'message': 'Gagal Mengubah Profil', 'error': error_message}
            return jsonify(response), 500


    
# Untuk Menfubah format timedelta database ke format 00:00
def format_timedelta(timedelta_value):
    hours, remainder = divmod(timedelta_value.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}"



# Menmabahkan data ke cart
@app.route('/add-cart/<int:user_id>', methods=["POST"])
def addCart(user_id): 
    data = request.get_json()
    product_id = data['productId']
    quantity = data['quantity']
    cur = mysql.connection.cursor()

    # Cek apakah produk sudah ada di keranjang belanja
    cur.execute("SELECT id, quantity FROM shopping_cart WHERE user_id=%s AND product_id=%s", (user_id, product_id))
    exist = cur.fetchone()

    if exist:
        # Produk sudah ada, update quantity
        new_quantity = exist[1] + quantity
        cur.execute("UPDATE shopping_cart SET quantity=%s WHERE id=%s", (new_quantity, exist[0]))
    else:
        cur.execute("INSERT INTO shopping_cart (user_id, product_id, quantity) VALUES (%s, %s, %s)", (user_id, product_id, quantity))

    mysql.connection.commit()

    response = {'status': 'success', 'message': 'Berhasil Menambahkan ke keranjang'}
    return jsonify(response)



# Mengambil Data Keranjang User
@app.route('/get-data-cart/<int:user_id>', methods=["GET"])
def get_cart(user_id) : 
    cur = mysql.connection.cursor()
    cur.execute("SELECT c.* , p.* FROM shopping_cart c INNER JOIN products p ON c.product_id = p.id WHERE c.user_id = %s", (user_id,))
    data = cur.fetchall() 
    cur.close() 

    cart = [{'user_id':row[0], 'quantity' : row[3], 'product_id': row[5], 'name': row[7], 'image': row[8], 'description': row[9], 'price': row[10], 'stok': row[13], 'seller_id': row[6]} for row in data]

    totalQuantity = sum(item['quantity'] for item in cart)
    subtotal = sum(item['price'] * item['quantity'] for item in cart)

    return jsonify({'cart' : cart}, {'subtotal' : subtotal}, {'quantityTotal' : totalQuantity})

@app.route('/delete-cart/<int:productId>/<int:user_id>', methods=["DELETE"])
def delete_cart(productId, user_id) : 
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM shopping_cart WHERE product_id=%s AND user_id=%s", (productId, user_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'status': 'success', 'message': 'Produk berhasil dihapus'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



# Mengambil Data Produk User Seller 
@app.route('/get-my-product/<int:seller_id>', methods=["GET"])
def my_product_seller(seller_id):
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM products WHERE seller_id = %s", (seller_id,))
    data = cur.fetchall()

    products = [{'id': row[0], 'name': row[2], 'image': row[3], 'description': row[4], 'price': row[5], 'stok': row[8], 'views': row[9], 'terjual':row[10]} for row in data]
    if data : 
        return jsonify({'products' : products})
    else : 
        return jsonify({"Error": "Tidak Ditemukan Data"})


# Untuk Menghapus Data Produk 
@app.route('/delete-product/<int:productId>', methods=["DELETE"])
def delete_product(productId): 
    cur = mysql.connection.cursor() 
    cur.execute("DELETE FROM products WHERE id=%s", (productId,))
    cur.connection.commit()

    return jsonify({'status': 'success', 'message': 'Produk berhasil dihapus'})



# Untuk Menupdate Data Produk
@app.route('/update-product/<int:productId>', methods=["PUT"])
def update_product(productId):
    try:
        subfolder = 'product'
        data = request.form
        gambar = [request.files['image1'], request.files['image2'], request.files['image3'], request.files['image4']]
        image1 = gambar[0].filename
        image2= gambar[1].filename
        image3= gambar[2].filename
        image4= gambar[3].filename
        name = data['name']
        description = data['description']
        harga = data['harga']
        stok = data['stok']

        cur = mysql.connection.cursor() 

        if any(file.filename for file in gambar):
            image_filenames = []

            for index, file in enumerate(gambar):
                image_filename = save_image(file, subfolder)
                image_filenames.append(image_filename)

            image1, image2, image3, image4 = image_filenames
        else:
            cur.execute("SELECT image1, image2, image3, image4 FROM image_product WHERE product_id=%s", (productId,))
            image = cur.fetchone()
            image1 = image[0]
            image2 = image[1]
            image3 = image[2]
            image4 = image[3]

        cur.execute("UPDATE products SET name=%s, image=%s, description=%s, price=%s, stok=%s WHERE id=%s", (name, image1, description, harga, stok, productId,))
        mysql.connection.commit()

        cur.execute("UPDATE image_product SET image1=%s, image2=%s, image3=%s, image4=%s WHERE product_id=%s", (image1, image2, image3, image4, productId,))
        mysql.connection.commit()



        response = {'status': 'success', 'message': 'Berhasil Mengubah Produk!'}
        return jsonify(response), 200  
    
    except Exception as e:
        error_message = str(e)
        response = {'status': 'error', 'message': 'Gagal Mengubah Produk', 'error': error_message}
        return jsonify(response), 500 



# Endpoint untuk update stok
@app.route('/update-stok/<int:productId>', methods=["PUT"])
def update_stok(productId) : 
    try : 
        cur = mysql.connection.cursor() 
        data = request.get_json()
        stok = data.get('stock')

        cur.execute("UPDATE products SET stok=%s WHERE id=%s",(stok, productId,))
        mysql.connection.commit() 

        return jsonify({'status' : 'succrss', 'message' : 'Berhasil Menyimpan Perubahan!'}), 200
    except Exception as e:
        error_message = str(e)
        response = {'status': 'error', 'message': 'Gagal Menyimpan Perubahan', 'error': error_message}
        return jsonify(response), 500 
    


# Endpoint Untuk Menambahkan Data Produk
@app.route('/add-product', methods=["POST"])
def add_product(): 
    try: 
        subfolder = 'product'
        data = request.form
        gambar = [request.files['image1'], request.files['image2'], request.files['image3'], request.files['image4']]
        image1 = gambar[0].filename
        image2= gambar[1].filename
        image3= gambar[2].filename
        image4= gambar[3].filename
        seller_id = data['seller_id']
        name = data['name']
        description = data['description']
        harga = data['harga']
        stok = data['stok'] 

        for index, file in enumerate(gambar):
            image_filename = save_image(file, subfolder)

        cur = mysql.connection.cursor() 
        cur.execute("INSERT INTO products (seller_id, name, image, description, price, stok) VALUES (%s, %s, %s, %s, %s, %s)", (seller_id, name, image1, description, harga, stok,))
        mysql.connection.commit()

        product_id = cur.lastrowid

        cur.execute("INSERT INTO image_product (product_id, image1, image2, image3, image4) VALUES (%s, %s, %s, %s, %s)", (product_id,image1, image2, image3, image4 ))
        mysql.connection.commit()

        response = {'status': 'success', 'message': 'Berhasil Menyimpan Produk!'}
        return jsonify(response), 200 
     
    except Exception as e:
        error_message = str(e)
        response = {'status': 'error', 'message': 'Gagal Mengubah Produk', 'error': error_message}
        return jsonify(response), 500 

    

# Endpoint untuk mengambil data profil
@app.route('/get-profile-data/<int:user_id>', methods=['GET'])
def profile_data(user_id) :
    try : 
        cur = mysql.connection.cursor() 
        cur.execute("SELECT * FROM users WHERE id=%s", (user_id,)) 
        data = cur.fetchone()

        users = [{'user_id': data[0], 'nama': data[1], 'nama_belakang':data[2], 'username': data[3], 'email': data[5], 'no_telp': data[6], 'ttl': data[7], 'profile_image' : data[9]}]

        mysql.connection.commit()

        return jsonify({'user': users})

    except Exception as e:
        error_message = str(e)
        response = {'status': 'error', 'message': 'Gagal Mengambil Data', 'error': error_message}
        return jsonify(response), 500 
    


# Endpoint untuk mengupdate data profil
@app.route('/update-profile-data/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    try:
        subfolder = 'profile_image'
        data = request.form
        gambar = request.files.get('image')
        firstName = data['firstName']
        lastName = data['lastName']
        tanggal_lahir = data['tanggallahir']

        cur = mysql.connection.cursor() 

        if gambar is None or gambar.filename == '':
            cur.execute("SELECT profile_image FROM users WHERE id=%s", (user_id,))
            data = cur.fetchone()
            image = data[0]
        else:
            image = save_image(gambar, subfolder)

        cur.execute("UPDATE users SET nama_depan=%s, nama_belakang=%s, tanggalLahir=%s, profile_image=%s WHERE id=%s", (firstName, lastName, tanggal_lahir, image, user_id,))
        mysql.connection.commit()

        response = {'status': 'success', 'message': 'Berhasil Mengubah Profil!'}
        return jsonify(response), 200  

    except Exception as e:
        error_message = str(e)
        response = {'status': 'error', 'message': 'Gagal Mengubah Profil', 'error': error_message}
        return jsonify(response), 500



# Endpoint untuk mengambil data alamat
@app.route('/get-alamat-user/<int:user_id>', methods=['GET'])
def get_alamat(user_id) : 
    try : 
        cur = mysql.connection.cursor() 
        cur.execute('''SELECT alamat_user.*, provinsi.name AS provinsi_name, kota.name AS kota_name, kecamatan.name AS kecamatan_name
                        FROM alamat_user
                        JOIN provinsi ON alamat_user.provinsi = provinsi.id
                        JOIN kota ON alamat_user.kota = kota.id
                        JOIN kecamatan ON alamat_user.kecamatan = kecamatan.id
                        WHERE alamat_user.user_id = %s
                    ''', (user_id,))

        data = cur.fetchall() 
        cur.close()

        alamat = [{'id_alamat' : row[0], 'nama_lengkap' : row[1], 'no_telp' : row[3], 'jalan' : row[4], 'id_kota' : row[5],  'id_kecamatan' : row[6], 'id_provinsi' : row[7],  'kota' : row[10], 'kecamatan' : row[11], 'provinsi' : row[9], 'kode_pos' : row[8]} for row in data]

        return jsonify({'alamat' : alamat}), 200 


    except Exception as e:
        error_message = str(e)
        response = {'status': 'error', 'message': 'Gagal Mengambil Data Alamat', 'error': error_message}
        return jsonify(response), 500



# Add alamat user
@app.route('/add-alamat', methods=['POST'])
def add_alamat() : 
    try : 
        data = request.get_json()
        nama_lengkap = data['nama_lengkap']
        user_id = data['user_id']
        no_telp = data['no_telp']
        jalan = data['jalan']
        kota = data['kota']
        kecamatan = data['kecamatan']
        provinsi = data['provinsi']
        kode_pos = data['kode_pos']


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO alamat_user (nama_lengkap, user_id, no_telp, jalan, kota, kecamatan, provinsi, kode_pos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nama_lengkap, user_id, no_telp, jalan, kota, kecamatan, provinsi, kode_pos))
        mysql.connection.commit()

        return jsonify({'status': 'success', 'message' : 'Berhasil Menyimpan Data Alamat !'}), 200
    except Exception as e:
        error_message = str(e)
        response = {'status': 'error', 'message': 'Gagal Menyimpan Data Alamat', 'error': error_message}
        return jsonify(response), 500


# Mengambil data provinsi
@app.route('/get-provinsi', methods=['GET'])
def provinsi(): 
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM provinsi")
    data = cur.fetchall() 

    provinsi = [{"id" : row[0], 'name' : row[1]} for row in data]
    return jsonify(provinsi)

# GET data Kota
@app.route('/get-kota/<int:province_id>', methods=['GET'])
def kota(province_id): 
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM kota WHERE province_id=%s", (province_id,))
    data = cur.fetchall() 

    kota = [{"id": row[0], 'regency_id' : row[1] ,'name': row[2]} for row in data]
    return jsonify(kota)

# mengambil data kecamatan
@app.route('/get-kecamatan/<int:regency_id>', methods=['GET'])
def kecamatan(regency_id): 
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM kecamatan WHERE regency_id=%s", (regency_id,))
    data = cur.fetchall() 

    kecamatan = [{"id": row[0], 'regency_id' : row[1] ,'name': row[2]} for row in data]
    return jsonify(kecamatan)


# ========================== PAYMENT GATEWAY MIDTRANS ==========================
@app.route('/get-token-transaction/<int:user_id>/<int:id_alamat>', methods=["POST"])
def get_token_transaction(user_id, id_alamat) : 
    try : 
        data = request.get_json()
        product_data = data['productData']
        subtotal = data['subtotal']
        seller_data = data['sellerData']

        cur = mysql.connection.cursor() 
        cur.execute("SELECT nama_depan, nama_belakang, email, no_telp FROM users WHERE id=%s ", (user_id,))
        customer_data = cur.fetchone() 

        cur.execute('''SELECT alamat_user.*, provinsi.name AS provinsi_name, kota.name AS kota_name, kecamatan.name AS kecamatan_name
                        FROM alamat_user
                        JOIN provinsi ON alamat_user.provinsi = provinsi.id
                        JOIN kota ON alamat_user.kota = kota.id
                        JOIN kecamatan ON alamat_user.kecamatan = kecamatan.id
                        WHERE alamat_user.id_alamat = %s
                    ''', (id_alamat,))
    
        user_address = cur.fetchone() 
        cur.close()
        
        token = get_token(customer_data, product_data, subtotal, user_address, seller_data, user_id)
        return jsonify(token), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@app.route('/get-data-transaksi/<string:order_id>', methods=["GET"])
def data_transaksi(order_id) : 
    cur = mysql.connection.cursor() 
    cur.execute("SELECT * FROM transaksi WHERE order_id = %s", (order_id,))
    data = cur.fetchone() 

    detail = [{"order_id" : data[1], 'nama_customer': data[2], 'email' : data[3], "phone" : data[4], 'items_detail' : data[5], 'subtotal': data[7]}]

    return jsonify(detail), 200


@app.route('/delete-all-cart/<int:user_id>', methods=["POST"])
def delete_all_cart(user_id) : 
    try : 
        cur = mysql.connection.cursor() 
        cur.execute("DELETE FROM shopping_cart WHERE user_id = %s",(user_id,))
        mysql.connection.commit() 
        cur.close() 

        return jsonify({"Success" : "Success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500



# =========================== LAIN - LAIN ===========================

# Function untuk menyimpan gambar
def save_image(file, subfolder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder, filename)
        file.save(file_path)
        
        send_file(filename, file_path, subfolder)

        return filename
    return None

def send_file(name, file_path, subfolder):
    url = 'http://127.0.0.1:5000/save-image'
    
    with open(file_path, 'rb') as file:
        files = {'file': (name, file, 'multipart/form-data')}
        data = {'subfolder': subfolder}
        response = requests.post(url, files=files, data=data)

    return response.json()

# Fungsi untuk mengecek ekstensi file yang diizinkan
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/history_transaction_user/<int:user_id>', methods=["GET"])
def history_transaction_user(user_id):
    try:
        cur = mysql.connection.cursor()

        cur.execute("""
                    SELECT 
                        transaksi.order_id,
                        transaksi.nama_customer,
                        GROUP_CONCAT(transaksi.items_details) AS all_product_ids,
                        GROUP_CONCAT(products.name) AS all_product_names,
                        GROUP_CONCAT(products.image) AS all_images,
                        SUM(transaksi.subtotal) AS total_subtotal,
                        transaksi.status_transaksi,
                        GROUP_CONCAT(products.price) AS all_prices,
                        GROUP_CONCAT(transaksi.quantity) AS all_quantities
                    FROM transaksi
                    JOIN products ON transaksi.items_details = products.id
                    WHERE transaksi.user_id = %s
                    GROUP BY transaksi.order_id, transaksi.nama_customer, transaksi.status_transaksi;
                    ORDER BY transaksi.order_id DESC;
                """, (user_id,))
        result = cur.fetchall()

        riwayat = [
            {
                'order_id': row[0],
                'nama_customer': row[1],
                'all_product_ids': row[2].split(',') if row[2] else [],
                'all_product_names': row[3].split(',') if row[3] else [],
                'all_images': row[4].split(',') if row[4] else [],
                'total_subtotal': float(row[5]) if row[5] else 0.0,
                'status_transaksi': row[6],
                'all_prices': row[7].split(',') if row[7] else [],
                'all_quantities': row[8].split(',') if row[8] else []
            }
            for row in result
        ]
        return jsonify({'riwayat': riwayat})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

    
@app.route('/history_transaction_seller/<int:seller_id>', methods=["GET"])
def history_transaction_seller(seller_id):
    try:
        cur = mysql.connection.cursor()

        cur.execute("""
                    SELECT 
                        transaksi.order_id,
                        transaksi.nama_customer,
                        GROUP_CONCAT(transaksi.items_details) AS all_product_ids,
                        GROUP_CONCAT(products.name) AS all_product_names,
                        GROUP_CONCAT(products.image) AS all_images,
                        SUM(transaksi.subtotal) AS total_subtotal,
                        transaksi.status_transaksi,
                        GROUP_CONCAT(products.price) AS all_prices,
                        GROUP_CONCAT(transaksi.quantity) AS all_quantities
                    FROM transaksi
                    JOIN products ON transaksi.items_details = products.id
                    WHERE transaksi.seller_id = %s
                    GROUP BY transaksi.order_id, transaksi.nama_customer, transaksi.status_transaksi;
                    ORDER BY transaksi.order_id DESC;
                """, (seller_id,))
        result = cur.fetchall()

        riwayat = [
            {
                'order_id': row[0],
                'nama_customer': row[1],
                'all_product_ids': row[2].split(',') if row[2] else [],
                'all_product_names': row[3].split(',') if row[3] else [],
                'all_images': row[4].split(',') if row[4] else [],
                'total_subtotal': float(row[5]) if row[5] else 0.0,
                'status_transaksi': row[6],
                'all_prices': row[7].split(',') if row[7] else [],
                'all_quantities': row[8].split(',') if row[8] else []
            }
            for row in result
        ]
        return jsonify({'riwayat': riwayat})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500



if __name__== "__main__":
    app.run(debug=True, port=3000)