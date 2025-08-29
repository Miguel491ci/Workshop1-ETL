from db import init_db
from etl import extract, transform, load

def main():
    # Paso 1: Inicializar BD y tablas
    init_db()

    # Paso 2: Extract
    df = extract()

    # Paso 3: Transform
    df, dim_candidate, dim_country, dim_date, dim_seniority, dim_technology = transform(df)

    # Paso 4: Load
    load(df, dim_candidate, dim_country, dim_date, dim_seniority, dim_technology)

if __name__ == "__main__":
    main()
