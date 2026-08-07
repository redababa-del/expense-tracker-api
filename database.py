import psycopg2

import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn




def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS utilisateurs(
            id SERIAL PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS depenses(
            id SERIAL PRIMARY KEY,
            montant NUMERIC(10,2) NOT NULL,
            categorie VARCHAR(100) NOT NULL,
            date DATE NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES utilisateurs(id)
        );
        """
    )

    conn.commit()
    conn.close()


def create_depense(montant, categorie, date, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO depenses (montant, categorie, date, user_id)
        VALUES (%s, %s, %s, %s)
    """, (montant, categorie, date, user_id))

    conn.commit()
    cursor.close()
    conn.close()


def get_all_depenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM depenses
    """)

    depenses = cursor.fetchall()

    cursor.close()
    conn.close()
    return depenses


def get_depense_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM depenses
        WHERE id = %s
    """, (id,))

    depense = cursor.fetchone()

    cursor.close()
    conn.close()
    return depense


def get_depenses_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM depenses 
        WHERE user_id = %s
    """, (user_id,))

    depenses = cursor.fetchall()

    cursor.close()
    conn.close()
    return depenses


def total_depenses_par_utilisateur(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(montant), 0)
        FROM depenses
        WHERE user_id = %s
    """, (user_id,))

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return total


def update_depense(id, montant, categorie, date, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE depenses
        SET montant = %s,
            categorie = %s,
            date = %s,
            user_id = %s
        WHERE id = %s
    """, (montant, categorie, date, user_id, id))

    conn.commit()
    cursor.close()
    conn.close()


def delete_depense(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM depenses
        WHERE id = %s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()


def total_par_categorie():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT categorie, SUM(montant)
        FROM depenses
        GROUP BY categorie
    """)

    resultats = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultats


def total_par_mois():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE_TRUNC('month', date) AS mois, SUM(montant)
        FROM depenses
        GROUP BY mois
    """)

    resultats = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultats


def ajouter_utilisateur(nom, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO utilisateurs (nom, email)
        VALUES (%s, %s)
    """, (nom, email))

    conn.commit()
    cursor.close()
    conn.close()








if __name__ == "__main__":
    conn = get_connection()
    print("Connexion réussie !")
    init_db()
    conn.close()