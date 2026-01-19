import os
import io
import sqlite3
import logging
from typing import Optional, List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from PIL import Image
import google.genai as genai

# ------------------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("virtual-tryon-backend")

# ------------------------------------------------------------------------------
# Environment
# ------------------------------------------------------------------------------
CATALOG_DB_PATH = os.getenv("CATALOG_DB_PATH", "/app/catalog.db")
CATALOG_IMAGES_DIR = os.getenv("CATALOG_IMAGES_DIR", "/app/archive/images")
MODEL_NAME = os.getenv("NANOBANANA_MODEL", "gemini-2.0-flash-image")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    logger.warning("⚠️ GOOGLE_API_KEY not set. Virtual try-on will not work.")

# ------------------------------------------------------------------------------
# Gemini Client
# ------------------------------------------------------------------------------
genai_client: Optional[genai.Client] = None

if GOOGLE_API_KEY:
    genai_client = genai.Client(api_key=GOOGLE_API_KEY)
    logger.info("✅ Gemini client initialized")

# ------------------------------------------------------------------------------
# FastAPI App
# ------------------------------------------------------------------------------
app = FastAPI(title="Virtual Try-On Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Static Images
# ------------------------------------------------------------------------------
if os.path.isdir(CATALOG_IMAGES_DIR):
    app.mount(
        "/catalog-images",
        StaticFiles(directory=CATALOG_IMAGES_DIR),
        name="catalog-images",
    )
    logger.info(f"📦 Serving catalog images from {CATALOG_IMAGES_DIR}")
else:
    logger.warning("⚠️ Catalog images directory not found")

# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------
def get_db():
    if not os.path.exists(CATALOG_DB_PATH):
        raise RuntimeError("catalog.db not found")
    return sqlite3.connect(CATALOG_DB_PATH)

# ------------------------------------------------------------------------------
# Health
# ------------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ------------------------------------------------------------------------------
# Products API (Enhanced with pricing and buy links)
# ------------------------------------------------------------------------------
@app.get("/products")
def get_products(
    gender: Optional[str] = Query(None, description="Men or Women"),
    limit: int = Query(12, ge=1, le=50),
    offset: int = Query(0, ge=0),
):
    conn = get_db()
    cursor = conn.cursor()

    # Check if price columns exist in the database
    cursor.execute("PRAGMA table_info(products)")
    columns = [col[1] for col in cursor.fetchall()]
    has_price = 'price' in columns
    has_original_price = 'original_price' in columns
    has_buy_url = 'buy_url' in columns

    # Build query based on available columns
    select_cols = "id, title, category, image"
    if has_price:
        select_cols += ", price"
    if has_original_price:
        select_cols += ", original_price"
    if has_buy_url:
        select_cols += ", buy_url"

    query = f"""
        SELECT {select_cols}
        FROM products
    """
    params: List = []

    if gender:
        query += " WHERE LOWER(category) = LOWER(?)"
        params.append(gender)

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    products = []
    for r in rows:
        product = {
            "id": r[0],
            "title": r[1],
            "category": r[2],
            "image_url": f"/catalog-images/{r[3]}",
        }
        
        # Add price fields if they exist
        col_idx = 4
        if has_price and len(r) > col_idx:
            product["price"] = r[col_idx]
            col_idx += 1
        
        if has_original_price and len(r) > col_idx:
            product["original_price"] = r[col_idx]
            # Calculate discount percentage
            if product.get("price") and r[col_idx]:
                try:
                    discount = int(((float(r[col_idx]) - float(product["price"])) / float(r[col_idx])) * 100)
                    product["discount"] = discount
                except:
                    pass
            col_idx += 1
        
        if has_buy_url and len(r) > col_idx:
            product["buy_url"] = r[col_idx]
        
        products.append(product)

    logger.info(f"Returning {len(products)} products for gender={gender}")

    return {
        "items": products,
        "limit": limit,
        "offset": offset,
        "count": len(products),
    }

# ------------------------------------------------------------------------------
# Virtual Try-On (ENHANCED FOR CATALOG-STYLE IMAGES)
# ------------------------------------------------------------------------------
@app.post("/virtual-try-on")
async def virtual_try_on(
    user_image: UploadFile = File(...),
    garment_image_url: Optional[str] = Form(None),
    garment_image: Optional[UploadFile] = File(None),
    garment_type: str = Form(...),
):
    if not genai_client:
        raise HTTPException(status_code=500, detail="Gemini not configured")

    try:
        # Load user image
        user_bytes = await user_image.read()
        user_pil = Image.open(io.BytesIO(user_bytes)).convert("RGB")

        # Load garment - prioritize uploaded, fallback to catalog
        if garment_image:
            # User uploaded their own garment
            garment_bytes = await garment_image.read()
            garment_pil = Image.open(io.BytesIO(garment_bytes)).convert("RGB")
            logger.info(f"Using custom uploaded garment for {garment_type}")
        elif garment_image_url:
            # Use catalog garment
            garment_path = garment_image_url.replace("/catalog-images/", "")
            garment_full_path = os.path.join(CATALOG_IMAGES_DIR, garment_path)

            if not os.path.exists(garment_full_path):
                raise HTTPException(status_code=404, detail="Garment image not found")

            garment_pil = Image.open(garment_full_path).convert("RGB")
            logger.info(f"Using catalog garment: {garment_path} for {garment_type}")
        else:
            raise HTTPException(
                status_code=400, 
                detail="Must provide either garment_image or garment_image_url"
            )

        # Enhanced prompt that handles both catalog images and standalone garments
        prompt = f"""You are an expert virtual try-on AI system. Perform a photorealistic virtual clothing try-on.

TASK: Replace the {garment_type} on the person in Image 1 with the {garment_type} from Image 2.

IMAGE 1 (Person): The target person who will wear the new garment
IMAGE 2 (Garment): The clothing item to apply - this may show:
  - A model wearing the garment (extract the {garment_type} only)
  - A standalone {garment_type} on plain background
  - A product photo of the {garment_type}

CRITICAL INSTRUCTIONS:

1. GARMENT EXTRACTION:
   - Identify and extract ONLY the {garment_type} from Image 2
   - If Image 2 shows a person wearing it, focus only on the {garment_type} itself
   - Ignore any other clothing items, accessories, or background in Image 2
   - Preserve the exact color, pattern, texture, and style of the {garment_type}

2. GARMENT APPLICATION:
   - Locate the current {garment_type} on the person in Image 1
   - Replace it completely with the {garment_type} from Image 2
   - Ensure perfect fit and alignment with the person's body shape and pose
   - Add natural wrinkles, folds, and draping based on body position
   - Match the lighting, shadows, and highlights to Image 1's environment

3. PRESERVE IN IMAGE 1:
   - Face, hair, and all facial features
   - Body proportions and pose
   - All other clothing items (pants, shoes, accessories) if only replacing {garment_type}
   - Background and environment
   - Original lighting conditions and color temperature
   - Skin tone and texture

4. PHOTOREALISM:
   - The result must look like a real photograph
   - Natural fabric physics (gravity, draping, movement)
   - Proper occlusion and layering
   - Realistic shadows and highlights
   - No visible seams or artifacts

OUTPUT: A single photorealistic image showing the person from Image 1 wearing the {garment_type} from Image 2.
"""

        logger.info(f"Sending request to Gemini for {garment_type} try-on")
        logger.info(f"User image size: {user_pil.size}, Garment image size: {garment_pil.size}")
        
        response = genai_client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt, user_pil, garment_pil],
        )

        # Enhanced error handling
        if not response:
            raise RuntimeError("No response from Gemini API")
        
        if not response.candidates:
            raise RuntimeError("No candidates in Gemini response")
        
        candidate = response.candidates[0]
        
        if not candidate.content or not candidate.content.parts:
            raise RuntimeError("No content parts in Gemini response")
        
        # Find the image part
        image_part = None
        for part in candidate.content.parts:
            if hasattr(part, "inline_data") and part.inline_data is not None:
                image_part = part
                break
        
        if not image_part:
            # Check if there's text response instead
            text_parts = [p.text for p in candidate.content.parts if hasattr(p, "text")]
            if text_parts:
                logger.error(f"Model returned text instead of image: {text_parts[0][:200]}")
                raise RuntimeError(f"Model returned text instead of image. It may need different input images or the try-on failed.")
            
            logger.error(f"No image data in response. Response: {response}")
            raise RuntimeError("Gemini did not return an image. The model may have failed to generate the try-on.")
        
        if not image_part.inline_data.data:
            raise RuntimeError("Image data is empty")

        # Convert to PIL Image
        out_image = Image.open(io.BytesIO(image_part.inline_data.data))
        
        logger.info(f"✅ Successfully generated try-on image: {out_image.size}")

        # Return as PNG
        buf = io.BytesIO()
        out_image.save(buf, format="PNG")
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        logger.exception("❌ Virtual try-on failed")
        raise HTTPException(status_code=500, detail=str(e))