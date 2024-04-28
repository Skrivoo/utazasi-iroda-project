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

admin = False


def select(what, where, filter_param=None, filter_param_filter=None):
    cur = con.cursor()
    if filter_param is None:
        data = [what, where]
        cur.execute("SELECT :1 FROM :2", data)
    else:
        data = [what, where, filter_param, filter_param_filter]
        cur.execute("SELECT :1 FROM :2 WHERE :3 = :4", data)
    eredmeny = cur.fetchall()
    cur.close()
    return eredmeny


def insert(where, which_line, what):
    cur = con.cursor()
    sql = "INSERT INTO :table_name VALUES (:which_line) (:what)"
    cur.execute(sql, table_name=where, which_line=which_line, what=what)
    con.commit()


def delete(where, what, column_name):
    cur = con.cursor()
    sql = "DELETE FROM :table_name WHERE :comlumn_name = :what"
    cur.execute(sql, table_name=where, comlumn_name=column_name, what=what)
    con.commit()


def update(where, what, column_name):
    cur = con.cursor()
    sql = "UPDATE :table_name SET :what where = :column_name"
    cur.execute(sql, table_name=where, column_name=column_name, what=what)
    con.commit()


@app.route('/')
@app.route('/home')
def index():
    if 'loggedin' in session:
        msg = 'Be vagy jelentkezve'
    else:
        msg = 'Udvozlunk a repulogep szolgaltatonknal'
    return render_template('index.html', connection=con.instance_name, msg=msg)


@app.route('/registration', methods=['GET', 'POST'])
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
        is_admin = 0
        if password != password_again:
            msg = 'A ket jelszo nem egyezik meg!'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            try:
                insert("SZEMELY", ":1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5, :6", f"{id_number},\
                {name}, {birthdate}, {email}, {hashed_password}, {is_admin}")
                # cur = con.cursor()
                # cur.execute("INSERT INTO SZEMELY VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5, :6)",
                #            (id_number, name, birthdate, email, hashed_password, is_admin))
                # con.commit()
            except Exception as e:
                print(e)
                msg = 'A regisztracio sikertelen :('
    elif request.method == 'POST':
        msg = 'Tolts ki minden mezot!'
    return render_template('registration.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and \
            'password' in request.form and \
            'email' in request.form:
        hashed_password = select("jelszo", "szemely", "email_cim", request.form['email'])[0]
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
    # TODO finish the logic
    insurance_list = select("*", "BIZTOSITAS")
    return render_template('insurance.html', insurance=insurance_list)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    cur = con.cursor()
    sql = "SELECT admin, email_cim FROM SZEMELY where email_cim = :email"
    cur.execute(sql, email=request.form['email'])
    is_admin = cur.fetchone()[0]
    cur.close()
    if is_admin == 1:
        admin_user = "Admin vagy!"
        return render_template('index.html', is_admin=admin_user)
    else:
        admin_user = ""
        return render_template('index.html', is_admin=admin_user)


@app.route('/manage_user', methods=['GET', 'POST'])
def manage_user():
    msg = 'Írd be a user adatait akit törölni szeretnél'
    if request.method == 'POST' and \
            'name' in request.form and \
            'email' in request.form and \
            'id-number' in request.form and\
            'delete' in request.form and \
            'change' in request.form:
        if request.form['delete'] == 'Törlöm':
            delete("SZEMELY", request.form['name'], "NEV")
        if request.form['change'] == 'Megváltoztatom':
            update('SZEMELY', f"{request.form['name']}, {request.form['email']}, {request.form['id-number']}")
    return render_template('manageUser.html', msg=msg)


app.run(host='0.0.0.0', port=5000)
