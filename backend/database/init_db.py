import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("../backend/.env")

def init_database():
    #Docker
    # conn = psycopg2.connect(
    #     host="localhost",
    #     port=5433,
    #     database="blockchain_db",
    #     user="postgres",
    #     password="password"
    # )
    #Railway
    conn = psycopg2.connect(
        host="postgres.railway.internal",
        port=5432,
        database="railway",
        user="postgres",
        password="KOIoMjMhagyMMWJCsulfUAzRGmXiPbNP"
    )
    cursor = conn.cursor()
    
    # Read and execute schema file
    with open("schema.sql", "r") as f:
        schema = f.read()
    
    cursor.execute(schema)
    conn.commit()
    
    print("✅ Database tables created successfully!")
    print("\nTables created:")
    
    # Verify tables exist
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    
    tables = cursor.fetchall()
    for table in tables:
        print(f"   ✓ {table[0]}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_database()
