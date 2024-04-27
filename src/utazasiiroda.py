from flask import Flask, render_template, request, url_for, session, redirect
from flask_bcrypt import Bcrypt
import oracledb

connection_string = "localhost:1521/freepdb1"
con = oracledb.connect(
    user="SYSTEM", password='jelszo', dsn=connection_string
)

app = Flask(__name__)
app.secret_key = 'nagyon titkos kod'
bcrypt = Bcrypt(app)

@app.route('/')
@app.route('/home')
def index():
    if 'loggedin' in session:
        msg = 'Be vagy jelentkezve'
    else:
        msg = 'Udvozlunk a repulogep szolgaltatonknal'
    return render_template('index.html', connection=con.instance_name, msg=msg)

@app.route('/registration', methods =['GET', 'POST'])
def registration():
    msg = ''
    if request.method == 'POST' and \
            'name' in request.form and \
            'email' in request.form and \
            'password' in request.form and \
            'password-again' in request.form and \
            'id-number' in request.form and \
            'birthdate' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_again = request.form['password-again']
        id_number = request.form['id-number']
        birthdate = request.form['birthdate']
        if password != password_again:
            msg = 'A ket jelszo nem egyezik meg!'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO SZEMELY VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5)", (id_number, name, birthdate, email, hashed_password))
                con.commit()
            except Exception as e:
                print(e)
                msg = 'A regisztracio sikertelen :('
    elif request.method == 'POST':
        msg = 'Tolts ki minden mezot!'
    return render_template('registration.html', msg = msg)
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and \
            'password' in request.form and \
            'email' in request.form:
        cur = con.cursor()
        sql = "SELECT PASSWD FROM SZEMELY WHERE EMAIL = :email"
        cur.execute(sql, email=request.form['email'])
        hashed_password = cur.fetchone()[0]
        cur.close()
        is_valid = bcrypt.check_password_hash(hashed_password, request.form['password'])
        if is_valid:
            session['loggedin'] = True
            session['email'] = request.form['email']
            msg = 'Sikeres bejelentkezes!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Sikertelen bejelentkezes, nem megfelelo email vagy jelszo!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/insurance')
def insurance():
    #TODO finish the logic
    cur = con.cursor()
    cur.execute("SELECT * FROM BIZTOSITAS")
    insurance_list = cur.fetchall()
    cur.close()
    return render_template('insurance.html', insurance=insurance_list)

app.run(host='0.0.0.0', port=5000)
