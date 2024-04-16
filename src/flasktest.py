from flask import Flask, render_template
import oracledb

cs = "localhost:1521/freepdb1"
con = oracledb.connect(
    user="SYSTEM", password='jelszo', dsn=cs
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', connection=con.instance_name)


app.run(host='0.0.0.0', port=80)
