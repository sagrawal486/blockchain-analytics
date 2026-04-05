from database import SessionLocal
from etl_service import fetch_and_save_transactions, get_wallet_summary

TEST_WALLET = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

db = SessionLocal()

# Fetch and save
fetch_and_save_transactions(TEST_WALLET, db)

# Get summary from DB
summary = get_wallet_summary(TEST_WALLET, db)
print("\n📊 Wallet Summary from Database:")
for key, val in summary.items():
    print(f"   {key}: {val}")

db.close()