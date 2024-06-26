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
    user_points = None
    if is_user_logged_in():
        msg = 'Be vagy jelentkezve'
        user_points = get_user_points()
    else:
        msg = 'Udvozlunk a repulogep szolgaltatonknal'
    return render_template('index.html', connection=con.instance_name, user_points=user_points, msg=msg, active='index', admin_privilege=is_user_admin())


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
                cur.execute("INSERT INTO SZEMELY VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5, :6)",
                            (id_number, name, birthdate, email, hashed_password, 0))
                con.commit()
            except Exception as e:
                print(e)
                msg = 'A regisztracio sikertelen :('
    elif request.method == 'POST':
        msg = 'Tolts ki minden mezot!'
    return render_template('registration.html', msg=msg, active='registration', admin_privilege=is_user_admin())


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if is_user_logged_in():
        msg = 'Mar be vagy jelentkezve'
    elif request.method == 'POST' and \
            'password' in request.form and \
            'email' in request.form:
        cur = con.cursor()
        sql = "SELECT PASSWD, IS_ADMIN FROM SZEMELY WHERE EMAIL = :email"
        cur.execute(sql, email=request.form['email'])
        result = cur.fetchone()
        hashed_password = result[0]
        is_admin = bool(result[1])
        cur.close()
        is_valid = bcrypt.check_password_hash(hashed_password, request.form['password'])
        if is_valid:
            session['loggedin'] = True
            session['email'] = request.form['email']
            if is_admin:
                session['admin'] = True
            msg = 'Sikeres bejelentkezes!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Sikertelen bejelentkezes, nem megfelelo email vagy jelszo!'
    return render_template('login.html', msg=msg, active='login', admin_privilege=is_user_admin())


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('admin', None)
    return redirect(url_for('index'))


@app.route('/plan_trip', methods=['GET', 'POST'])
def plan_trip():
    cur = con.cursor()
    if request.method == 'POST':
        try:
            from_filter = request.form['from_filter']
            to_filter = request.form['to_filter']
            when_filter = request.form['when_filter']
            owner_filter = request.form['owner_filter']
            action = request.form['action']
            email = session['email']
            if action == 'Minden jarat':
                cur.execute("SELECT * FROM JARAT")
                trip_list = cur.fetchall()
            elif action == 'Sajat utazasok':
                output_cursor = cur.var(oracledb.DB_TYPE_CURSOR)
                cur.execute("""
                DECLARE
                    person_id SZEMELY.Szemelyi_szam%TYPE;
                    trip_cursor SYS_REFCURSOR;
                BEGIN
                    SELECT SZEMELYI_SZAM INTO person_id FROM SZEMELY WHERE EMAIL = :email;
                    OPEN trip_cursor FOR
                    SELECT *
                    FROM JARAT
                    JOIN UTAZAS ON JARAT.Jarat_szam = UTAZAS.Jarat_szam
                    WHERE UTAZAS.Szemelyi_szam = person_id;
                    :output_cursor := trip_cursor;
                END;""", email=session['email'], output_cursor=output_cursor)
                trip_list = output_cursor.getvalue().fetchall()
            elif action == 'Szures' and owner_filter == 'any':
                cur.execute("""
                SELECT * FROM JARAT WHERE
                (:from_filter = 'any' OR Honnan = :from_filter) AND
                (:to_filter = 'any' OR Hova = :to_filter) AND
                (:when_filter = 'any' OR Ido = TO_TIMESTAMP(:when_filter, 'YYYY-MM-DD HH24:MI:SS')) 
                """, from_filter=from_filter, to_filter=to_filter, when_filter=when_filter)
                trip_list = cur.fetchall()
            elif action == 'Szures' and owner_filter == 'relevant':
                output_cursor = cur.var(oracledb.DB_TYPE_CURSOR)
                cur.execute("""
                DECLARE
                    person_id SZEMELY.Szemelyi_szam%TYPE;
                    trip_cursor SYS_REFCURSOR;
                BEGIN
                    SELECT SZEMELYI_SZAM INTO person_id FROM SZEMELY WHERE EMAIL = :email;
                    OPEN trip_cursor FOR 
                    SELECT * FROM JARAT 
                    JOIN UTAZAS ON JARAT.Jarat_szam = UTAZAS.Jarat_szam WHERE
                    (UTAZAS.Szemelyi_szam = person_id) AND
                    (:from_filter = 'any' OR Honnan = :from_filter) AND
                    (:to_filter = 'any' OR Hova = :to_filter) AND
                    (:when_filter = 'any' OR Ido = TO_TIMESTAMP(:when_filter, 'YYYY-MM-DD HH24:MI:SS'));
                    :output_cursor := trip_cursor;
                END;
                """, from_filter=from_filter, to_filter=to_filter, when_filter=when_filter, email=email,
                            output_cursor=output_cursor)
                trip_list = output_cursor.getvalue().fetchall()
            elif action == 'Szures' and is_user_admin():
                output_cursor = cur.var(oracledb.DB_TYPE_CURSOR)
                cur.execute("""
                DECLARE
                    trip_cursor SYS_REFCURSOR;
                BEGIN
                    OPEN trip_cursor FOR 
                    SELECT * FROM JARAT 
                    JOIN UTAZAS ON JARAT.Jarat_szam = UTAZAS.Jarat_szam WHERE
                    (UTAZAS.Szemelyi_szam = :person_id) AND
                    (:from_filter = 'any' OR Honnan = :from_filter) AND
                    (:to_filter = 'any' OR Hova = :to_filter) AND
                    (:when_filter = 'any' OR Ido = TO_TIMESTAMP(:when_filter, 'YYYY-MM-DD HH24:MI:SS'));
                    :output_cursor := trip_cursor;
                END;
                """, from_filter=from_filter, to_filter=to_filter, when_filter=when_filter, person_id=owner_filter,
                            output_cursor=output_cursor)
                trip_list = output_cursor.getvalue().fetchall()
        except:
            print('Valami probléma adódott.')
            return redirect(url_for('plan_trip'))
    else:
        cur.execute("SELECT * FROM JARAT")
        trip_list = cur.fetchall()
    cur.execute("SELECT Neve, Kod FROM VAROS")
    cities = cur.fetchall()
    cur.execute("SELECT Ido FROM JARAT GROUP BY Ido")
    times = cur.fetchall()
    cur.execute("SELECT Nev, Szemelyi_szam FROM SZEMELY")
    users = cur.fetchall()
    cur.close()
    return render_template('plan_trip.html', admin_privilege=is_user_admin(), users=users, times=times, cities=cities,
                           trip_list=trip_list, is_user_logged_in=is_user_logged_in(), active='plan_trip')


@app.route('/reserve_trip/<id>')
def reserve_trip(id):
    msg = ''
    cur = con.cursor()
    try:
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
    finally:
        cur.close()
    return render_template('index.html', msg=msg, active='index')


@app.route('/insurance', methods=['GET', 'POST'])
def insurance():
    insurance_list = []
    msg = ''
    if request.method == 'POST' and \
            'id' in request.form and \
            'type' in request.form and \
            'duedate' in request.form and \
            'price' in request.form:
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO BIZTOSITAS VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4)",
                        (request.form['id'], request.form['type'], request.form['duedate'], request.form['price']))
            con.commit()
            msg = 'A biztositas sikeresen hozzaadva'
        except:
            msg = 'Biztositas felvitele sikertelen'
    elif request.method == 'POST' and 'type_filter' in request.form:
        type_filter = request.form['type_filter']
        time_from = request.form['time_from']
        time_to = request.form['time_to']
        value_from = request.form['value_from']
        value_to = request.form['value_to']
        action = request.form['action']
        cur = con.cursor()
        if action == 'Osszes':
            cur.execute("SELECT * FROM BIZTOSITAS")
            insurance_list = cur.fetchall()
        elif type_filter == 'any':
            cur.execute("""
                        SELECT * FROM BIZTOSITAS 
                        WHERE TO_DATE(:time_from, 'YYYY-MM-DD') <= Lejarat AND 
                        Lejarat <= TO_DATE(:time_to, 'YYYY-MM-DD') AND
                        :value_from <= Erteke AND Erteke <= :value_to""",
                        time_from=time_from,
                        time_to=time_to,
                        value_from=value_from,
                        value_to=value_to)
            insurance_list = cur.fetchall()

        else:
            cur.execute("""
                        SELECT * FROM BIZTOSITAS 
                        WHERE Tipus = :type_filter AND
                        TO_DATE(:time_from, 'YYYY-MM-DD') <= Lejarat AND 
                        Lejarat <= TO_DATE(:time_to, 'YYYY-MM-DD') AND
                        :value_from <= Erteke AND Erteke <= :value_to""",
                        type_filter=type_filter,
                        time_from=time_from,
                        time_to=time_to,
                        value_from=value_from,
                        value_to=value_to)
            insurance_list = cur.fetchall()

        cur.close()
    else:
        cur = con.cursor()
        cur.execute("SELECT * FROM BIZTOSITAS")
        insurance_list = cur.fetchall()
        cur.close()

    cur = con.cursor()
    cur.execute("SELECT Tipus FROM BIZTOSITAS GROUP BY Tipus")
    type_list = cur.fetchall()
    cur.close()
    return render_template(
        'insurance.html',
        types=type_list,
        insurance=insurance_list,
        is_user_logged_in=is_user_logged_in(),
        admin_privilege=is_user_admin(),
        msg=msg,
        active='insurance'
    )


@app.route('/insurance/<id>/delete')
def delete_insurance(id):
    cur = con.cursor()
    sql = "DELETE FROM BIZTOSITAS WHERE BIZTOSITAS_AZONOSITO = :id"
    cur.execute(sql, id=id)
    con.commit()
    cur.close()
    return redirect(url_for('insurance'))


@app.route('/accommodations', methods=['GET', 'POST'])
def accommodations():
    msg = ''
    accommodation_list = []
    if request.method == 'POST' and \
            'id' in request.form and \
            'address' in request.form and \
            'city' in request.form and \
            'price' in request.form and \
            'name' in request.form:
        try:
            cur = con.cursor()
            cur.execute("INSERT INTO SZALLAS VALUES (:1, :2, :3, :4, :5)",
                        (request.form['id'], request.form['name'], request.form['price'], request.form['address'],
                         request.form['city']))
            con.commit()
            msg = 'A szallas sikeresen hozzaadva'
        except:
            msg = 'Szallas felvitele sikertelen'
    elif request.method == 'POST' and 'city_filter' in request.form:
        city_filter = request.form['city_filter']
        cost_from = request.form['cost_from']
        cost_to = request.form['cost_to']
        try:
            cost_from = int(cost_from)
            cost_to = int(cost_to)
            if cost_from > cost_to:
                raise Exception
        except:
            return redirect(url_for('accommodations'))
        action = request.form['action']
        cur = con.cursor()
        filter = request.form['city_filter']
        if action == 'Osszes':
            cur.execute("SELECT * FROM SZALLAS")
            accommodation_list = cur.fetchall()
        elif action == 'Sajat utazasokhoz':
            output_cursor = cur.var(oracledb.DB_TYPE_CURSOR)
            cur.execute("""
                DECLARE
                    person_id SZEMELY.Szemelyi_szam%TYPE;
                    hotel_cursor SYS_REFCURSOR;
                BEGIN
                    SELECT SZEMELYI_SZAM INTO person_id FROM SZEMELY WHERE EMAIL = :email;

                    OPEN hotel_cursor FOR
                    WITH cities AS (
                        SELECT Varos_Kod FROM (
                            SELECT Varos_Kod
                            FROM JARAT
                            JOIN UTAZAS ON JARAT.Jarat_szam = UTAZAS.Jarat_szam
                            WHERE UTAZAS.Szemelyi_szam = person_id
                            GROUP BY Varos_Kod
                        )
                    )
                    SELECT * FROM SZALLAS WHERE Varos_Kod IN (SELECT Varos_Kod FROM cities);
                    :output_cursor := hotel_cursor;
                END;""",
                        email=session['email'], output_cursor=output_cursor)
            accommodation_list = output_cursor.getvalue().fetchall()
        elif city_filter == 'relevant':
            output_cursor = cur.var(oracledb.DB_TYPE_CURSOR)
            cur.execute("""
                DECLARE
                    person_id SZEMELY.Szemelyi_szam%TYPE;
                    hotel_cursor SYS_REFCURSOR;
                BEGIN
                    SELECT SZEMELYI_SZAM INTO person_id FROM SZEMELY WHERE EMAIL = :email;
                    
                    OPEN hotel_cursor FOR
                    WITH cities AS (
                        SELECT Varos_Kod
                        FROM (
                            SELECT Varos_Kod
                            FROM JARAT
                            JOIN UTAZAS ON JARAT.Jarat_szam = UTAZAS.Jarat_szam
                            WHERE UTAZAS.Szemelyi_szam = person_id
                            GROUP BY Varos_Kod
                        )
                    ),
                    hotels AS (
                        SELECT * 
                        FROM SZALLAS
                        WHERE Varos_Kod IN (SELECT Varos_Kod FROM cities)
                    )
                    SELECT * 
                    FROM hotels 
                    WHERE (CAST(:cost_from AS NUMERIC) <= Ar) AND (Ar <= CAST(:cost_to AS NUMERIC));
                        
                    :output_cursor := hotel_cursor;
                END;""",
                        email=session['email'],
                        cost_from=str(cost_from),
                        cost_to=str(cost_to),
                        output_cursor=output_cursor,
                        )
            accommodation_list = output_cursor.getvalue().fetchall()
        elif city_filter == 'any':
            cur.execute("SELECT * FROM SZALLAS WHERE (:cost_from <= Ar) AND (Ar <= :cost_to)", cost_from=cost_from,
                        cost_to=cost_to)
            accommodation_list = cur.fetchall()
        else:
            try:
                cur.execute(
                    "SELECT * FROM SZALLAS WHERE (Varos_Kod = :city_code) AND  (:cost_from <= Ar) AND (Ar <= :cost_to)",
                    city_code=filter, cost_from=cost_from, cost_to=cost_to)
                accommodation_list = cur.fetchall()
            except:
                cur.close()
                return redirect(url_for(accommodations))
        cur.close()
    else:
        cur = con.cursor()
        cur.execute("SELECT * FROM SZALLAS")
        accommodation_list = cur.fetchall()
        cur.close()
    cur = con.cursor()
    cur.execute("SELECT Neve, Kod FROM VAROS")
    cities = cur.fetchall()
    cur.close()
    return render_template(
        'accommodations.html',
        cities=cities,
        accommodations=accommodation_list,
        is_user_logged_in=is_user_logged_in(),
        admin_privilege=is_user_admin(),
        msg=msg,
        active='accommodations'
    )


@app.route('/accommodation/<id>/delete')
def delete_accommodation(id):
    cur = con.cursor()
    sql = "DELETE FROM SZALLAS WHERE AZONOSITO = :id"
    cur.execute(sql, id=id)
    con.commit()
    cur.close()
    return redirect(url_for('accommodations'))


# ADMIN BEJELENTKEZÉS: sima bejelentkezés email:admin password:admin, majd /admin megnyitása
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if is_user_logged_in:
        cur = con.cursor()
        sql = "SELECT Is_Admin FROM SZEMELY WHERE Email = :email"
        cur.execute(sql, email=session['email'])
        is_admin = False if cur.fetchone()[0] == 0 else True
        cur.close()
        if is_admin:
            admin_user = "Admin vagy!"
            session['admin'] = True
            return render_template('admin.html', is_admin=admin_user, active='index')
    return redirect(url_for('index'))


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
                cur.execute(sql, id_number=request.form['id-number'], name=request.form['name'],
                            email=request.form['email'])
                con.commit()
                msg = 'A felhasznalo sikeresen frissitve'
    return render_template('manage_user.html', msg=msg, active='manage_user', admin_privilege=is_user_admin())


@app.route('/manage_flights', methods=['GET', 'POST'])
def manage_flights():
    msg = ''
    cur = con.cursor()
    cur.execute("SELECT * FROM UTAZAS")
    flights_list = cur.fetchall()
    if request.method == 'POST' and \
            'flight_number' in request.form and \
            'old_flight_number' in request.form and \
            'action' in request.form:
        if request.form['action'] == 'Fríssités':
            if ('flight_number' not in request.form or 'id-number' not in request.form or
                    'old_flight_number' not in request.form):
                msg = 'Az szemelyi azonosito es a járat számok megadasa is szukseges'
            else:
                cur = con.cursor()
                sql = """UPDATE UTAZAS 
                     SET JARAT_SZAM = :flight_number 
                     WHERE SZEMELYI_SZAM = :id_number AND JARAT_SZAM = :old_flight_number"""
                cur.execute(sql, id_number=request.form['id-number'], flight_number=request.form['flight_number'],
                            old_flight_number=request.form['old_flight_number'])
                con.commit()
                cur = con.cursor()
                cur.execute("SELECT * FROM UTAZAS")
                flights_list = cur.fetchall()
                msg = 'A járat sikeresen frissitve'
        if request.form['action'] == 'Törlés':
            if 'flight_number' not in request.form or 'id-number' not in request.form:
                msg = 'Az szemelyi azonosito es a járat szám megadasa is szukseges'
            else:
                cur = con.cursor()
                sql = """DELETE FROM UTAZAS 
                                     WHERE SZEMELYI_SZAM = :id_number AND JARAT_SZAM = :flight_number"""
                cur.execute(sql, id_number=request.form['id-number'], flight_number=request.form['flight_number'])
                con.commit()
                cur.close()
                cur = con.cursor()
                cur.execute("SELECT * FROM UTAZAS")
                flights_list = cur.fetchall()
                cur.close()
                msg = 'A járat sikeresen törölve'
    return render_template(
        'manage_flights.html',
        msg=msg,
        flights=flights_list,
        active='manage_flights',
        admin_privilege=is_user_admin()
    )


def get_user_points():
    cur = con.cursor()
    cur.execute("SELECT PONT FROM SZEMELY WHERE EMAIL = :user_email", user_email=session['email'])
    user_points = cur.fetchone()[0]
    cur.close()
    return user_points


def is_user_logged_in():
    return True if 'loggedin' in session else False


def is_user_admin():
    return True if 'admin' in session else False


app.run(host='0.0.0.0', port=5000)
