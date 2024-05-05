CREATE TABLE VAROS (
    Kod VARCHAR2(50) PRIMARY KEY,
    Neve VARCHAR2(255) NOT NULL,
    Orszag VARCHAR2(100) NOT NULL
);

CREATE TABLE LEGITARSASAG (
    Ceg_kod VARCHAR2(50) PRIMARY KEY,
    Nev VARCHAR2(255) NOT NULL
);

CREATE TABLE SZEMELY (
    Szemelyi_szam VARCHAR2(20) PRIMARY KEY,
    Nev VARCHAR2(255) NOT NULL,
    Szul_ev DATE NOT NULL,
    Email VARCHAR2(255) NOT NULL,
    PASSWD VARCHAR2(255) NOT NULL
);

CREATE TABLE SZALLAS (
    Azonosito VARCHAR2(50) PRIMARY KEY,
    Neve VARCHAR2(255) NOT NULL,
    Ar NUMBER NOT NULL,
    Cim VARCHAR2(255) NOT NULL,
    Varos_kod VARCHAR2(50),
    CONSTRAINT FK_Varos_Kod FOREIGN KEY (Varos_kod)
    REFERENCES VAROS (Kod) ON DELETE SET NULL
);

CREATE TABLE BIZTOSITAS (
    Biztositas_azonosito VARCHAR2(50) PRIMARY KEY,
    Tipus VARCHAR2(100) NOT NULL,
    Lejarat DATE NOT NULL,
    Erteke NUMBER NOT NULL
);

CREATE TABLE GEP (
    Gep_szama VARCHAR2(50) PRIMARY KEY,
    Gep_tipusa VARCHAR2(100) NOT NULL,
    Ulohelyek_szama NUMBER NOT NULL
);

CREATE TABLE JARAT (
    Jarat_szam VARCHAR2(50) PRIMARY KEY,
    Hova VARCHAR2(255) NOT NULL,
    Honnan VARCHAR2(255) NOT NULL,
    Ido TIMESTAMP NOT NULL,
    Gep_szama VARCHAR2(50) NOT NULL,
    Varos_kod VARCHAR2(50) NOT NULL,
    CONSTRAINT FK_Gep_Szama FOREIGN KEY (Gep_szama)
    REFERENCES GEP (Gep_szama) ON DELETE CASCADE,
    CONSTRAINT FK_Varos_Kod_Jarat FOREIGN KEY (Varos_kod)
    REFERENCES VAROS (Kod) ON DELETE CASCADE
);

CREATE TABLE UTAZAS (
    Szemelyi_szam VARCHAR2(20),
    Jarat_szam VARCHAR2(50),
    Ules_szam VARCHAR2(50),
    PRIMARY KEY (Szemelyi_szam, Jarat_szam),
    CONSTRAINT FK_Szemelyi_Szam FOREIGN KEY (Szemelyi_szam)
    REFERENCES SZEMELY (Szemelyi_szam) ON DELETE CASCADE,
    CONSTRAINT FK_Jarat_Szam FOREIGN KEY (Jarat_szam)
    REFERENCES JARAT (Jarat_szam) ON DELETE CASCADE
);

INSERT INTO VAROS VALUES ('VAR001', 'City1', 'Country1');
INSERT INTO VAROS VALUES ('VAR002', 'City2', 'Country2');
INSERT INTO VAROS VALUES ('VAR003', 'City3', 'Country3');
INSERT INTO VAROS VALUES ('VAR004', 'City4', 'Country4');
INSERT INTO VAROS VALUES ('VAR005', 'City5', 'Country5');
INSERT INTO VAROS VALUES ('VAR006', 'City6', 'Country6');
INSERT INTO VAROS VALUES ('VAR007', 'City7', 'Country7');
INSERT INTO VAROS VALUES ('VAR008', 'City8', 'Country8');
INSERT INTO VAROS VALUES ('VAR009', 'City9', 'Country9');
INSERT INTO VAROS VALUES ('VAR010', 'City10', 'Country0');
INSERT INTO VAROS VALUES ('VAR011', 'City11', 'Country1');
INSERT INTO VAROS VALUES ('VAR012', 'City12', 'Country2');
INSERT INTO VAROS VALUES ('VAR013', 'City13', 'Country3');
INSERT INTO VAROS VALUES ('VAR014', 'City14', 'Country4');
INSERT INTO VAROS VALUES ('VAR015', 'City15', 'Country5');
INSERT INTO VAROS VALUES ('VAR016', 'City16', 'Country6');
INSERT INTO VAROS VALUES ('VAR017', 'City17', 'Country7');
INSERT INTO VAROS VALUES ('VAR018', 'City18', 'Country8');
INSERT INTO VAROS VALUES ('VAR019', 'City19', 'Country9');
INSERT INTO VAROS VALUES ('VAR020', 'City20', 'Country0');
INSERT INTO VAROS VALUES ('VAR021', 'City21', 'Country1');
INSERT INTO VAROS VALUES ('VAR022', 'City22', 'Country2');
INSERT INTO VAROS VALUES ('VAR023', 'City23', 'Country3');
INSERT INTO VAROS VALUES ('VAR024', 'City24', 'Country4');
INSERT INTO VAROS VALUES ('VAR025', 'City25', 'Country5');
INSERT INTO VAROS VALUES ('VAR026', 'City26', 'Country6');
INSERT INTO VAROS VALUES ('VAR027', 'City27', 'Country7');
INSERT INTO VAROS VALUES ('VAR028', 'City28', 'Country8');
INSERT INTO VAROS VALUES ('VAR029', 'City29', 'Country9');
INSERT INTO VAROS VALUES ('VAR030', 'City30', 'Country0');
INSERT INTO LEGITARSASAG VALUES ('LG001', 'Airline1');
INSERT INTO LEGITARSASAG VALUES ('LG002', 'Airline2');
INSERT INTO LEGITARSASAG VALUES ('LG003', 'Airline3');
INSERT INTO LEGITARSASAG VALUES ('LG004', 'Airline4');
INSERT INTO LEGITARSASAG VALUES ('LG005', 'Airline5');
INSERT INTO LEGITARSASAG VALUES ('LG006', 'Airline6');
INSERT INTO LEGITARSASAG VALUES ('LG007', 'Airline7');
INSERT INTO LEGITARSASAG VALUES ('LG008', 'Airline8');
INSERT INTO LEGITARSASAG VALUES ('LG009', 'Airline9');
INSERT INTO LEGITARSASAG VALUES ('LG010', 'Airline10');
INSERT INTO LEGITARSASAG VALUES ('LG011', 'Airline11');
INSERT INTO LEGITARSASAG VALUES ('LG012', 'Airline12');
INSERT INTO LEGITARSASAG VALUES ('LG013', 'Airline13');
INSERT INTO LEGITARSASAG VALUES ('LG014', 'Airline14');
INSERT INTO LEGITARSASAG VALUES ('LG015', 'Airline15');
INSERT INTO LEGITARSASAG VALUES ('LG016', 'Airline16');
INSERT INTO LEGITARSASAG VALUES ('LG017', 'Airline17');
INSERT INTO LEGITARSASAG VALUES ('LG018', 'Airline18');
INSERT INTO LEGITARSASAG VALUES ('LG019', 'Airline19');
INSERT INTO LEGITARSASAG VALUES ('LG020', 'Airline20');
INSERT INTO LEGITARSASAG VALUES ('LG021', 'Airline21');
INSERT INTO LEGITARSASAG VALUES ('LG022', 'Airline22');
INSERT INTO LEGITARSASAG VALUES ('LG023', 'Airline23');
INSERT INTO LEGITARSASAG VALUES ('LG024', 'Airline24');
INSERT INTO LEGITARSASAG VALUES ('LG025', 'Airline25');
INSERT INTO LEGITARSASAG VALUES ('LG026', 'Airline26');
INSERT INTO LEGITARSASAG VALUES ('LG027', 'Airline27');
INSERT INTO LEGITARSASAG VALUES ('LG028', 'Airline28');
INSERT INTO LEGITARSASAG VALUES ('LG029', 'Airline29');
INSERT INTO LEGITARSASAG VALUES ('LG030', 'Airline30');
INSERT INTO SZEMELY VALUES ('ID00001', 'Person1', TO_DATE('1971-01-01', 'YYYY-MM-DD'), 'email1@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00002', 'Person2', TO_DATE('1972-01-01', 'YYYY-MM-DD'), 'email2@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00003', 'Person3', TO_DATE('1973-01-01', 'YYYY-MM-DD'), 'email3@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00004', 'Person4', TO_DATE('1974-01-01', 'YYYY-MM-DD'), 'email4@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00005', 'Person5', TO_DATE('1975-01-01', 'YYYY-MM-DD'), 'email5@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00006', 'Person6', TO_DATE('1976-01-01', 'YYYY-MM-DD'), 'email6@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00007', 'Person7', TO_DATE('1977-01-01', 'YYYY-MM-DD'), 'email7@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00008', 'Person8', TO_DATE('1978-01-01', 'YYYY-MM-DD'), 'email8@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00009', 'Person9', TO_DATE('1979-01-01', 'YYYY-MM-DD'), 'email9@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00010', 'Person10', TO_DATE('1980-01-01', 'YYYY-MM-DD'), 'email10@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00011', 'Person11', TO_DATE('1981-01-01', 'YYYY-MM-DD'), 'email11@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00012', 'Person12', TO_DATE('1982-01-01', 'YYYY-MM-DD'), 'email12@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00013', 'Person13', TO_DATE('1983-01-01', 'YYYY-MM-DD'), 'email13@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00014', 'Person14', TO_DATE('1984-01-01', 'YYYY-MM-DD'), 'email14@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00015', 'Person15', TO_DATE('1985-01-01', 'YYYY-MM-DD'), 'email15@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00016', 'Person16', TO_DATE('1986-01-01', 'YYYY-MM-DD'), 'email16@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00017', 'Person17', TO_DATE('1987-01-01', 'YYYY-MM-DD'), 'email17@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00018', 'Person18', TO_DATE('1988-01-01', 'YYYY-MM-DD'), 'email18@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00019', 'Person19', TO_DATE('1989-01-01', 'YYYY-MM-DD'), 'email19@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00020', 'Person20', TO_DATE('1990-01-01', 'YYYY-MM-DD'), 'email20@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00021', 'Person21', TO_DATE('1991-01-01', 'YYYY-MM-DD'), 'email21@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00022', 'Person22', TO_DATE('1992-01-01', 'YYYY-MM-DD'), 'email22@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00023', 'Person23', TO_DATE('1993-01-01', 'YYYY-MM-DD'), 'email23@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00024', 'Person24', TO_DATE('1994-01-01', 'YYYY-MM-DD'), 'email24@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00025', 'Person25', TO_DATE('1995-01-01', 'YYYY-MM-DD'), 'email25@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00026', 'Person26', TO_DATE('1996-01-01', 'YYYY-MM-DD'), 'email26@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00027', 'Person27', TO_DATE('1997-01-01', 'YYYY-MM-DD'), 'email27@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00028', 'Person28', TO_DATE('1998-01-01', 'YYYY-MM-DD'), 'email28@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00029', 'Person29', TO_DATE('1999-01-01', 'YYYY-MM-DD'), 'email29@cim.com', 'erosjelszo1');
INSERT INTO SZEMELY VALUES ('ID00030', 'Person30', TO_DATE('2000-01-01', 'YYYY-MM-DD'), 'email30@cim.com', 'erosjelszo1');
INSERT INTO SZALLAS VALUES ('SZL001', 'Hotel 1', 1050, 'Address 1, City 1', 'VAR002');
INSERT INTO SZALLAS VALUES ('SZL002', 'Hotel 2', 1100, 'Address 2, City 2', 'VAR003');
INSERT INTO SZALLAS VALUES ('SZL003', 'Hotel 3', 1150, 'Address 3, City 3', 'VAR004');
INSERT INTO SZALLAS VALUES ('SZL004', 'Hotel 4', 1200, 'Address 4, City 4', 'VAR005');
INSERT INTO SZALLAS VALUES ('SZL005', 'Hotel 5', 1250, 'Address 5, City 5', 'VAR006');
INSERT INTO SZALLAS VALUES ('SZL006', 'Hotel 6', 1300, 'Address 6, City 6', 'VAR007');
INSERT INTO SZALLAS VALUES ('SZL007', 'Hotel 7', 1350, 'Address 7, City 7', 'VAR008');
INSERT INTO SZALLAS VALUES ('SZL008', 'Hotel 8', 1400, 'Address 8, City 8', 'VAR009');
INSERT INTO SZALLAS VALUES ('SZL009', 'Hotel 9', 1450, 'Address 9, City 9', 'VAR010');
INSERT INTO SZALLAS VALUES ('SZL010', 'Hotel 10', 1500, 'Address 10, City 10', 'VAR011');
INSERT INTO SZALLAS VALUES ('SZL011', 'Hotel 11', 1550, 'Address 11, City 11', 'VAR012');
INSERT INTO SZALLAS VALUES ('SZL012', 'Hotel 12', 1600, 'Address 12, City 12', 'VAR013');
INSERT INTO SZALLAS VALUES ('SZL013', 'Hotel 13', 1650, 'Address 13, City 13', 'VAR014');
INSERT INTO SZALLAS VALUES ('SZL014', 'Hotel 14', 1700, 'Address 14, City 14', 'VAR015');
INSERT INTO SZALLAS VALUES ('SZL015', 'Hotel 15', 1750, 'Address 15, City 15', 'VAR016');
INSERT INTO SZALLAS VALUES ('SZL016', 'Hotel 16', 1800, 'Address 16, City 16', 'VAR017');
INSERT INTO SZALLAS VALUES ('SZL017', 'Hotel 17', 1850, 'Address 17, City 17', 'VAR018');
INSERT INTO SZALLAS VALUES ('SZL018', 'Hotel 18', 1900, 'Address 18, City 18', 'VAR019');
INSERT INTO SZALLAS VALUES ('SZL019', 'Hotel 19', 1950, 'Address 19, City 19', 'VAR020');
INSERT INTO SZALLAS VALUES ('SZL020', 'Hotel 20', 2000, 'Address 20, City 20', 'VAR021');
INSERT INTO SZALLAS VALUES ('SZL021', 'Hotel 21', 2050, 'Address 21, City 21', 'VAR022');
INSERT INTO SZALLAS VALUES ('SZL022', 'Hotel 22', 2100, 'Address 22, City 22', 'VAR023');
INSERT INTO SZALLAS VALUES ('SZL023', 'Hotel 23', 2150, 'Address 23, City 23', 'VAR024');
INSERT INTO SZALLAS VALUES ('SZL024', 'Hotel 24', 2200, 'Address 24, City 24', 'VAR025');
INSERT INTO SZALLAS VALUES ('SZL025', 'Hotel 25', 2250, 'Address 25, City 25', 'VAR026');
INSERT INTO SZALLAS VALUES ('SZL026', 'Hotel 26', 2300, 'Address 26, City 26', 'VAR027');
INSERT INTO SZALLAS VALUES ('SZL027', 'Hotel 27', 2350, 'Address 27, City 27', 'VAR028');
INSERT INTO SZALLAS VALUES ('SZL028', 'Hotel 28', 2400, 'Address 28, City 28', 'VAR029');
INSERT INTO SZALLAS VALUES ('SZL029', 'Hotel 29', 2450, 'Address 29, City 29', 'VAR030');
INSERT INTO SZALLAS VALUES ('SZL030', 'Hotel 30', 2500, 'Address 30, City 30', 'VAR001');
INSERT INTO BIZTOSITAS VALUES ('INS001', 'Health', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 1000);
INSERT INTO BIZTOSITAS VALUES ('INS002', 'Life', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 16000);
INSERT INTO BIZTOSITAS VALUES ('INS003', 'Car', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 15000);
INSERT INTO BIZTOSITAS VALUES ('INS004', 'Home', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 8000);
INSERT INTO BIZTOSITAS VALUES ('INS005', 'Travel', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 10000);
INSERT INTO BIZTOSITAS VALUES ('INS006', 'Health', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 15000);
INSERT INTO BIZTOSITAS VALUES ('INS007', 'Life', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 19000);
INSERT INTO BIZTOSITAS VALUES ('INS008', 'Car', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 19000);
INSERT INTO BIZTOSITAS VALUES ('INS009', 'Home', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 19000);
INSERT INTO BIZTOSITAS VALUES ('INS010', 'Travel', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 16000);
INSERT INTO BIZTOSITAS VALUES ('INS011', 'Health', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 2000);
INSERT INTO BIZTOSITAS VALUES ('INS012', 'Life', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 7000);
INSERT INTO BIZTOSITAS VALUES ('INS013', 'Car', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 4000);
INSERT INTO BIZTOSITAS VALUES ('INS014', 'Home', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 3000);
INSERT INTO BIZTOSITAS VALUES ('INS015', 'Travel', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 13000);
INSERT INTO BIZTOSITAS VALUES ('INS016', 'Health', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 12000);
INSERT INTO BIZTOSITAS VALUES ('INS017', 'Life', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 18000);
INSERT INTO BIZTOSITAS VALUES ('INS018', 'Car', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 3000);
INSERT INTO BIZTOSITAS VALUES ('INS019', 'Home', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 6000);
INSERT INTO BIZTOSITAS VALUES ('INS020', 'Travel', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 15000);
INSERT INTO BIZTOSITAS VALUES ('INS021', 'Health', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 8000);
INSERT INTO BIZTOSITAS VALUES ('INS022', 'Life', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 13000);
INSERT INTO BIZTOSITAS VALUES ('INS023', 'Car', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 18000);
INSERT INTO BIZTOSITAS VALUES ('INS024', 'Home', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 1000);
INSERT INTO BIZTOSITAS VALUES ('INS025', 'Travel', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 9000);
INSERT INTO BIZTOSITAS VALUES ('INS026', 'Health', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 3000);
INSERT INTO BIZTOSITAS VALUES ('INS027', 'Life', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 20000);
INSERT INTO BIZTOSITAS VALUES ('INS028', 'Car', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 11000);
INSERT INTO BIZTOSITAS VALUES ('INS029', 'Home', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 14000);
INSERT INTO BIZTOSITAS VALUES ('INS030', 'Travel', TO_DATE('2025-12-31', 'YYYY-MM-DD'), 4000);
INSERT INTO GEP VALUES ('AC001', 'Airbus A320', 211);
INSERT INTO GEP VALUES ('AC002', 'Boeing 777', 167);
INSERT INTO GEP VALUES ('AC003', 'Airbus A380', 189);
INSERT INTO GEP VALUES ('AC004', 'Boeing 787', 285);
INSERT INTO GEP VALUES ('AC005', 'Boeing 737', 239);
INSERT INTO GEP VALUES ('AC006', 'Airbus A320', 159);
INSERT INTO GEP VALUES ('AC007', 'Boeing 777', 252);
INSERT INTO GEP VALUES ('AC008', 'Airbus A380', 261);
INSERT INTO GEP VALUES ('AC009', 'Boeing 787', 219);
INSERT INTO GEP VALUES ('AC010', 'Boeing 737', 231);
INSERT INTO GEP VALUES ('AC011', 'Airbus A320', 232);
INSERT INTO GEP VALUES ('AC012', 'Boeing 777', 150);
INSERT INTO GEP VALUES ('AC013', 'Airbus A380', 170);
INSERT INTO GEP VALUES ('AC014', 'Boeing 787', 157);
INSERT INTO GEP VALUES ('AC015', 'Boeing 737', 109);
INSERT INTO GEP VALUES ('AC016', 'Airbus A320', 267);
INSERT INTO GEP VALUES ('AC017', 'Boeing 777', 173);
INSERT INTO GEP VALUES ('AC018', 'Airbus A380', 291);
INSERT INTO GEP VALUES ('AC019', 'Boeing 787', 205);
INSERT INTO GEP VALUES ('AC020', 'Boeing 737', 208);
INSERT INTO GEP VALUES ('AC021', 'Airbus A320', 165);
INSERT INTO GEP VALUES ('AC022', 'Boeing 777', 269);
INSERT INTO GEP VALUES ('AC023', 'Airbus A380', 282);
INSERT INTO GEP VALUES ('AC024', 'Boeing 787', 238);
INSERT INTO GEP VALUES ('AC025', 'Boeing 737', 182);
INSERT INTO GEP VALUES ('AC026', 'Airbus A320', 227);
INSERT INTO GEP VALUES ('AC027', 'Boeing 777', 193);
INSERT INTO GEP VALUES ('AC028', 'Airbus A380', 165);
INSERT INTO GEP VALUES ('AC029', 'Boeing 787', 141);
INSERT INTO GEP VALUES ('AC030', 'Boeing 737', 291);
INSERT INTO JARAT VALUES ('FL001', 'City18', 'City20', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC002', 'VAR002');
INSERT INTO JARAT VALUES ('FL002', 'City12', 'City11', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC003', 'VAR003');
INSERT INTO JARAT VALUES ('FL003', 'City23', 'City7', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC004', 'VAR004');
INSERT INTO JARAT VALUES ('FL004', 'City21', 'City1', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC005', 'VAR005');
INSERT INTO JARAT VALUES ('FL005', 'City30', 'City13', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC001', 'VAR001');
INSERT INTO JARAT VALUES ('FL006', 'City4', 'City13', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC002', 'VAR002');
INSERT INTO JARAT VALUES ('FL007', 'City1', 'City13', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC003', 'VAR003');
INSERT INTO JARAT VALUES ('FL008', 'City24', 'City19', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC004', 'VAR004');
INSERT INTO JARAT VALUES ('FL009', 'City28', 'City28', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC005', 'VAR005');
INSERT INTO JARAT VALUES ('FL010', 'City12', 'City23', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC001', 'VAR001');
INSERT INTO JARAT VALUES ('FL011', 'City6', 'City26', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC002', 'VAR002');
INSERT INTO JARAT VALUES ('FL012', 'City14', 'City25', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC003', 'VAR003');
INSERT INTO JARAT VALUES ('FL013', 'City12', 'City28', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC004', 'VAR004');
INSERT INTO JARAT VALUES ('FL014', 'City1', 'City17', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC005', 'VAR005');
INSERT INTO JARAT VALUES ('FL015', 'City30', 'City1', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC001', 'VAR001');
INSERT INTO JARAT VALUES ('FL016', 'City5', 'City20', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC002', 'VAR002');
INSERT INTO JARAT VALUES ('FL017', 'City21', 'City14', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC003', 'VAR003');
INSERT INTO JARAT VALUES ('FL018', 'City15', 'City15', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC004', 'VAR004');
INSERT INTO JARAT VALUES ('FL019', 'City25', 'City6', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC005', 'VAR005');
INSERT INTO JARAT VALUES ('FL020', 'City18', 'City21', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC001', 'VAR001');
INSERT INTO JARAT VALUES ('FL021', 'City18', 'City20', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC002', 'VAR002');
INSERT INTO JARAT VALUES ('FL022', 'City29', 'City23', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC003', 'VAR003');
INSERT INTO JARAT VALUES ('FL023', 'City6', 'City26', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC004', 'VAR004');
INSERT INTO JARAT VALUES ('FL024', 'City25', 'City2', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC005', 'VAR005');
INSERT INTO JARAT VALUES ('FL025', 'City6', 'City25', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC001', 'VAR001');
INSERT INTO JARAT VALUES ('FL026', 'City5', 'City18', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC002', 'VAR002');
INSERT INTO JARAT VALUES ('FL027', 'City7', 'City26', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC003', 'VAR003');
INSERT INTO JARAT VALUES ('FL028', 'City21', 'City25', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC004', 'VAR004');
INSERT INTO JARAT VALUES ('FL029', 'City4', 'City20', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC005', 'VAR005');
INSERT INTO JARAT VALUES ('FL030', 'City26', 'City12', TO_TIMESTAMP('2024-01-01 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'AC001', 'VAR001');
INSERT INTO UTAZAS VALUES ('ID00025', 'FL008', '2A');
INSERT INTO UTAZAS VALUES ('ID00007', 'FL025', '1A');
INSERT INTO UTAZAS VALUES ('ID00018', 'FL018', '10A');
INSERT INTO UTAZAS VALUES ('ID00014', 'FL026', '25A');
INSERT INTO UTAZAS VALUES ('ID00026', 'FL004', '20A');
INSERT INTO UTAZAS VALUES ('ID00026', 'FL014', '29A');
INSERT INTO UTAZAS VALUES ('ID00030', 'FL020', '13A');
INSERT INTO UTAZAS VALUES ('ID00014', 'FL004', '12A');
INSERT INTO UTAZAS VALUES ('ID00003', 'FL011', '3A');
INSERT INTO UTAZAS VALUES ('ID00011', 'FL004', '8A');
INSERT INTO UTAZAS VALUES ('ID00008', 'FL013', '3A');
INSERT INTO UTAZAS VALUES ('ID00017', 'FL028', '23A');
INSERT INTO UTAZAS VALUES ('ID00004', 'FL006', '22A');
INSERT INTO UTAZAS VALUES ('ID00021', 'FL018', '6A');
INSERT INTO UTAZAS VALUES ('ID00005', 'FL014', '28A');
INSERT INTO UTAZAS VALUES ('ID00002', 'FL001', '28A');
INSERT INTO UTAZAS VALUES ('ID00030', 'FL019', '13A');
INSERT INTO UTAZAS VALUES ('ID00017', 'FL026', '11A');
INSERT INTO UTAZAS VALUES ('ID00011', 'FL002', '5A');
INSERT INTO UTAZAS VALUES ('ID00009', 'FL012', '19A');
INSERT INTO UTAZAS VALUES ('ID00006', 'FL014', '24A');
INSERT INTO UTAZAS VALUES ('ID00012', 'FL008', '16A');
INSERT INTO UTAZAS VALUES ('ID00026', 'FL015', '9A');
INSERT INTO UTAZAS VALUES ('ID00027', 'FL005', '24A');
INSERT INTO UTAZAS VALUES ('ID00001', 'FL015', '5A');
INSERT INTO UTAZAS VALUES ('ID00024', 'FL014', '1A');
INSERT INTO UTAZAS VALUES ('ID00022', 'FL011', '29A');
INSERT INTO UTAZAS VALUES ('ID00008', 'FL006', '10A');

