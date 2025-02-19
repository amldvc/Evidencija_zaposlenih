from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import mysql.connector
import hashlib

from datetime import timedelta
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app, supports_credentials=True)


from dotenv import load_dotenv
import os

# Učitavanje .env fajla
load_dotenv()

# Dobijanje vrednosti promenljivih okruženja
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")

print(f"DB_PORT iz .env: {db_port}")  # Provera da li se učitava ispravno

# Konekcija sa bazom
konekcija = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name,
    port=int(db_port)  # Pretvaramo u int jer dolazi kao string
)

# Funkcija za formatiranje vremena
def formatiraj_vreme(termin):
    """
    Pretvara vreme iz formata "8:00:00", "08:00:00" ili "8:00" u slot, npr. "08:00 - 09:30".
    """
    try:
        # Ako je 'termin' objekat tipa datetime.time, konvertuj ga u format HH:MM:SS
        formatted_time = termin.strftime("%H:%M:%S")
    except AttributeError:
        # Ako je 'termin' string, proveri format:
        parts = termin.split(":")
        if len(parts) == 2:
            # Format "H:M" (bez sekundi) – dopuni sa ":00" i dodaj vodeću nulom za sat ako je potrebno
            hour, minute = parts
            formatted_time = f"{int(hour):02}:{minute}:00"
        elif len(parts) == 3:
            # Format "H:M:S" – osiguraj vodeću nulom za sat
            hour, minute, second = parts
            formatted_time = f"{int(hour):02}:{minute}:{second}"
        else:
            formatted_time = termin  # Ako format nije prepoznat, vrati original
 
    # Mapa slotova – koristi normalizovani format (HH:MM:SS)
    vremenski_slotovi = {
        "08:00:00": "08:00 - 09:30",
        "09:30:00": "09:30 - 11:00",
        "11:00:00": "11:00 - 12:30",
        "13:00:00": "13:00 - 14:30",
        "14:30:00": "14:30 - 16:00"
    }
    return vremenski_slotovi.get(formatted_time, formatted_time)

# Funkcija za generisanje lozinke
def generate_password(ime):
    plain_password = ime + "2025"
    return plain_password  # Nema više hash-a, vraćamo samo običan tekst
 
from datetime import date, datetime
 
# Ruta za prikazivanje zaposlenih 
@app.route('/api/zaposleni', methods=['GET'])
def zaposleni():
    with konekcija.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM zaposleni")
        zaposleni_lista = cursor.fetchall()
 
    # Formatiraj datum za svakog zaposlenog
    for zaposleni in zaposleni_lista:
        datum_zaposlenja = zaposleni['datum_zaposlenja']
        # Ispis radi debugovanja
        print(f"Originalni datum: {datum_zaposlenja} (type: {type(datum_zaposlenja)})")
        if isinstance(datum_zaposlenja, date):
            # Ako je već date (ili datetime) objekat, formatiraj ga
            zaposleni['datum_zaposlenja'] = datum_zaposlenja.strftime("%d.%m.%Y")
            print(f"Formatirani datum: {zaposleni['datum_zaposlenja']}")
        elif isinstance(datum_zaposlenja, str):
            # Ako je datum string, pokušaj da ga parsiraš kao ISO format ("YYYY-MM-DD")
            try:
                parsed_date = date.fromisoformat(datum_zaposlenja)
                zaposleni['datum_zaposlenja'] = parsed_date.strftime("%d.%m.%Y")
                print(f"Formatirani datum (parsed): {zaposleni['datum_zaposlenja']}")
            except Exception as e:
                print(f"Greška pri parsiranju stringa datuma: {datum_zaposlenja} - {e}")
                # Ako parsiranje ne uspe, ostavi originalnu vrednost
                zaposleni['datum_zaposlenja'] = datum_zaposlenja
        else:
            print(f"Greška: datum_zaposlenja nije tipa date ili string, već: {type(datum_zaposlenja)}")
            zaposleni['datum_zaposlenja'] = str(datum_zaposlenja)
 
    return jsonify(zaposleni_lista)

# Ruta za dodavanje zaposlenog
@app.route('/api/dodaj_zaposlenog', methods=['POST'])
def dodaj_zaposlenog():
    data = request.json  # Koristimo JSON umesto FormData
    imeiprezime = data.get('imeiprezime')
    pozicija = data.get('pozicija')
    datum_zaposlenja = data.get('datumzaposlenja', '')  
    mejl = data.get('email')
    kontakt = data.get('kontakt')

    if " " in imeiprezime:
        ime, prezime = imeiprezime.split(" ", 1)
    else:
        ime, prezime = imeiprezime, ""

    cursor = konekcija.cursor(dictionary=True)

    try:
        # Dodavanje zaposlenog u tabelu zaposleni
        cursor.execute("""
            INSERT INTO zaposleni (ime, prezime, pozicija, datum_zaposlenja, mejl, kontakt)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (ime, prezime, pozicija, datum_zaposlenja, mejl, kontakt))
        konekcija.commit()

        # Generisanje lozinke (ime + 2025)
        password = generate_password(ime)

        # Provera da li mejl već postoji u korisnicima
        cursor.execute("SELECT * FROM korisnici WHERE email = %s", (mejl,))
        existing_user = cursor.fetchone()

        if not existing_user:
            cursor.execute("""
                INSERT INTO korisnici (email, lozinka, uloga)
                VALUES (%s, %s, %s)
            """, (mejl, password, pozicija))
            konekcija.commit()

        return jsonify({"message": "Zaposleni uspešno dodat!"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()

# Ruta za prikaz rasporeda rada
from flask import jsonify

@app.route('/api/radnik_raspored', methods=['GET'])
def api_radnik_raspored():
    role = session.get("role")
    user_email = session.get("user")

    # Sada uvek ostaje None, dok korisnik sam ne odabere
    odabrani_zaposleni_id = None

    zaposleni_lista = []
    with konekcija.cursor(dictionary=True) as cursor:
        if role == "menadzer":
            # Menadžer vidi sve zaposlene
            cursor.execute("SELECT id, ime, prezime FROM zaposleni")
            zaposleni_lista = cursor.fetchall()
        elif role == "radnik":
            cursor.execute("SELECT id, ime, prezime FROM zaposleni WHERE mejl = %s", (user_email,))
            zaposleni_lista = cursor.fetchall()
        if zaposleni_lista:
            odabrani_zaposleni_id = zaposleni_lista[0]["id"]

    return jsonify({
        "zaposleni_lista": zaposleni_lista,
        "odabrani_zaposleni_id": odabrani_zaposleni_id,  # Ostaće None
        "role": role
    })

@app.route('/api/radnik_raspored/<int:zaposleni_id>', methods=['GET'])
def api_dohvati_raspored(zaposleni_id):
    raspored = {}
    with konekcija.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT dan, termin, klijent FROM raspored_rada WHERE zaposleni_id = %s", (zaposleni_id,))
        rezultati = cursor.fetchall()
 
        for red in rezultati:
            dan = red['dan']
            termin = formatiraj_vreme(str(red['termin']))
            klijent = red['klijent']
 
            if dan not in raspored:
                raspored[dan] = {}
 
            raspored[dan][termin] = klijent
 
    print("Podaci koji se šalju:", raspored)  # OVO JE BITNO ZA DEBEGING!
    return jsonify({"raspored": raspored})

@app.route('/api/izmena_rasporeda', methods=['GET', 'POST'])
def izmena_rasporeda():
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({"error": "Nevalidan JSON format!"}), 400

        zaposleni_id = data.get('zaposleni_id')
        dan = data.get('dan')
        termin = data.get('termin')
        klijent = data.get('klijent')

        if not zaposleni_id or not dan or not termin or not klijent:
            return jsonify({"error": "Sva polja su obavezna!"}), 400

        # Normalizacija vrednosti
        dan = dan.capitalize()
        termin = termin.strip()

        with konekcija.cursor() as cursor:
            # Brišemo postojeći termin ako postoji
            cursor.execute("""
                DELETE FROM raspored_rada 
                WHERE zaposleni_id = %s AND dan = %s AND termin = %s
            """, (zaposleni_id, dan, termin))

            # Ubacujemo novi termin
            cursor.execute("""
                INSERT INTO raspored_rada (zaposleni_id, dan, termin, klijent) 
                VALUES (%s, %s, %s, %s)
            """, (zaposleni_id, dan, termin, klijent))

            konekcija.commit()

        return jsonify({"message": "Termin uspešno dodat!"}), 201

    # GET - Dobavljanje podataka o rasporedu
    with konekcija.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id, ime, prezime FROM zaposleni")
        zaposleni_lista = cursor.fetchall()

        cursor.execute("""
            SELECT r.id, r.dan, r.termin, r.klijent, z.ime, z.prezime
            FROM raspored_rada r
            JOIN zaposleni z ON r.zaposleni_id = z.id
            ORDER BY FIELD(r.dan, 'Ponedeljak', 'Utorak', 'Sreda', 'Četvrtak', 'Petak'), r.termin
        """)
        raspored_podaci = cursor.fetchall()

    # Formiranje JSON odgovora
    raspored = {}
    for red in raspored_podaci:
        dan = red['dan']
        termin = str(red['termin'])  # Konvertovanje timedelta u string
        klijent = red['klijent']
        ime_prezime = f"{red['ime']} {red['prezime']} ({klijent})"

        if dan not in raspored:
            raspored[dan] = {}

    raspored[dan][termin] = {
        "id": red['id'],
        "zaposleni": ime_prezime
    }

    return jsonify({
        "zaposleni_lista": zaposleni_lista,
        "raspored": raspored
    })


@app.route('/api/obrisi_termin', methods=['DELETE'])
def obrisi_termin():
    if 'user' not in session or session.get('role') != 'menadzer':
        return jsonify({"error": "Nemate dozvolu za ovu akciju."}), 403

    data = request.json
    termin_id = data.get('termin_id')

    if not termin_id:
        return jsonify({"error": "Nedostaje termin_id"}), 400

    with konekcija.cursor() as cursor:
        cursor.execute("DELETE FROM raspored_rada WHERE id = %s", (termin_id,))
        konekcija.commit()

    return jsonify({"message": "Termin uspešno obrisan!"}), 200


# Stranica menadžera
@app.route('/api/menadzer', methods=['GET'])
def menadzer(): 
    
    with konekcija.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM zaposleni WHERE pozicija = 'menadzer'")
        podaci = cursor.fetchall()

    return jsonify({"zaposleni": podaci})


# Login stranica
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    print("Primljen zahtev:", data)  # <--- Loguj primljene podatke
    
    email = data.get('email')
    password = data.get('password')

    cursor = konekcija.cursor(dictionary=True)
    cursor.execute("SELECT * FROM korisnici WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    cursor = konekcija.cursor(dictionary=True)
    cursor.execute("SELECT id FROM zaposleni WHERE mejl = %s", (email,))
    zaposleni_id = cursor.fetchone()
    cursor.close()
    print(zaposleni_id)

    print("Korisnik iz baze:", user)  # <--- Loguj podatke iz baze

    if user:
        ime = email.split("@")[0].capitalize()
        expected_password = ime + "2025"

        print("Očekivana lozinka:", expected_password)  # <--- Loguj generisanu lozinku

        if user['lozinka'] == expected_password:
            session['user'] = email
            session['role'] = user['uloga']

            normalizovana_uloga = user['uloga'].lower().replace("ž", "z")

            roles_map = {
                "admin": "zaposleni",
                "menadzer": "menadzer",
                "radnik": "radnik_raspored"
            }

            role_redirect = roles_map.get(normalizovana_uloga, 'login')

            print(user)

            return jsonify({
                'status': 'success',
                'ulogovan_id': zaposleni_id['id'],  # Vraća ID ulogovanog korisnika
                'redirect': role_redirect
            })

        else:
            print("Pogrešna lozinka!")
            return jsonify({'status': 'error', 'message': 'Pogrešna lozinka!'}), 400
    else:
        print("Ne postoji nalog sa tim emailom!")
        return jsonify({'status': 'error', 'message': 'Ne postoji nalog sa tim emailom!'}), 400


# Logout
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    session.pop('role', None)  # Uklanjamo i ulogu korisnika iz sesije
    return jsonify({"message": "Uspešno ste se odjavili."}), 200

if __name__ == '__main__':
    app.config["DEBUG"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = True

    app.run(debug=True)