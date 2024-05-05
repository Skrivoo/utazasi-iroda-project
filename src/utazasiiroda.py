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
    if is_user_logged_in():
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
        if password != password_again:
            msg = 'A ket jelszo nem egyezik meg!'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO SZEMELY VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5)",
                            (id_number, name, birthdate, email, hashed_password))
                con.commit()
            except Exception as e:
                print(e)
                msg = 'A regisztracio sikertelen :('
    elif request.method == 'POST':
        msg = 'Tolts ki minden mezot!'
    return render_template('registration.html', msg=msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if is_user_logged_in():
        msg = 'Mar be vagy jelentkezve'
    elif request.method == 'POST' and \
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


@app.route('/plan_trip')
def plan_trip():
    cur = con.cursor()
    cur.execute("SELECT * FROM JARAT")
    trip_list = cur.fetchall()
    cur.close()
    return render_template('plan_trip.html', trip_list=trip_list, is_user_logged_in = is_user_logged_in())

@app.route('/reserve_trip/<id>')
def reserve_trip(id):
    msg = ''
    try:
        cur = con.cursor()
        output = cur.var(int)
        cur.execute("""
                declare
                    number_of_seats INTEGER;
                    reserved_seats INTEGER;
                begin
                    SELECT b.ULOHELYEK_SZAMA INTO number_of_seats FROM JARAT a JOIN GEP b ON a.GEP_SZAMA = b.GEP_SZAMA WHERE a.JARAT_SZAM = :in_val;
                    SELECT COUNT(*) INTO reserved_seats FROM UTAZAS WHERE JARAT_SZAM = :in_val;
                    IF reserved_seats < number_of_seats THEN
                        :out_val := reserved_seats + 1;
                    ELSE
                        :out_val := -999;
                    END IF;
                end;""", in_val=id, out_val=output)
        if output.getvalue() == -999:
            msg = 'A foglalas sikertelen, nincs mar szabad hely a gepen'
        else:
            cur.execute("""
                        declare
                            person_id VARCHAR2(20);
                        begin
                            SELECT SZEMELYI_SZAM INTO person_id FROM SZEMELY WHERE EMAIL = :email;
                            INSERT INTO UTAZAS VALUES (person_id, :flight_id, :seat_number);
                        end;""", email=session['email'], seat_number=output.getvalue(), flight_id=id)
            con.commit()
            msg = f'Sikeres foglalas, a {id} azonositoju jaraton az On ulesszama: {output.getvalue()}'
    except oracledb.IntegrityError:
        msg = 'Mar foglalt erre az utra'
    cur.close()
    return render_template('index.html', msg=msg)


@app.route('/insurance')
def insurance():
    #TODO ha benne lesznek az admin funkciok akkor le kell kerni, hogy admin-e a user. A biztositas torles mar mukodik es benne van a tablazatban de csak adminkent akarjuk engedelyezni
    admin_privilege = False
    cur = con.cursor()
    cur.execute("SELECT * FROM BIZTOSITAS")
    insurance_list = cur.fetchall()
    cur.close()
    return render_template(
        'insurance.html',
        insurance=insurance_list,
        is_user_logged_in = is_user_logged_in(),
        admin_privilege = admin_privilege
    )

@app.route('/insurance/<id>/delete')
def delete_insurance(id):
    cur = con.cursor()
    sql = "DELETE FROM BIZTOSITAS WHERE BIZTOSITAS_AZONOSITO = :id"
    cur.execute(sql, id=id)
    con.commit()
    cur.close()
    return redirect(url_for('insurance'))

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
    msg = ''
    if request.method == 'POST' and \
            'email' in request.form and \
            'action' in request.form:
        if request.form['action'] == 'Torles':
            cur = con.cursor()
            sql = "DELETE FROM SZEMELY WHERE EMAIL = :email"
            cur.execute(sql, email=request.form['email'])
            con.commit()
            msg = 'A felhasznalo sikeresen torolve'
        if request.form['action'] == 'Frissites':
            if 'name' not in request.form or 'id-number' not in request.form:
                msg = 'Az szemelyi azonosito es a nev megadasa is szukseges'
            else:
                cur = con.cursor()
                sql = "UPDATE SZEMELY SET SZEMELYI_SZAM = :id_number, NEV = :name WHERE EMAIL = :email"
                cur.execute(sql, id_number=request.form['id-number'], name=request.form['name'], email=request.form['email'])
                con.commit()
                msg = 'A felhasznalo sikeresen frissitve'
    return render_template('manage_user.html', msg=msg)

def is_user_logged_in():
    return True if 'loggedin' in session else False


app.run(host='0.0.0.0', port=5000)
