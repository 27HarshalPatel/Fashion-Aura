"""
Database Migration Script: Add Pricing and Buy URL columns
Run this script to add e-commerce features to your catalog database
"""

import sqlite3
import os
import random

CATALOG_DB_PATH = os.getenv("CATALOG_DB_PATH", "catalog.db")

def migrate_database():
    """Add price, original_price, and buy_url columns to products table"""
    
    if not os.path.exists(CATALOG_DB_PATH):
        print(f"❌ Database not found at {CATALOG_DB_PATH}")
        return
    
    conn = sqlite3.connect(CATALOG_DB_PATH)
    cursor = conn.cursor()
    
    # Check existing columns
    cursor.execute("PRAGMA table_info(products)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    print(f"📋 Existing columns: {existing_columns}")
    
    # Add price column if it doesn't exist
    if 'price' not in existing_columns:
        print("➕ Adding 'price' column...")
        cursor.execute("ALTER TABLE products ADD COLUMN price REAL")
        conn.commit()
        print("✅ Added 'price' column")
    
    # Add original_price column if it doesn't exist
    if 'original_price' not in existing_columns:
        print("➕ Adding 'original_price' column...")
        cursor.execute("ALTER TABLE products ADD COLUMN original_price REAL")
        conn.commit()
        print("✅ Added 'original_price' column")
    
    # Add buy_url column if it doesn't exist
    if 'buy_url' not in existing_columns:
        print("➕ Adding 'buy_url' column...")
        cursor.execute("ALTER TABLE products ADD COLUMN buy_url TEXT")
        conn.commit()
        print("✅ Added 'buy_url' column")
    
    # Generate sample pricing for existing products
    print("\n💰 Generating sample pricing data...")
    cursor.execute("SELECT id, title FROM products WHERE price IS NULL")
    products = cursor.fetchall()
    
    for product_id, title in products:
        # Generate realistic pricing
        base_price = random.uniform(15.0, 80.0)
        discount_percent = random.choice([0, 20, 30, 40, 50, 60, 70])
        
        if discount_percent > 0:
            original_price = base_price
            price = round(base_price * (1 - discount_percent / 100), 2)
        else:
            price = round(base_price, 2)
            original_price = None
        
        # Generate a sample buy URL (you'll need to update these with real URLs)
        # Format: use the product title to create a URL-friendly slug
        slug = title.lower().replace(' ', '-').replace("'", '')[:50]
        buy_url = f"https://example.com/product/{slug}"
        
        cursor.execute("""
            UPDATE products 
            SET price = ?, original_price = ?, buy_url = ?
            WHERE id = ?
        """, (price, original_price, buy_url, product_id))
    
    conn.commit()
    print(f"✅ Updated {len(products)} products with pricing data")
    
    # Show sample results
    cursor.execute("SELECT id, title, price, original_price FROM products LIMIT 5")
    print("\n📊 Sample products with pricing:")
    for row in cursor.fetchall():
        discount = ""
        if row[3]:  # original_price exists
            discount_pct = int(((row[3] - row[2]) / row[3]) * 100)
            discount = f" ({discount_pct}% OFF)"
        print(f"  • {row[1]}: ${row[2]}{discount}")
    
    conn.close()
    print("\n✅ Migration completed successfully!")
    print("\n⚠️  Note: Buy URLs are set to example.com - update them with real product URLs")

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    print(f"📍 Database: {CATALOG_DB_PATH}\n")
    migrate_database()