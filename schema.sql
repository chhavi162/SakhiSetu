-- schema.sql
-- Purane tables ko hata kar naye सिरे se banane ke liye
DROP TABLE IF EXISTS criteria;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS schemes;

-- 1. Main Schemes Table: Isme scheme ka naam, department aur URL rahega
CREATE TABLE schemes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    state_coverage TEXT NOT NULL, 
    funding_purpose TEXT,        
    official_url TEXT,
    application_method TEXT,     
    next_steps TEXT,
    source_url TEXT,
    last_verified TEXT
);

-- 2. Criteria Table: Isme scheme ki shartein (rules) store hongi
CREATE TABLE criteria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_id TEXT,
    criterion_key TEXT NOT NULL, 
    expected_value TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY(scheme_id) REFERENCES schemes(id) ON DELETE CASCADE
);

-- 3. Documents Table: Isme scheme ke liye required documents ki list hogi
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_id TEXT,
    document_code TEXT NOT NULL, 
    document_name TEXT NOT NULL,
    is_mandatory INTEGER DEFAULT 1,
    FOREIGN KEY(scheme_id) REFERENCES schemes(id) ON DELETE CASCADE
);