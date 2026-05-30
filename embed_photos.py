#!/usr/bin/env python3
"""
Baixa, redimensiona (800px) e converte para base64 data URI
as imagens curadas do Wikimedia Commons.
Salva em src/photos.json para ser carregado pelo build_html.py.

Uso: python3 embed_photos.py [key]
  sem argumento: processa todas
  com argumento: processa só a variedade informada (ex: python3 embed_photos.py tommy)
"""
import json, os, base64, urllib.request, io, sys, time
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "src", "photos.json")

WM_THUMB = "https://upload.wikimedia.org/wikipedia/commons/thumb/{h1}/{h12}/{fname}/{w}px-{fname}"

# Curated list: key -> {whole, cut} with Wikimedia filenames and credits
# Only include images confirmed to be the correct variety + right shot.
# Format: {"file": "Filename.jpg", "thumb_w": 800, "credit": "Author, Licença"}
CURATED = {
    "tommy": {
        "inteira": {
            # Fruit display - Embrapa/CostaPPPR, CC BY-SA 4.0
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/MangaTommyAtkinsDSC4597.jpg/960px-MangaTommyAtkinsDSC4597.jpg",
            "credit": "CostaPPPR / Wikimedia Commons, CC BY-SA 4.0",
        },
        "cortada": {
            # "sliced, ripe Tommy Atkins mango" — Asit K. Ghosh, CC BY-SA 3.0
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Mango_TommyAtkins06_Asit.jpg/960px-Mango_TommyAtkins06_Asit.jpg",
            "credit": "Asit K. Ghosh / Wikimedia Commons, CC BY-SA 3.0",
        },
    },
    "palmer": {
        "inteira": {
            # Display at Fruit & Spice Park festival — Asit K. Ghosh, CC BY-SA 3.0
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Mango_Palmer_Asit_fs8.jpg/960px-Mango_Palmer_Asit_fs8.jpg",
            "credit": "Asit K. Ghosh / Wikimedia Commons, CC BY-SA 3.0",
        },
    },
    "kent": {
        "inteira": {
            # Display at Fruit & Spice Park festival — Asit K. Ghosh, CC BY-SA 3.0
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Mango_Kent_Asit_fs8.jpg/960px-Mango_Kent_Asit_fs8.jpg",
            "credit": "Asit K. Ghosh / Wikimedia Commons, CC BY-SA 3.0",
        },
    },
    "haden": {
        "inteira": {
            # Display at Fruit & Spice Park festival — Asit K. Ghosh, CC BY-SA 3.0
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Mango_Haden_Asit_fs8.jpg/960px-Mango_Haden_Asit_fs8.jpg",
            "credit": "Asit K. Ghosh / Wikimedia Commons, CC BY-SA 3.0",
        },
    },
    "mallika": {
        "inteira": {
            # Market in Mumbai — Raju Kasambe, CC BY-SA 4.0
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Mallika_Mango_Indian_variety_IMG_20230603_113916_%281%29.jpg/960px-Mallika_Mango_Indian_variety_IMG_20230603_113916_%281%29.jpg",
            "credit": "Raju Kasambe / Wikimedia Commons, CC BY-SA 4.0",
        },
    },
    "ataulfo": {
        "inteira": {
            # Ataulfo mango grown in Soconusco, Mexico — Omegatron, CC BY-SA 3.0
            "url": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Ataulfo_mango.jpg",
            "credit": "Omegatron / Wikimedia Commons, CC BY-SA 3.0",
        },
    },
    "osteen": {
        "inteira": {
            # Fruit & Spice Park display — Asit K. Ghosh, CC BY-SA 3.0
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Mango_Osteen_Asit_fs.jpg/960px-Mango_Osteen_Asit_fs.jpg",
            "credit": "Asit K. Ghosh / Wikimedia Commons, CC BY-SA 3.0",
        },
    },
    "vandyke": {
        "inteira": {
            # Fruit & Spice Park display — Asit K. Ghosh, CC BY-SA 3.0
            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Mango_VanDyke_Asit_fs8.jpg/960px-Mango_VanDyke_Asit_fs8.jpg",
            "credit": "Asit K. Ghosh / Wikimedia Commons, CC BY-SA 3.0",
        },
    },
    # Brazilian varieties: no confirmed free photos — leave gaps
    # espada, rosa, uba, bourbon, coquinho, maca, keitt, sensation, itamaraca
}

# Varieties without confirmed photos (for reporting)
GAPS = ["espada", "rosa", "uba", "bourbon", "coquinho", "maca", "keitt", "sensation", "itamaraca"]


def download_and_encode(url, max_side=800, quality=82):
    """Download image, resize to max_side, return JPEG base64 data URI."""
    req = urllib.request.Request(url, headers={"User-Agent": "MangosBrasil/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    print(f"    Download OK: {w}×{h}px, {len(data)//1024} KB")
    if max(w, h) > max_side:
        scale = max_side / max(w, h)
        nw, nh = int(w*scale), int(h*scale)
        img = img.resize((nw, nh), Image.LANCZOS)
        print(f"    Redimensionado: {nw}×{nh}px")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    data_uri = f"data:image/jpeg;base64,{b64}"
    print(f"    Encoded: {len(data_uri)//1024} KB em base64")
    return data_uri


def process_key(key, spec, existing):
    result = existing.get(key, {})
    updated = False

    for kind in ("inteira", "cortada"):
        if kind not in spec:
            continue
        if result.get(kind):
            print(f"  [{kind}] já existe, pulando.")
            continue
        info = spec[kind]
        url = info["url"]
        credit = info["credit"]
        print(f"  [{kind}] Baixando: {url[:80]}...")
        try:
            data_uri = download_and_encode(url)
            result[kind] = data_uri
            result["credito"] = credit  # latest credit wins (merge later if needed)
            updated = True
        except Exception as e:
            print(f"  [{kind}] ERRO: {e}")
        time.sleep(3)

    return result, updated


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None

    # Load existing
    existing = {}
    if os.path.exists(OUT_PATH):
        existing = json.load(open(OUT_PATH, encoding="utf-8"))
        print(f"Carregados {len(existing)} registros existentes de {OUT_PATH}\n")

    keys_to_process = [target] if target else list(CURATED.keys())

    for key in keys_to_process:
        if key not in CURATED:
            print(f"[{key}] não está na lista curada — lacuna registrada.")
            continue
        print(f"\n=== {key} ===")
        result, updated = process_key(key, CURATED[key], existing)
        existing[key] = result
        if updated:
            json.dump(existing, open(OUT_PATH, "w", encoding="utf-8"), ensure_ascii=False)
            print(f"  Salvo em {OUT_PATH}")

    print("\n\n=== LACUNAS (sem foto livre confirmada) ===")
    for k in GAPS:
        print(f"  {k}: mantém ilustração SVG como fallback")

    print("\n=== RESUMO ===")
    for k in list(CURATED.keys()) + GAPS:
        v = existing.get(k, {})
        i = "✓" if v.get("inteira") else "✗"
        c = "✓" if v.get("cortada") else "✗"
        print(f"  {k}: inteira={i}  cortada={c}")
