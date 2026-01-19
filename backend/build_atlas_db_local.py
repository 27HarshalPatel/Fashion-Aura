import os
import sqlite3
import hashlib

# Updated to match backend paths
DB_PATH = "archive/products.db"  # Changed from catalog.db to products.db
IMAGES_DIR = "archive/images"

# Ensure the archive directory exists
os.makedirs("archive", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    image TEXT NOT NULL
)
""")

# wipe old data
cur.execute("DELETE FROM products")

def make_id(text):
    return hashlib.md5(text.encode()).hexdigest()[:16]

inserted_count = 0
for fname in os.listdir(IMAGES_DIR):
    if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        continue

    parts = fname.split("-")
    if len(parts) < 3:
        print(f"⚠️  Skipping {fname} (doesn't match expected format: Category-Title-Info.ext)")
        continue

    category = parts[0]        # Men / Women
    title = " ".join(parts[1:]).replace("_", " ").rsplit(".", 1)[0]

    pid = make_id(fname)

    try:
        cur.execute(
            "INSERT INTO products (id, title, category, image) VALUES (?, ?, ?, ?)",
            (pid, title, category, fname)
        )
        inserted_count += 1
        print(f"✓ Added: {category} - {title}")
    except Exception as e:
        print(f"✗ Error adding {fname}: {e}")

conn.commit()

# Show statistics
cur.execute("SELECT COUNT(*) FROM products")
total = cur.fetchone()[0]

cur.execute("SELECT category, COUNT(*) FROM products GROUP BY category")
categories = cur.fetchall()

print("\n" + "="*50)
print(f"✓ Database rebuilt successfully: {DB_PATH}")
print(f"  Total products: {total}")
print(f"  Inserted: {inserted_count}")
for cat, count in categories:
    print(f"  - {cat}: {count} items")
print("="*50)

conn.close()