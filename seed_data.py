# seed_data.py
import sqlite3
import os

def seed_database(db_path="sakhisetu.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Purana data clear kar rahe hain taaki duplicates na rahein
    cursor.execute("DELETE FROM documents")
    cursor.execute("DELETE FROM criteria")
    cursor.execute("DELETE FROM schemes")

    # 5 Verified Government Schemes Data (Updated URLs)
    schemes = [
        {
            "id": "pmmy",
            "name": "Pradhan Mantri Mudra Yojana (PMMY)",
            "department": "Ministry of Finance",
            "state_coverage": "ALL",
            "funding_purpose": "working_capital",
            "official_url": "https://www.mudra.org.in/",
            "application_method": "online",
            "next_steps": "Apply via JanSamarth portal or directly visit any commercial bank branch with business proof.",
            "source_url": "https://www.mudra.org.in/",
            "last_verified": "2026-10-10",
            "criteria": [
                {"criterion_key": "business_stage", "expected_value": "any", "description": "Applicable for new or existing micro enterprises"},
                {"criterion_key": "is_woman_entrepreneur", "expected_value": "any", "description": "Open to all, women given preference"},
                {"criterion_key": "registration_status", "expected_value": "any", "description": "Registered or non-registered micro enterprises"}
            ],
            "documents": [
                {"document_code": "aadhaar", "document_name": "Aadhaar Card"},
                {"document_code": "pan", "document_name": "PAN Card"},
                {"document_code": "bank_statement", "document_name": "Last 6 months Bank Statement"}
            ]
        },
        {
            "id": "standup_india",
            "name": "Stand-Up India Scheme",
            "department": "Ministry of Finance",
            "state_coverage": "ALL",
            "funding_purpose": "setup",
            "official_url": "https://www.standupmitra.in/",
            "application_method": "online",
            "next_steps": "Register on Stand-Up Mitra portal, submit detailed project report and greenfield business setup proof.",
            "source_url": "https://www.standupmitra.in/",
            "last_verified": "2026-10-10",
            "criteria": [
                {"criterion_key": "is_woman_entrepreneur", "expected_value": "true", "description": "Must be a woman or SC/ST entrepreneur holding at least 51% stake"},
                {"criterion_key": "business_stage", "expected_value": "new", "description": "Greenfield / new enterprise setup only"},
                {"criterion_key": "business_type", "expected_value": "manufacturing, services, trading", "description": "Manufacturing, service, or trading sector"}
            ],
            "documents": [
                {"document_code": "aadhaar", "document_name": "Aadhaar Card"},
                {"document_code": "pan", "document_name": "PAN Card"},
                {"document_code": "project_report", "document_name": "Detailed Project Report (DPR)"},
                {"document_code": "caste_or_gender_proof", "document_name": "Gender/Category Certificate"}
            ]
        },
        {
            "id": "pmegp",
            "name": "Prime Minister Employment Generation Programme (PMEGP)",
            "department": "KVIC / Ministry of MSME",
            "state_coverage": "ALL",
            "funding_purpose": "setup",
            "official_url": "https://www.myscheme.gov.in/schemes/pmegp",  # Yahan naya link daal diya
            "application_method": "online",
            "next_steps": "Apply on MyScheme or KVIC portal with project profile.",
            "source_url": "https://www.myscheme.gov.in/",
            "last_verified": "2026-10-10",
            "criteria": [
                {"criterion_key": "business_stage", "expected_value": "new", "description": "Only new projects eligible"},
                {"criterion_key": "registration_status", "expected_value": "udyam_registered", "description": "Udyam registration required after project sanction"}
            ],
            "documents": [
                {"document_code": "aadhaar", "document_name": "Aadhaar Card"},
                {"document_code": "pan", "document_name": "PAN Card"},
                {"document_code": "project_report", "document_name": "Project Report"},
                {"document_code": "education_proof", "document_name": "Class 8th Pass Marksheet (if project > 10 Lakhs)"}
            ]
         } ,
        {
            "id": "tread",
            "name": "Trade Related Entrepreneurship Assistance and Development (TREAD)",
            "department": "Ministry of MSME",
            "state_coverage": "ALL",
            "funding_purpose": "capacity_building",
            "official_url": "https://msme.gov.in/",
            "application_method": "offline",
            "next_steps": "Contact registered NGOs / Micro Finance Institutions handling TREAD sanctions.",
            "source_url": "https://msme.gov.in/",
            "last_verified": "2026-10-10",
            "criteria": [
                {"criterion_key": "is_woman_entrepreneur", "expected_value": "true", "description": "Exclusively for women entrepreneurs operating via NGOs"}
            ],
            "documents": [
                {"document_code": "aadhaar", "document_name": "Aadhaar Card"},
                {"document_code": "ngo_membership", "document_name": "NGO / SHG Association Proof"},
                {"document_code": "bank_statement", "document_name": "Bank Statement"}
            ]
        },
        {
            "id": "mahila_samriddhi",
            "name": "Mahila Samriddhi Yojana",
            "department": "National Scheduled Castes Finance & Development Corporation",
            "state_coverage": "ALL",
            "funding_purpose": "micro finance",
            "official_url": "https://nsfdc.nic.in/",
            "application_method": "offline",
            "next_steps": "Submit proposal via State Channelizing Agencies (SCAs).",
            "source_url": "https://nsfdc.nic.in/",
            "last_verified": "2026-10-10",
            "criteria": [
                {"criterion_key": "is_woman_entrepreneur", "expected_value": "true", "description": "Exclusively for women entrepreneurs"},
                {"criterion_key": "business_type", "expected_value": "micro", "description": "Targeted at micro-level tiny business activities"}
            ],
            "documents": [
                {"document_code": "aadhaar", "document_name": "Aadhaar Card"},
                {"document_code": "caste_certificate", "document_name": "Caste Certificate (if applicable)"},
                {"document_code": "income_certificate", "document_name": "Income Certificate"}
            ]
        }
    ]

    for s in schemes:
        cursor.execute("""
            INSERT INTO schemes (id, name, department, state_coverage, funding_purpose, official_url, application_method, next_steps, source_url, last_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (s["id"], s["name"], s["department"], s["state_coverage"], s["funding_purpose"], s["official_url"], s["application_method"], s["next_steps"], s["source_url"], s["last_verified"]))

        for c in s["criteria"]:
            cursor.execute("""
                INSERT INTO criteria (scheme_id, criterion_key, expected_value, description)
                VALUES (?, ?, ?, ?)
            """, (s["id"], c["criterion_key"], c["expected_value"], c["description"]))

        for d in s["documents"]:
            cursor.execute("""
                INSERT INTO documents (scheme_id, document_code, document_name)
                VALUES (?, ?, ?)
            """, (s["id"], d["document_code"], d["document_name"]))

    conn.commit()
    conn.close()
    print("Database updated successfully with working links!")

if __name__ == "__main__":
    seed_database()