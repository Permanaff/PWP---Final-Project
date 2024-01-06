from flask import Flask, render_template, session, request , redirect, url_for, flash, jsonify 
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import requests
import os

app = Flask(__name__)

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
        # cur.execute(" SELECT * FROM users WHERE users.email = %s AND users.password = %s;", (email, passwd))
        # result = cur.fetchone()

        api_url = 'http://127.0.0.1:3000/login'
        api_data = {'email': email, 'password': passwd}
        response = requests.post(api_url, data=api_data)
   
        if response.status_code == 200:
            data = response.json()
            print(data)

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

            print("SUKSES")
            return jsonify({'status': 'success', 'message': 'File received and saved successfully'})
        else:
            print(" KURANG SUKSES")
            return jsonify({'status': 'error', 'message': 'Invalid file or file extension'})
    except Exception as e:
        print("ERROR COK")
        return jsonify({'status': 'error', 'message': 'Error receiving and saving file', 'error': str(e)})


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



if __name__== "__main__":
    app.run(debug=True)