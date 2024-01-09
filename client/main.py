from flask import Flask, render_template, session, request , redirect, url_for, flash, jsonify 
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.utils import secure_filename
from midtransclient import Snap, CoreApi
import requests
import os
import json

app = Flask(__name__)
CORS(app)


core = CoreApi(
    is_production=False,
    server_key= '<Your Server Key>',
    client_key='<Yout Client Key>'
)

app.secret_key = '!@#$%'

app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"]= ''
app.config["MYSQL_DB"] = 'ecommerce2'
app.config["UPLOAD_FOLDER"] = 'static/images/'

mysql = MySQL(app)

# Home
@app.route('/')
def home():
    if 'is_logged_in' in session : 
        return render_template('home.html', level_user=session['level_user'],  session = session['status'], name=session['username'], user_id = session['user_id'])
    else :
        return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        email = request.form['inpEmail']
        passwd = request.form['inpPass']

        cur = mysql.connection.cursor()

        api_url = 'http://127.0.0.1:3000/login'
        api_data = {'email': email, 'password': passwd}
        response = requests.post(api_url, data=api_data)
   
        if response.status_code == 200:
            data = response.json()

            user_id = data[0]['user_id']
            username = data[0]['username']
            level_user = data[0]['level_user']

            if data:
                session['is_logged_in'] = True
                session['user_id'] = user_id
                session['username'] = username
                session['level_user'] = level_user
                session['status'] = True

                if level_user == 2 or level_user == 1 :
                    seller_id = data[0]['seller_id']
                    session['seller_id'] = seller_id
                
                return redirect(url_for('home'))
        else:
            error_message = "Login Gagal. Email atau password tidak valid."
            flash(error_message, 'error')
            print(session['seller_id'])
            return redirect(url_for('login', error='Login Gagal'))
        cur.close()
    else:
        return render_template('login.html')
    

@app.route('/daftar_toko', methods=["POST"])
def daftar_toko() : 
    nama_toko = request.form['inpNamaToko']
    user_id = session['user_id']

    api_url = 'http://127.0.0.1:3000/daftar-toko'
    api_data = {'nama_toko': nama_toko, 'user_id': user_id}
    response = requests.post(api_url, data=api_data)

    if response.status_code == 200:
        data = response.json()
        session.pop('level_user', None)
        session['level_user'] = data[0]['level_user']
        session['seller_id'] = data[0]['seller_id']
        
    return redirect(url_for('home'))

    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST" and "inpUser" in request.form and "inpEmail" in request.form and "inpPass" in request.form:
        nama = request.form["firstName"]
        lastName = request.form["lastName"]
        username = request.form["inpUser"]
        email = request.form["inpEmail"]
        passwd = request.form["inpPass"]
        level_user = 3
        image = 'default-profile.png'
        no_telp = request.form["inpTelp"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (nama_depan, nama_belakang, username, email, no_telp, password, level_user, profile_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(nama, lastName, username, email, no_telp, passwd, level_user, image))
        mysql.connection.commit()

        return redirect(url_for('login'))
    else:
        return render_template('register.html')


# Halaman Detail Produk
@app.route('/detail-product/<int:id>', methods=["POST", "GET"])
def detailProduct(id): 
    if 'is_logged_in' in session : 
        return render_template('detail_product.html', product_id=id, level_user=session['level_user'],  session = session['status'], name=session['username'], user_id=session['user_id'])  
    else :
        return render_template('detail_product.html', product_id=id, level_user=3,  session = False, user_id=0) 

# ================================= PROFILE =================================
@app.route('/account')
@app.route('/account/profil-saya')
def account() :
    if 'is_logged_in' in session : 
        return render_template('profile.html',level_user=session['level_user'],  session = session['status'], name=session['username'], user_id=session['user_id'])  
    else :
        return redirect(url_for('login'))

@app.route('/account/alamat-saya')
def alamat_saya() : 
    return render_template('profile/alamat-saya.html',level_user=session['level_user'],  session = session['status'], name=session['username'], user_id=session['user_id'])  
    
@app.route('/account/riwayat-pembelian')
def pembelian() : 
    return render_template('profile/riwayat-pembelian.html',level_user=session['level_user'],  session = session['status'], name=session['username'], user_id=session['user_id'])  

# =============================== PROFILE END =============================== 


# ================================ DASHBOARD ================================
# Halaman Detail Produk
@app.route('/dashboard', methods=["GET", "POST"])
def dashboard(): 
    if 'is_logged_in' in session : 
        return render_template('dashboard.html',level_user=session['level_user'],  session = session['status'], name=session['username'], seller_id = session['seller_id'])  
    else :
        return redirect(url_for('login'))

# Halaman Dashboard Toko Anda
@app.route('/dashboard/toko-anda', methods=["GET", "POST"])
def tokoAnda() : 
    return render_template("/dashboard/tokoAnda.html", seller_id = session['seller_id'], user_id=session['user_id'])
   
# Halaman Dashboard Daftar Produk
@app.route('/dashboard/daftar-produk', methods=["GET", "POST"])
def daftar_produk() : 
    return render_template("/dashboard/daftar-produk.html", seller_id = session['seller_id'])

# Halaman Dashboard Tambah Produk 
@app.route('/dashboard/tambah-produk', methods=["GET", "POST"])
def tambah_produk() : 
    return render_template("/dashboard/tambah-produk.html", seller_id = session['seller_id'])


# ================================ DASHBOARD END ================================ 

# Halaman Cart
@app.route('/cart')
def cart():
    if session['status'] == False : 
       return redirect(url_for('login'))
    else : 
        return render_template('cart.html', user_id=session['user_id'], level_user=session['level_user'],  session = session['status'], name=session['username'])  


@app.route('/after-payment')
def after_payment():
    return render_template('after-payment.html', user_id=session['user_id'], level_user=session['level_user'],  session = session['status'], name=session['username'])  


# Untuk Mengmbil status session buat navbar
@app.route('/get_user_status')
def get_user_status():
    return {'logged_in': 'user_id' in session}



# Untuk Logout 
@app.route('/logout', methods=['GET', 'POST'])
def logout(): 
    session.pop('is_logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('level_user', None)
    session['status'] = False
    session.pop('seller_id', None)
    return redirect(url_for('home'))

#  =========================================================================================================================================


@app.route('/save-image', methods=['POST'])
def receive_data():
    try:
        file = request.files['file']
        subfolder = request.form.get('subfolder', '') 

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder, filename)
            file.save(file_path)

            return jsonify({'status': 'success', 'message': 'File received and saved successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid file or file extension'})
    except Exception as e:
        print("ERROR COK")
        return jsonify({'status': 'error', 'message': 'Error receiving and saving file', 'error': str(e)})


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/notification_handler', methods=['POST'])
def notification_handler():
    request_json = request.get_json()
    transaction_status_dict = core.transactions.notification(request_json)

    order_id           = request_json['order_id']
    transaction_status = request_json['transaction_status']
    fraud_status       = request_json['fraud_status']
    transaction_json   = json.dumps(transaction_status_dict)

    summary = 'Transaction notification received. Order ID: {order_id}. Transaction status: {transaction_status}. Fraud status: {fraud_status}.<br>Raw notification object:<pre>{transaction_json}</pre>'.format(order_id=order_id,transaction_status=transaction_status,fraud_status=fraud_status,transaction_json=transaction_json)

    # [5.B] Handle transaction status on your backend
    # Sample transaction_status handling logic
    if transaction_status == 'capture':
        if fraud_status == 'challenge':
            # TODO set transaction status on your databaase to 'challenge'
            cur = mysql.connection.cursor() 
            cur.execute("UPDATE transaksi SET status_transaksi = %s WHERE order_id = %s",(transaction_status, order_id,))
            mysql.connection.commit() 

        elif fraud_status == 'accept':
            # TODO set transaction status on your databaase to 'success'
            cur = mysql.connection.cursor() 
            cur.execute("UPDATE transaksi SET status_transaksi = %s WHERE order_id = %s",(transaction_status, order_id,))
            mysql.connection.commit() 

    elif transaction_status == 'settlement':
        # TODO set transaction status on your databaase to 'success'
        cur = mysql.connection.cursor() 
        cur.execute("UPDATE transaksi SET status_transaksi = %s WHERE order_id = %s",(transaction_status, order_id,))
        mysql.connection.commit() 
        
    elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
        # TODO set transaction status on your databaase to 'failure'
        cur = mysql.connection.cursor() 
        cur.execute("UPDATE transaksi SET status_transaksi = %s WHERE order_id = %s",(transaction_status, order_id,))
        mysql.connection.commit() 
        
    elif transaction_status == 'pending':
        # TODO set transaction status on your databaase to 'pending' / waiting payment
        cur = mysql.connection.cursor() 
        cur.execute("UPDATE transaksi SET status_transaksi = %s WHERE order_id = %s",(transaction_status, order_id,))
        mysql.connection.commit() 

    elif transaction_status == 'refund':
        # TODO set transaction status on your databaase to 'refund'
        cur = mysql.connection.cursor() 
        cur.execute("UPDATE transaksi SET status_transaksi = %s WHERE order_id = %s",(transaction_status, order_id,))
        mysql.connection.commit() 

    # app.logger.info(summary)
    return jsonify(summary)





if __name__== "__main__":
    app.run(debug=True)
