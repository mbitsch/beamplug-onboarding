from datetime import datetime
import psycopg2
import os

def get_conn():
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return psycopg2.connect(database_url)
    else: 

        return psycopg2.connect(
            host="pg-145fc447-test1-d59a.g.aivencloud.com",      # fx "localhost"
            port=10580,             # standardport
            dbname="beam",     # navnet på din database i pgAdmin
            user="avnadmin",       # din postgres-bruger
            password=os.environ.get("DB_PASSWORD", "LOCAL_DEV_ONLY")   # <-- SKIFT DEN HER
    )


# ---------- Database helper-funktioner ----------

def init_db():
    """Opret tabel i PostgreSQL, hvis den ikke findes."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            id SERIAL PRIMARY KEY,
            customer_id TEXT,
            wifi_ssid TEXT,
            wifi_password TEXT,
            radiator_setting TEXT,
            payment_info TEXT,
            created_at TIMESTAMP
        )
        """
    )
    conn.commit()
    cur.close()
    conn.close()


def save_registration(customer_id, wifi_ssid, wifi_password,
                      radiator_setting, payment_info):
    """Gem registreringen i PostgreSQL."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO registrations
        (customer_id, wifi_ssid, wifi_password, radiator_setting, payment_info, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (customer_id, wifi_ssid, wifi_password, radiator_setting, payment_info,
         datetime.utcnow())
    )
    conn.commit()
    cur.close()
    conn.close()


def send_to_energinet_stub(customer_id):
    """Stub – her ville I kalde Energinet-API’et."""
    print(f"[Energinet] Ville nu sende data for customer_id={customer_id}")
