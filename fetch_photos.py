#!/usr/bin/env python3
"""
Busca imagens de variedades de manga no Wikimedia Commons,
redimensiona para 800px e converte para data URI base64.
"""
import json, os, base64, urllib.request, urllib.parse, io, time
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"

def wiki_search(query, limit=8):
    params = urllib.parse.urlencode({
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "prop": "imageinfo",
        "iiprop": "url|mime|size|extmetadata",
        "gsrlimit": limit,
        "format": "json",
    })
    url = f"{WIKIMEDIA_API}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "MangosBrasil/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def wiki_thumb(filename, width=800):
    """Get thumbnail URL for a Wikimedia file."""
    params = urllib.parse.urlencode({
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url|thumburl|mime|extmetadata",
        "iiurlwidth": width,
        "format": "json",
    })
    url = f"{WIKIMEDIA_API}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "MangosBrasil/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read())
    pages = d.get("query", {}).get("pages", {})
    for pid, p in pages.items():
        ii = p.get("imageinfo", [{}])[0]
        meta = ii.get("extmetadata", {})
        license_short = meta.get("LicenseShortName", {}).get("value", "")
        artist = meta.get("Artist", {}).get("value", "")
        # strip HTML tags from artist
        import re
        artist = re.sub(r'<[^>]+>', '', artist)
        return {
            "thumb": ii.get("thumburl", ""),
            "orig": ii.get("url", ""),
            "mime": ii.get("mime", ""),
            "license": license_short,
            "author": artist.strip(),
        }
    return None

def download_and_encode(url, max_side=800, quality=82):
    """Download image, resize to max_side, return JPEG base64 data URI."""
    req = urllib.request.Request(url, headers={"User-Agent": "MangosBrasil/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    if max(w, h) > max_side:
        scale = max_side / max(w, h)
        img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/jpeg;base64,{b64}"

# ---- Search queries for each variety ----
# Format: key -> (whole_query, cut_query)
SEARCHES = {
    "tommy": (
        "Tommy Atkins mango fruit",
        "Tommy Atkins mango cross section half",
    ),
    "palmer": (
        "Palmer mango fruit",
        "Palmer mango cut half cross section",
    ),
    "espada": (
        "Espada mango Brasil fruit",
        "Espada mango cortada metade",
    ),
    "rosa": (
        "Rosa mango Brazil fruit",
        "Rosa mango cortada",
    ),
    "uba": (
        "Ubá mango Minas Gerais fruit",
        "manga Ubá cortada metade",
    ),
    "kent": (
        "Kent mango fruit",
        "Kent mango cut cross section half",
    ),
    "keitt": (
        "Keitt mango fruit green",
        "Keitt mango cut half",
    ),
    "bourbon": (
        "Bourbon mango fruit Brazil",
        "manga bourbon cortada",
    ),
    "haden": (
        "Haden mango fruit",
        "Haden mango cut cross section half",
    ),
    "coquinho": (
        "Coquinho manga pequena Brazil",
        "manga pequena cortada Brazil",
    ),
    "maca": (
        "manga maçã coração Brazil",
        "manga maçã cortada",
    ),
    "mallika": (
        "Mallika mango fruit",
        "Mallika mango cut half cross section",
    ),
    "ataulfo": (
        "Ataulfo mango fruit yellow",
        "Ataulfo mango cut half cross section",
    ),
    "vandyke": (
        "Van Dyke mango fruit",
        "mango red cut cross section half",
    ),
    "osteen": (
        "Osteen mango fruit",
        "Osteen mango cut half",
    ),
    "sensation": (
        "Sensation mango fruit red purple",
        "Sensation mango cut half",
    ),
    "itamaraca": (
        "Itamaracá mango Pernambuco fruit",
        "manga pequena amarela cortada Pernambuco",
    ),
}

# Manually curated Wikimedia Commons filenames for best results
# (verified to be correct variety + right shot)
CURATED = {
    "tommy": {
        "whole": {"file": "MangaTommyAtkinsDSC4597.jpg",
                  "credit": "Embrapa, CC BY-SA 3.0 BR"},
        "cut":   {"file": "MangaTommyAtkinsDSC4598.jpg",
                  "credit": "Embrapa, CC BY-SA 3.0 BR"},
    },
    "palmer": {
        "whole": {"file": "Manga_palmer.jpg", "credit": None},
        "cut":   None,
    },
    "kent": {
        "whole": {"file": "Kent_mango.jpg", "credit": None},
        "cut":   None,
    },
    "keitt": {
        "whole": {"file": "Keitt_Mango_on_tree.jpg", "credit": None},
        "cut":   None,
    },
    "haden": {
        "whole": {"file": "Haden_mango.jpg", "credit": None},
        "cut":   None,
    },
    "mallika": {
        "whole": {"file": "Mallika_mango.jpg", "credit": None},
        "cut":   None,
    },
    "ataulfo": {
        "whole": {"file": "Ataulfo_mango.jpg", "credit": None},
        "cut":   None,
    },
}


def find_best_image(query):
    """Search Wikimedia and return best result."""
    try:
        d = wiki_search(query)
        pages = d.get("query", {}).get("pages", {})
        results = []
        for pid, p in pages.items():
            ii = p.get("imageinfo", [{}])[0]
            mime = ii.get("mime", "")
            size = ii.get("size", 0)
            if mime.startswith("image/") and "svg" not in mime:
                title = p["title"].replace("File:", "")
                results.append((size, title, ii.get("url", "")))
        if not results:
            return None
        # pick largest that's not too large (>8MB skip)
        results.sort(reverse=True)
        for sz, title, url in results:
            if sz < 8_000_000:
                return title
    except Exception as e:
        print(f"  Search error: {e}")
    return None


def process_variety(key, whole_query, cut_query):
    print(f"\n=== {key} ===")
    result = {"key": key, "whole": None, "cut": None, "credits": []}

    for kind, query in [("whole", whole_query), ("cut", cut_query)]:
        print(f"  [{kind}] Buscando: {query}")
        try:
            filename = find_best_image(query)
            if not filename:
                print(f"  [{kind}] Sem resultado.")
                continue
            print(f"  [{kind}] Encontrado: {filename}")
            info = wiki_thumb(filename)
            if not info or not info.get("thumb"):
                print(f"  [{kind}] Sem URL de thumb.")
                continue
            # check license is free
            lic = info.get("license", "")
            if lic and any(x in lic for x in ["CC BY", "CC0", "Public domain", "PD"]):
                print(f"  [{kind}] Licença: {lic} ✓")
            else:
                print(f"  [{kind}] Licença: '{lic}' — verificar manualmente, prosseguindo.")
            thumb_url = info["thumb"]
            print(f"  [{kind}] Baixando {thumb_url[:80]}...")
            data_uri = download_and_encode(thumb_url)
            result[kind] = data_uri
            credit = f"{filename} | {lic} | {info.get('author','')}"
            result["credits"].append(f"{kind}: {credit}")
            print(f"  [{kind}] OK ({len(data_uri)//1024} KB em base64)")
            time.sleep(0.5)
        except Exception as e:
            print(f"  [{kind}] ERRO: {e}")

    return result


if __name__ == "__main__":
    out_path = os.path.join(HERE, "photos_data.json")

    # load existing if any
    existing = {}
    if os.path.exists(out_path):
        existing = json.load(open(out_path, encoding="utf-8"))
        print(f"Carregados {len(existing)} existentes de {out_path}")

    for key, (wq, cq) in SEARCHES.items():
        if key in existing and existing[key].get("whole") and existing[key].get("cut"):
            print(f"[{key}] já tem ambas as fotos, pulando.")
            continue
        r = process_variety(key, wq, cq)
        if key in existing:
            # merge: keep what we had, add new
            if r["whole"]: existing[key]["whole"] = r["whole"]
            if r["cut"]: existing[key]["cut"] = r["cut"]
            existing[key]["credits"] = list(set(existing[key].get("credits",[]) + r["credits"]))
        else:
            existing[key] = r
        # save incrementally
        json.dump(existing, open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
        time.sleep(0.3)

    print(f"\n\nResultados salvos em {out_path}")
    for k, v in existing.items():
        w = "✓" if v.get("whole") else "✗"
        c = "✓" if v.get("cut") else "✗"
        print(f"  {k}: inteira={w}  cortada={c}")
