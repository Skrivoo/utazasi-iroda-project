# Utazási iroda project

#### A dokumentáció
A dokumentáció LaTeX-ben íródott. Compileoláshoz itt egy segédlet. Ha jetbrains IDEA-t használunk, töltsük le [ezt](https://plugins.jetbrains.com/plugin/9473-texify-idea) a plugint. A használathoz töltsük le a MiKTeX-et [itt](https://miktex.org/download). Állítsuk be az SDK-t, a default elérési útvonal windowon `C:\Users\Username\AppData\Local\Programs\MiKTeX`. Ezek után a `main.tex`-ből már compile-olható a pdf.

#### Az adatbázis
Az Oracle database 23-ra esett a választás. Felhasznált image: https://hub.docker.com/r/gvenzl/oracle-free
Kell egy docker desktop, windows-on hasznos ha WSL2-vel össze van kötve.
`docker run -d -p 1521:1521 -e ORACLE_PASSWORD=jelszo -v oracle-volume:/opt/oracle/oradata gvenzl/oracle-free`

#### Programozási környezet
Python-t használtunk és Flask framework-öt. Bootstrap lett felhasználva a kinézethez. Fejlesztéshez a következő lépések elvégzése szükséges.
Terminálban a repón belül:
`python -m venv utazasiiroda` majd `source utazasiiroda/bin/activate`
`pip install -r requirements.txt`