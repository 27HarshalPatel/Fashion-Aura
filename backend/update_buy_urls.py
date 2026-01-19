"""
Script to update buy_url with DIRECT brand website URLs
Redirects to official brand sites, not Google Shopping
"""

import sqlite3
import os
import csv
import re
from urllib.parse import quote_plus

CATALOG_DB_PATH = os.getenv("CATALOG_DB_PATH", "catalog.db")

def extract_brand_from_title(title):
    """Extract brand name from product title"""
    title_lower = title.lower()
    
    # Brand mapping with domain and category info
    brands = {
        # Major brands
        'hollister': {'domain': 'www.hollisterco.com', 'region': 'us'},
        'abercrombie': {'domain': 'www.abercrombie.com', 'region': 'us'},
        'gap': {'domain': 'www.gap.com', 'region': 'us'},
        'old navy': {'domain': 'oldnavy.gap.com', 'region': 'us'},
        'banana republic': {'domain': 'bananarepublic.gap.com', 'region': 'us'},
        'h&m': {'domain': 'www2.hm.com', 'region': 'en_us'},
        'uniqlo': {'domain': 'www.uniqlo.com', 'region': 'us/en'},
        'zara': {'domain': 'www.zara.com', 'region': 'us/en'},
        
        # Fast fashion
        'forever 21': {'domain': 'www.forever21.com', 'region': 'us'},
        'forever21': {'domain': 'www.forever21.com', 'region': 'us'},
        'h and m': {'domain': 'www2.hm.com', 'region': 'en_us'},
        
        # American brands
        'american eagle': {'domain': 'www.ae.com', 'region': 'us/en'},
        'aerie': {'domain': 'www.ae.com', 'region': 'us/en'},
        'aeropostale': {'domain': 'www.aeropostale.com', 'region': ''},
        
        # Premium brands
        'tommy hilfiger': {'domain': 'usa.tommy.com', 'region': 'en'},
        'calvin klein': {'domain': 'www.calvinklein.us', 'region': 'en'},
        'ralph lauren': {'domain': 'www.ralphlauren.com', 'region': ''},
        'polo ralph lauren': {'domain': 'www.ralphlauren.com', 'region': ''},
        
        # Denim brands
        'levi': {'domain': 'www.levi.com', 'region': 'US/en_US'},
        "levi's": {'domain': 'www.levi.com', 'region': 'US/en_US'},
        'wrangler': {'domain': 'www.wrangler.com', 'region': 'en-us'},
        'lee': {'domain': 'www.lee.com', 'region': 'us'},
        
        # Sportswear
        'nike': {'domain': 'www.nike.com', 'region': ''},
        'adidas': {'domain': 'www.adidas.com', 'region': 'us'},
        'puma': {'domain': 'us.puma.com', 'region': 'en'},
        'under armour': {'domain': 'www.underarmour.com', 'region': 'en-us'},
        'reebok': {'domain': 'www.reebok.com', 'region': 'us'},
        
        # Specialty
        'j.crew': {'domain': 'www.jcrew.com', 'region': ''},
        'jcrew': {'domain': 'www.jcrew.com', 'region': ''},
        'madewell': {'domain': 'www.madewell.com', 'region': ''},
        'urban outfitters': {'domain': 'www.urbanoutfitters.com', 'region': ''},
        'target': {'domain': 'www.target.com', 'region': ''},
        'walmart': {'domain': 'www.walmart.com', 'region': ''},
    }
    
    for brand, info in brands.items():
        if brand in title_lower:
            return brand, info['domain'], info['region']
    
    return None, None, None

def generate_brand_url(title, brand, domain, region):
    """Generate direct brand website URL based on brand and product"""
    
    # Clean the title - remove brand name
    search_term = title
    for brand_variant in [brand, brand.title(), brand.upper()]:
        search_term = search_term.replace(brand_variant, '')
    
    # Clean up search term
    search_term = re.sub(r'[^\w\s-]', '', search_term)
    search_term = search_term.strip()
    search_query = quote_plus(search_term)
    
    # Brand-specific URL patterns for DIRECT SITE (not Google)
    
    # === GAP BRANDS ===
    if 'gap.com' in domain:
        return f"https://{domain}/browse/search.do?searchText={search_query}"
    
    # === HOLLISTER & ABERCROMBIE ===
    elif 'hollisterco.com' in domain or 'abercrombie.com' in domain:
        return f"https://{domain}/shop/{region}/search?searchTerm={search_query}"
    
    # === H&M ===
    elif 'hm.com' in domain:
        return f"https://{domain}/{region}/search-results.html?q={search_query}"
    
    # === UNIQLO ===
    elif 'uniqlo.com' in domain:
        return f"https://{domain}/{region}/search?q={search_query}"
    
    # === ZARA ===
    elif 'zara.com' in domain:
        return f"https://{domain}/{region}/search?searchTerm={search_query}"
    
    # === FOREVER 21 ===
    elif 'forever21.com' in domain:
        return f"https://{domain}/{region}/search/?q={search_query}"
    
    # === AMERICAN EAGLE ===
    elif 'ae.com' in domain:
        return f"https://{domain}/{region}/search?q={search_query}"
    
    # === TOMMY HILFIGER ===
    elif 'tommy.com' in domain:
        return f"https://{domain}/{region}/search?q={search_query}"
    
    # === CALVIN KLEIN ===
    elif 'calvinklein.us' in domain:
        return f"https://{domain}/{region}/search?q={search_query}"
    
    # === RALPH LAUREN ===
    elif 'ralphlauren.com' in domain:
        return f"https://{domain}/search?q={search_query}"
    
    # === LEVI'S ===
    elif 'levi.com' in domain:
        return f"https://{domain}/{region}/search?q={search_query}"
    
    # === NIKE ===
    elif 'nike.com' in domain:
        return f"https://{domain}/w?q={search_query}"
    
    # === ADIDAS ===
    elif 'adidas.com' in domain:
        return f"https://{domain}/{region}/search?q={search_query}"
    
    # === PUMA ===
    elif 'puma.com' in domain:
        return f"https://{domain}/{region}/search/?q={search_query}"
    
    # === UNDER ARMOUR ===
    elif 'underarmour.com' in domain:
        return f"https://{domain}/{region}/s?q={search_query}"
    
    # === J.CREW ===
    elif 'jcrew.com' in domain:
        return f"https://{domain}/search2?q={search_query}"
    
    # === URBAN OUTFITTERS ===
    elif 'urbanoutfitters.com' in domain:
        return f"https://{domain}/search?q={search_query}"
    
    # === TARGET ===
    elif 'target.com' in domain:
        return f"https://{domain}/s?searchTerm={search_query}"
    
    # === WALMART ===
    elif 'walmart.com' in domain:
        return f"https://{domain}/search?q={search_query}"
    
    # === GENERIC FALLBACK ===
    else:
        # Try common patterns
        if region:
            return f"https://{domain}/{region}/search?q={search_query}"
        else:
            return f"https://{domain}/search?q={search_query}"

def generate_real_brand_urls():
    """Generate DIRECT brand website URLs (not Google Shopping)"""
    
    conn = sqlite3.connect(CATALOG_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, category FROM products")
    products = cursor.fetchall()
    
    updated_count = 0
    brand_count = {}
    unknown_products = []
    
    print("\n🔄 Generating direct brand website URLs...\n")
    
    for idx, (product_id, title, category) in enumerate(products, 1):
        brand, domain, region = extract_brand_from_title(title)
        
        if brand and domain:
            # Generate direct brand URL
            buy_url = generate_brand_url(title, brand, domain, region)
            
            # Track brands
            brand_count[brand] = brand_count.get(brand, 0) + 1
            
            # Use index for display, not product_id
            print(f"✓ [{idx:3d}] {title[:50]:50s} → {domain}")
        else:
            # If we can't detect brand, create a generic search URL based on category
            if category and category.lower() in ['men', 'women']:
                # Use a general fashion retailer as fallback
                search_query = quote_plus(title)
                buy_url = f"https://www.amazon.com/s?k={search_query}"
                print(f"⚠ [{idx:3d}] {title[:50]:50s} → Amazon (fallback)")
            else:
                search_query = quote_plus(title)
                buy_url = f"https://www.google.com/search?tbm=shop&q={search_query}"
                print(f"❌ [{idx:3d}] {title[:50]:50s} → Google Shopping (no brand)")
            
            unknown_products.append((product_id, title))
        
        cursor.execute(
            "UPDATE products SET buy_url = ? WHERE id = ?",
            (buy_url, product_id)
        )
        updated_count += 1
    
    conn.commit()
    conn.close()
    
    # Summary
    print("\n" + "="*80)
    print(f"✅ Updated {updated_count} products with direct brand URLs")
    print("="*80)
    
    print("\n📊 Brands Detected:")
    for brand, count in sorted(brand_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {brand.title():20s} : {count:3d} products")
    
    if unknown_products:
        print(f"\n⚠️  {len(unknown_products)} products without brand detection:")
        for pid, ptitle in unknown_products[:10]:
            print(f"  • {ptitle[:70]}")
        if len(unknown_products) > 10:
            print(f"  ... and {len(unknown_products) - 10} more")
        print("\n💡 Tip: Edit these product titles to include brand names")

def update_buy_urls_from_csv(csv_path):
    """Update buy URLs from a CSV file"""
    
    conn = sqlite3.connect(CATALOG_DB_PATH)
    cursor = conn.cursor()
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            product_id = row['id']
            buy_url = row.get('new_buy_url') or row.get('buy_url')
            
            if buy_url and buy_url.strip():
                cursor.execute(
                    "UPDATE products SET buy_url = ? WHERE id = ?",
                    (buy_url, product_id)
                )
                count += 1
    
    conn.commit()
    conn.close()
    print(f"✅ Updated {count} product URLs from CSV")

def show_current_urls(limit=10):
    """Display current buy URLs"""
    
    conn = sqlite3.connect(CATALOG_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT id, title, buy_url FROM products LIMIT {limit}")
    
    print("\n📋 Sample Product URLs:")
    print("="*80)
    for idx, row in enumerate(cursor.fetchall(), 1):
        print(f"\n[{idx:3d}] {row[1][:60]}")
        print(f"      → {row[2]}")
    print("="*80)
    
    conn.close()

def export_products_to_csv():
    """Export products to CSV for manual URL addition"""
    
    conn = sqlite3.connect(CATALOG_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, category, buy_url FROM products")
    products = cursor.fetchall()
    
    output_file = "products_for_url_update.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'category', 'current_buy_url', 'new_buy_url'])
        
        for product in products:
            writer.writerow([product[0], product[1], product[2], product[3], ''])
    
    conn.close()
    print(f"✅ Exported {len(products)} products to {output_file}")
    print(f"📝 Edit the 'new_buy_url' column and re-import with option 2")

def test_url_patterns():
    """Test URL generation with sample products"""
    
    test_products = [
        "Hollister Baggy Plaid Short-Sleeve Shirt",
        "Gap Men's Boxy Fit Flannel Shirt",
        "Uniqlo Men's Regular Fit Checked Shirt",
        "H&M Men's Regular Fit Shirt",
        "Old Navy Men's Classic Fit Everyday Shirt",
        "Zara Men's Regular Fit Checked Shirt",
        "Nike Sportswear Club T-Shirt",
        "Adidas Essentials Single Jersey T-Shirt",
        "Generic Plaid Shirt",
    ]
    
    print("\n🧪 Testing URL Generation:")
    print("="*80)
    
    for title in test_products:
        brand, domain, region = extract_brand_from_title(title)
        if brand and domain:
            url = generate_brand_url(title, brand, domain, region)
            print(f"\n✓ {title[:50]}")
            print(f"  Brand: {brand.title()}")
            print(f"  URL: {url}")
        else:
            print(f"\n❌ {title[:50]}")
            print(f"  Brand: Not detected")
    
    print("="*80)

if __name__ == "__main__":
    print("🔗 Direct Brand URL Generator")
    print("="*80)
    print("This tool generates URLs that go DIRECTLY to brand websites")
    print("(Not Google Shopping)")
    print("="*80)
    print("\nChoose an option:")
    print("1. Generate direct brand URLs (RECOMMENDED)")
    print("2. Update from CSV file")
    print("3. Export products to CSV for editing")
    print("4. Test URL patterns")
    print("5. Show current URLs")
    print("="*80)
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting URL generation...")
        generate_real_brand_urls()
        print("\n")
        show_current_urls(5)
    elif choice == "2":
        csv_path = input("Enter CSV file path: ").strip()
        if os.path.exists(csv_path):
            update_buy_urls_from_csv(csv_path)
        else:
            print(f"❌ File not found: {csv_path}")
    elif choice == "3":
        export_products_to_csv()
    elif choice == "4":
        test_url_patterns()
    elif choice == "5":
        limit = input("How many products to show? (default 10): ").strip()
        show_current_urls(int(limit) if limit else 10)
    else:
        print("❌ Invalid choice")