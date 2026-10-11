# database.py
import sqlite3
import os

DB_PATH = "sakhisetu.db"

def get_db_connection():
    """Database connection establish karta hai."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Schema file ko read karke database tables banata hai agar wo pehle se nahi hain."""
    if os.path.exists("schema.sql"):
        with open("schema.sql", "r") as f:
            schema = f.read()
        conn = get_db_connection()
        conn.executescript(schema)
        conn.close()

def get_all_schemes():
    """
    Returns all scheme records as Python dictionaries in the agreed format.
    Ye function baaki team members ke sath shared contract hai.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schemes")
    rows = cursor.fetchall()

    schemes = []
    for row in rows:
        scheme_id = row["id"]

        # Is scheme ke liye criteria fetch karna
        cursor.execute("SELECT criterion_key, expected_value, description FROM criteria WHERE scheme_id = ?", (scheme_id,))
        criteria_rows = cursor.fetchall()
        criteria = [
            {
                "key": c["criterion_key"],
                "expected_value": c["expected_value"],
                "description": c["description"]
            }
            for c in criteria_rows
        ]

        # Is scheme ke liye required documents fetch karna
        cursor.execute("SELECT document_code, document_name, is_mandatory FROM documents WHERE scheme_id = ?", (scheme_id,))
        doc_rows = cursor.fetchall()
        documents = [
            {
                "code": d["document_code"],
                "name": d["document_name"],
                "is_mandatory": bool(d["is_mandatory"])
            }
            for d in doc_rows
        ]

        # Agreed common format ke hisaab se dictionary banana
        schemes.append({
            "id": row["id"],
            "name": row["name"],
            "department": row["department"],
            "state_coverage": row["state_coverage"],
            "funding_purpose": row["funding_purpose"],
            "official_url": row["official_url"],
            "application_method": row["application_method"],
            "next_steps": row["next_steps"],
            "source_url": row["source_url"],
            "last_verified": row["last_verified"],
            "criteria": criteria,
            "documents": documents
        })

    conn.close()
    return schemes

def get_scheme_by_id(scheme_id):
    """Kisi ek specific scheme ki details ID ke base par return karta hai."""
    all_schemes = get_all_schemes()
    for scheme in all_schemes:
        if scheme["id"] == scheme_id:
            return scheme
    return None