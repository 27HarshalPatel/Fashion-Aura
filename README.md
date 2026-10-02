# 🎨 Fashion Aura - AI-Powered Virtual Try-On

<div align="center">

![Fashion Aura Banner](https://img.shields.io/badge/Fashion-Aura-6366f1?style=for-the-badge&logo=sparkles&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini%202.0-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**Experience the future of fashion with AI-powered virtual try-on technology**

[Demo Video](#-demo) • [Features](#-features) • [Installation](#-installation) • [Documentation](#-documentation)

</div>

---

## 📺 Demo

<div align="center">
  
  [![Fashion Aura Demo](demo.gif)](Fashion-Aura-Launch-video.mp4)
  
  *One photo, three shirts. Click for the version with sound, or watch the [full walkthrough](demo.mp4).*
  
</div>

---

## 🌟 Overview

**Fashion Aura** is a cutting-edge virtual try-on application that leverages Google's Gemini 2.0 Flash AI model to provide photorealistic clothing visualization. Users can upload their photos and instantly see how different garments would look on them before making a purchase decision.

### Key Highlights

- 🤖 **AI-Powered Try-On**: Utilizes Google Gemini 2.0 Flash for state-of-the-art image generation
- 🛍️ **E-Commerce Integration**: Browse 78,000+ products with direct links to brand websites
- 📸 **Custom Garment Upload**: Try on your own clothing images or choose from the catalog
- 🎯 **Smart Detection**: Automatic garment type detection (shirt, pants, dress, jacket, etc.)
- ⚡ **Real-Time Processing**: 4-8 second try-on generation
- 🌐 **Responsive Design**: Beautiful UI with modern gradient effects and animations
- 🔗 **Brand Integration**: Direct links to 30+ fashion brands (Hollister, Gap, H&M, Uniqlo, Nike, etc.)

---

## ✨ Features

### For Users

- **Virtual Try-On**: Upload a photo and see yourself wearing any garment from the catalog
- **Custom Garments**: Upload your own clothing images to try on
- **Browse Catalog**: Explore thousands of products with prices and discounts
- **Shopping Links**: One-click access to official brand websites
- **Download Results**: Save your try-on images for future reference
- **Gender Filters**: Separate catalogs for Men's and Women's fashion

### For Developers

- **Containerized Deployment**: Docker Compose for easy setup
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Database Management**: SQLite with migration scripts
- **Scalable Architecture**: Modular design for easy extensions
- **Brand URL Generator**: Automated URL creation for 30+ brands

---

## 🏗️ Architecture & Pipeline

### System Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  Frontend (UI)  │ ──────> │  Backend (API)   │ ──────> │  Gemini 2.0 AI  │
│   Nginx:8080    │  HTTP   │  FastAPI:8000    │  gRPC   │   Flash Image   │
│                 │         │                  │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
         │                           │                            │
         │                           ▼                            │
         │                  ┌─────────────────┐                   │
         │                  │   SQLite DB     │                   │
         │                  │  (78K products) │                   │
         │                  └─────────────────┘                   │
         │                           │                            │
         └───────────────────────────┴────────────────────────────┘
                              Shared Volumes
```

### Processing Pipeline

#### 1. **User Upload Phase**
```
User Photo Upload → File Validation → Base64 Encoding → Frontend Preview
                                                              ↓
Custom Garment Upload (Optional) → Garment Type Detection → Ready for Try-On
```

#### 2. **Catalog Selection Phase**
```
Database Query (Gender Filter) → Product Retrieval → Image Serving
        ↓                              ↓                    ↓
   Pagination                    Price Calculation    Brand URL Linking
        ↓                              ↓                    ↓
   Grid Display ← ─────────────────────┴────────────────────┘
```

#### 3. **Virtual Try-On Pipeline**
```
┌──────────────────────────────────────────────────────────────────┐
│                     Try-On Request Initiated                      │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Step 1: Image Preparation                                        │
│  • Load user photo (PIL Image conversion)                         │
│  • Load garment image (catalog or custom upload)                  │
│  • Resize/optimize for API (max dimensions)                       │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Step 2: Garment Type Detection                                   │
│  • Analyze filename (shirt.jpg, pants.jpg, etc.)                  │
│  • Parse product title for keywords                               │
│  • Default to 'shirt' if unknown                                  │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Step 3: Prompt Engineering                                       │
│  • Build context-aware prompt with garment type                   │
│  • Specify preservation requirements (face, pose, background)     │
│  • Define photorealism constraints                                │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Step 4: Gemini AI Processing                                     │
│  • Send images + prompt to Gemini 2.0 Flash                       │
│  • Model extracts garment from reference image                    │
│  • AI applies garment to user's body with:                        │
│    - Pose matching                                                │
│    - Lighting adaptation                                          │
│    - Natural wrinkle/fold generation                              │
│    - Shadow/highlight rendering                                   │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Step 5: Response Processing                                      │
│  • Extract image data from API response                           │
│  • Validate image generation success                              │
│  • Convert to PNG format                                          │
│  • Stream back to client                                          │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│  Step 6: Frontend Display                                         │
│  • Render result image in preview panel                           │
│  • Enable download button                                         │
│  • Show success message with garment type                         │
└──────────────────────────────────────────────────────────────────┘
```

#### 4. **E-Commerce Integration Pipeline**
```
Product Selection → Brand Detection → URL Generation → Redirect to Store
                         ↓                   ↓
                   30+ Brands          Search Query
                   Recognized          Optimization
```

---

## 🚀 Installation

### Prerequisites

- **Docker & Docker Compose** (v20.10+)
- **Google Cloud Account** (for Gemini API access)
- **78K+ Product Dataset** (Fashion images)

### Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fashion-aura.git
cd fashion-aura
```

#### 2. Set Up Google Cloud Credentials

Create `backend/keys.json` with your service account:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "your-cert-url"
}
```

#### 3. Configure Environment Variables

Create `backend/.env`:

```env
GOOGLE_API_KEY=your-gemini-api-key-here
CATALOG_DB_PATH=/app/catalog.db
CATALOG_IMAGES_DIR=/app/archive/images
```

#### 4. Prepare the Database

Place your product catalog:

```bash
# Your structure should look like:
backend/
  ├── archive/
  │   ├── images/          # 78K+ product images
  │   └── products.db      # Source database
  ├── catalog.db           # Will be created
  └── ...
```

Run database migration:

```bash
cd backend
python add_pricing_columns.py
python update_buy_urls.py  # Choose option 1
```

#### 5. Launch with Docker

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### 6. Access the Application

- **Frontend**: http://localhost:8080
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📁 Project Structure

```
Fashion-Aura/
│
├── backend/
│   ├── archive/
│   │   ├── images/              # 78K+ product images
│   │   ├── atlas_data.csv       # Product metadata
│   │   ├── atlas_data.feather   # Optimized data format
│   │   └── products.db          # Source database
│   │
│   ├── __pycache__/             # Python cache
│   ├── venv/                    # Virtual environment
│   │
│   ├── .env                     # Environment variables
│   ├── app.py                   # FastAPI application
│   ├── catalog.db               # Main product database
│   ├── Dockerfile               # Backend container config
│   ├── keys.json                # GCP service account
│   ├── requirements.txt         # Python dependencies
│   │
│   ├── add_pricing_columns.py  # Database migration script
│   ├── build_atlas_db_local.py # Database builder
│   └── update_buy_urls.py       # Brand URL generator
│
├── index.html                   # Frontend UI
├── demo.gif                     # demo video in .gif format
├── Demo.png                     # Sample screenshot of Fashion Aura Result
├── demo.mp4                     # demo video in .mp4 format
├── nginx.conf                   # Nginx configuration
├── docker-compose.yml           # Docker orchestration
└── README.md                    # This file
```

---

## 🔧 Configuration

### Database Schema

```sql
CREATE TABLE products (
    id TEXT PRIMARY KEY,           -- Unique product ID (MD5 hash)
    title TEXT NOT NULL,           -- Product name
    category TEXT NOT NULL,        -- Men/Women
    image TEXT NOT NULL,           -- Image filename
    price REAL,                    -- Current price
    original_price REAL,           -- Original price (for discounts)
    buy_url TEXT                   -- Brand website link
);
```

### Docker Compose Services

| Service | Port | Description |
|---------|------|-------------|
| **backend** | 8000 | FastAPI server with Gemini AI integration |
| **frontend** | 8080 | Nginx serving the web interface |

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Gemini API key | `AIza...` |
| `CATALOG_DB_PATH` | Database file path | `/app/catalog.db` |
| `CATALOG_IMAGES_DIR` | Images directory | `/app/archive/images` |
| `NANOBANANA_MODEL` | AI model name | `gemini-2.0-flash-image` |
| `GCP_PROJECT_ID` | Google Cloud project | `gen-lang-client-...` |

---

## 🛠️ API Documentation

### Endpoints

#### **GET /health**
Health check endpoint

**Response:**
```json
{
  "status": "ok"
}
```

---

#### **GET /products**
Retrieve product catalog with pagination

**Query Parameters:**
- `gender` (optional): "Men" or "Women"
- `limit` (default: 12): Items per page (1-50)
- `offset` (default: 0): Pagination offset

**Response:**
```json
{
  "items": [
    {
      "id": "36d5fc816d37b1c4",
      "title": "Hollister Baggy Plaid Short-Sleeve Shirt",
      "category": "Men",
      "image_url": "/catalog-images/Men-Shirt-12345.jpg",
      "price": 29.99,
      "original_price": 59.99,
      "discount": 50,
      "buy_url": "https://www.hollisterco.com/shop/us/search?searchTerm=baggy+plaid+shirt"
    }
  ],
  "limit": 12,
  "offset": 0,
  "count": 12
}
```

---

#### **POST /virtual-try-on**
Generate virtual try-on image

**Form Data:**
- `user_image` (file): User's photo
- `garment_image` (file, optional): Custom garment image
- `garment_image_url` (string, optional): Catalog garment URL
- `garment_type` (string): "shirt" | "pants" | "dress" | "jacket"

**Response:**
- Content-Type: `image/png`
- Binary image data

**Example Request:**
```bash
curl -X POST http://localhost:8000/virtual-try-on \
  -F "user_image=@user.jpg" \
  -F "garment_image_url=/catalog-images/Men-Shirt-001.jpg" \
  -F "garment_type=shirt"
```

---

## 🎨 Frontend Features

### User Interface Components

1. **Header Section**
   - Logo with gradient effect
   - Tagline and subtitle
   - Legal disclaimer banner

2. **User Photo Panel**
   - Drag & drop upload area
   - Image preview
   - Upload status indicators

3. **Garment Selection Panel**
   - Custom garment upload
   - Gender filters (Men/Women)
   - Product grid with:
     - Product images
     - Titles and prices
     - Discount badges
     - "Buy Now" buttons
   - Infinite scroll pagination

4. **Result Panel**
   - Try-on preview
   - Download button
   - Processing status
   - Detected garment type display

### UI/UX Highlights

- **Gradient Backgrounds**: Animated radial gradients
- **Glassmorphism**: Blur effects on panels
- **Smooth Animations**: Fade-in, slide-in, zoom effects
- **Hover Interactions**: Button highlights, card lifts
- **Responsive Design**: Mobile-friendly grid layout
- **Loading States**: Processing indicators with pulse animations

---

## 📊 Database Management

### Initial Setup

```bash
# Build database from images
python backend/build_atlas_db_local.py

# Add pricing columns
python backend/add_pricing_columns.py

# Generate brand URLs
python backend/update_buy_urls.py
# Choose option 1: Generate direct brand URLs
```

### Supported Brands

Fashion Aura automatically detects and generates URLs for 30+ brands:

| Category | Brands |
|----------|--------|
| **Fast Fashion** | Hollister, Abercrombie, Gap, Old Navy, H&M, Uniqlo, Zara, Forever 21 |
| **Sportswear** | Nike, Adidas, Puma, Under Armour, Reebok |
| **Premium** | Tommy Hilfiger, Calvin Klein, Ralph Lauren, Polo |
| **Denim** | Levi's, Wrangler, Lee |
| **Specialty** | American Eagle, J.Crew, Madewell, Urban Outfitters |
| **Retail** | Target, Walmart |

### Database Maintenance

```bash
# Export products to CSV
python backend/update_buy_urls.py
# Choose option 3

# Update from CSV
python backend/update_buy_urls.py
# Choose option 2, provide CSV path

# View current URLs
python backend/update_buy_urls.py
# Choose option 5
```

---

## 🧪 Testing

### Manual Testing

1. **Upload User Photo**
   - Test with different poses
   - Test with different backgrounds
   - Test with different lighting

2. **Try-On Catalog Item**
   - Select a shirt
   - Select pants
   - Select a dress

3. **Upload Custom Garment**
   - Upload a product photo with model
   - Upload a flat-lay garment image
   - Test filename detection (shirt.jpg, pants.png)

4. **E-Commerce Links**
   - Click "Buy Now" on Hollister product
   - Verify redirect to hollisterco.com
   - Test with multiple brands

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Get products
curl "http://localhost:8000/products?gender=Men&limit=5"

# Test try-on
curl -X POST http://localhost:8000/virtual-try-on \
  -F "user_image=@test_user.jpg" \
  -F "garment_image=@test_shirt.jpg" \
  -F "garment_type=shirt" \
  --output result.png
```

---

## 📝 Usage Guide

### Basic Workflow

1. **Upload Your Photo**
   - Click the upload area in the left panel
   - Select a clear, full-body or upper-body photo
   - Preview appears immediately

2. **Choose a Garment**
   - **Option A**: Browse the catalog
     - Filter by gender (Men/Women)
     - Click on a product image to select
     - See price and discount information
   - **Option B**: Upload your own
     - Click "Upload Garment"
     - Name the file appropriately (shirt.jpg, pants.jpg)
     - Preview appears in the small thumbnail

3. **Generate Try-On**
   - Click "Virtual Try-On" button
   - Wait 4-8 seconds for AI processing
   - View result in the right panel

4. **Save or Shop**
   - Click download icon to save the result
   - Click "Buy Now" to visit the brand's website

---

## 🔐 Legal & Compliance

### Disclaimer

Fashion Aura displays a prominent disclaimer:

> ⚠️ **Disclaimer:** This site is not affiliated with, endorsed by, or sponsored by any of the brands shown. All product images, brand names, and trademarks are the property of their respective owners. We are an independent virtual try-on service. Product links redirect to official brand websites for your convenience.

### Data Privacy

- **User photos**: Processed in-memory, not stored permanently
- **Try-on results**: Temporary, can be downloaded by user
- **No tracking**: No user data collection or analytics
- **External links**: Users redirected to official brand websites

### Terms of Use

- Virtual try-on is for visualization purposes only
- Actual product fit may vary
- No guarantees on product availability or pricing
- All purchases made through third-party retailers

---

## 🚧 Troubleshooting

### Common Issues

#### 1. Backend won't start
```bash
# Check logs
docker-compose logs backend

# Verify API key
cat backend/.env | grep GOOGLE_API_KEY

# Rebuild container
docker-compose up -d --build backend
```

#### 2. Images not loading
```bash
# Check image directory
ls backend/archive/images/ | wc -l

# Verify database mount
docker exec fashion-backend ls /app/archive/images

# Check permissions
chmod -R 755 backend/archive/images
```

#### 3. Try-on fails
```bash
# Check Gemini API quota
# Visit: https://console.cloud.google.com/

# Verify model name
docker exec fashion-backend env | grep NANOBANANA_MODEL

# Test with smaller images
# Reduce image size to < 2MB
```

#### 4. Buy URLs broken
```bash
# Regenerate URLs
python backend/update_buy_urls.py
# Choose option 1

# Check database
sqlite3 backend/catalog.db
SELECT buy_url FROM products LIMIT 5;
```

---

## 🔮 Future Enhancements

### Planned Features

- [ ] **Multi-Garment Try-On**: Try on complete outfits
- [ ] **Wishlist Feature**: Save favorite try-ons
- [ ] **Style Recommendations**: AI-powered outfit suggestions
- [ ] **Affiliate Integration**: Monetization through affiliate programs
- [ ] **Performance Optimization**: Faster try-on generation

### Technical Improvements

- [ ] CDN integration for images
- [ ] Redis caching for API responses
- [ ] PostgreSQL migration for better scalability
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Monitoring with Prometheus/Grafana

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini AI**: For the powerful image generation model
- **FastAPI**: For the excellent web framework
- **Fashion Dataset**: Atlas dataset with 78K+ products
- **Open Source Community**: For the amazing libraries and tools

---

## 📞 Contact & Support

- **Developer**: Harshal Anil Patel
- **Email**: harshal27patel@gmail.com
- **GitHub**: https://github.com/27HarshalPatel
- **Issues**: [Report a bug](https://github.com/27HarshalPatel/fashion-aura/issues)

---

## ⭐ Show Your Support

If you like this project, please give it a ⭐ on GitHub!

---

<div align="center">

**Built with ❤️ using AI and Modern Web Technologies**

Made possible by [Google Gemini](https://deepmind.google/technologies/gemini/) • [FastAPI](https://fastapi.tiangolo.com/) • [Docker](https://www.docker.com/)

</div>
