import os
import pandas as pd
import datetime
from connection import get_connection

# ===========================
# 1) EXTRACT
# ===========================
def extract(filepath="Data/candidates.csv"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filepath)

    # Detectar separador automáticamente (; o ,)
    df = pd.read_csv(file_path, sep=None, engine="python")

    # Normalizar nombres de columnas
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(r"\s+", "_", regex=True)
          .str.replace(r"[^a-z0-9_]+", "", regex=True)
    )

    # Normalizar valores clave
    if "email" in df.columns:
        df["email"] = df["email"].str.strip().str.lower()
    for col in ["country", "seniority", "technology"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.lower()

    # Convertir numéricos
    for col in ["code_challenge_score", "technical_interview_score", "yoe"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")

    # Parsear fecha
    if "application_date" in df.columns:
        df["application_date"] = pd.to_datetime(
            df["application_date"], errors="coerce", dayfirst=True
        )

    return df

# ===========================
# 2) TRANSFORM
# ===========================
def transform(df):
    # Crear HiredFlag
    df["hired_flag"] = ((df["code_challenge_score"] >= 7) &
                        (df["technical_interview_score"] >= 7)).astype(int)

    # DimCandidate
    dim_candidate = (
        df[["first_name", "last_name", "email", "yoe"]]
        .drop_duplicates()
        .rename(columns={"yoe": "exactyoe"})
        .reset_index(drop=True)
    )

    # DimCountry
    dim_country = df[["country"]].drop_duplicates().reset_index(drop=True)

    # DimDate
    dim_date = (
        df[["application_date"]]
        .drop_duplicates()
        .rename(columns={"application_date": "fulldate"})
        .reset_index(drop=True)
    )
    dim_date["year"] = dim_date["fulldate"].dt.year
    dim_date["month"] = dim_date["fulldate"].dt.month
    dim_date["quarter"] = dim_date["fulldate"].dt.quarter

    # DimSeniority
    dim_seniority = df[["seniority"]].drop_duplicates().reset_index(drop=True)

    # DimTechnology
    dim_technology = df[["technology"]].drop_duplicates().reset_index(drop=True)

    return df, dim_candidate, dim_country, dim_date, dim_seniority, dim_technology

# ===========================
# 3) LOAD
# ===========================
def load(df, dim_candidate, dim_country, dim_date, dim_seniority, dim_technology):
    conn = get_connection("hiring_excercise")
    cursor = conn.cursor()

    # ---- Insertar DimCandidate
    for _, row in dim_candidate.iterrows():
        cursor.execute("""
            INSERT INTO DimCandidate (FirstName, LastName, Email, ExactYoe)
            VALUES (%s, %s, %s, %s)
        """, (row["first_name"], row["last_name"], row["email"], int(row["exactyoe"])))

    # ---- Insertar DimCountry
    for _, row in dim_country.iterrows():
        cursor.execute("""
            INSERT INTO DimCountry (CountryName)
            VALUES (%s)
        """, (row["country"],))

    # ---- Insertar DimDate
    for _, row in dim_date.iterrows():
        cursor.execute("""
            INSERT INTO DimDate (FullDate, Year, Month, Quarter)
            VALUES (%s, %s, %s, %s)
        """, (row["fulldate"].date(), int(row["year"]), int(row["month"]), int(row["quarter"])))

    # ---- Insertar DimSeniority
    for _, row in dim_seniority.iterrows():
        cursor.execute("""
            INSERT INTO DimSeniority (SeniorityLevel)
            VALUES (%s)
        """, (row["seniority"],))

    # ---- Insertar DimTechnology
    for _, row in dim_technology.iterrows():
        cursor.execute("""
            INSERT INTO DimTechnology (TechnologyName)
            VALUES (%s)
        """, (row["technology"],))

    conn.commit()

    # ===========================
    # FACT TABLE
    # ===========================
    def get_lookup(table, key_col, id_col):
        cursor.execute(f"SELECT {id_col}, {key_col} FROM {table}")
        rows = cursor.fetchall()
        lookup = {}
        for id_val, key in rows:
            # Para fechas
            if isinstance(key, (pd.Timestamp,)):
                key = key.date()
            elif isinstance(key, (datetime.datetime,)):
                key = key.date()
            elif isinstance(key, datetime.date):
                pass  # ya es date
            else:
                # texto (country, seniority, technology, email)
                key = str(key).strip().lower()
            lookup[key] = id_val
        return lookup


    candidate_lookup = get_lookup("DimCandidate", "Email", "CandidateID")
    country_lookup = get_lookup("DimCountry", "CountryName", "CountryID")
    date_lookup = get_lookup("DimDate", "FullDate", "DateID")
    seniority_lookup = get_lookup("DimSeniority", "SeniorityLevel", "SeniorityID")
    technology_lookup = get_lookup("DimTechnology", "TechnologyName", "TechnologyID")

    for _, row in df.iterrows():
        candidate_id = candidate_lookup.get(row["email"])
        country_id = country_lookup.get(row["country"])
        date_id = date_lookup.get(row["application_date"].date())
        seniority_id = seniority_lookup.get(row["seniority"])
        technology_id = technology_lookup.get(row["technology"])

        if None in [candidate_id, country_id, date_id, seniority_id, technology_id]:
            print("⚠️ Dimensiones no encontradas ->",
            f"Candidate: {candidate_id}, Country: {country_id}, Date: {date_id}, Seniority: {seniority_id}, Tech: {technology_id}")
            print("Registro:", row.to_dict())
            continue

        cursor.execute("""
            INSERT INTO FactHiring (
                CandidateID, CountryID, DateID, SeniorityID, TechnologyID,
                CodeChallengeScore, TechnicalInterviewScore, HiredFlag
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            candidate_id,
            country_id,
            date_id,
            seniority_id,
            technology_id,
            float(row["code_challenge_score"]),
            float(row["technical_interview_score"]),
            int(row["hired_flag"])
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Carga ETL completada en MySQL ✅")
