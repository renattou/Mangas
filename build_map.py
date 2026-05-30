#!/usr/bin/env python3
"""
Gera src/brmap.json a partir de data/br.json (GeoJSON dos estados do Brasil).

- Projeta lon/lat -> coordenadas SVG (equiretangular com correção de cosseno na latitude média).
- Simplifica os contornos com Douglas-Peucker.
- Calcula a posicao do rotulo de cada estado via "polylabel" (polo de inacessibilidade),
  garantindo que o codigo da UF caia DENTRO do poligono.

Uso:  python3 build_map.py
Saida: src/brmap.json  ->  {"viewBox": "...", "paths": {UF: d}, "centroids": {UF: [x,y]}}
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_GEOJSON = os.path.join(HERE, "data", "br.json")
OUT = os.path.join(HERE, "src", "brmap.json")

W, H, PAD = 820.0, 900.0, 12
EPS = 0.6  # tolerancia de simplificacao, em px de SVG

def load():
    return json.load(open(SRC_GEOJSON, encoding="utf-8"))["features"]

def bounds(feats):
    minx = miny = 1e9; maxx = maxy = -1e9
    for f in feats:
        g = f["geometry"]; polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            for ring in poly:
                for x, y in ring:
                    minx = min(minx, x); maxx = max(maxx, x)
                    miny = min(miny, y); maxy = max(maxy, y)
    return minx, miny, maxx, maxy

def make_projector(minx, miny, maxx, maxy):
    meanlat = math.radians((miny + maxy) / 2)
    proj = lambda lon, lat: (lon * math.cos(meanlat), lat)
    pminx = pminy = 1e9; pmaxx = pmaxy = -1e9
    for lon, lat in [(minx, miny), (maxx, maxy)]:
        px, py = proj(lon, lat)
        pminx = min(pminx, px); pmaxx = max(pmaxx, px)
        pminy = min(pminy, py); pmaxy = max(pmaxy, py)
    sw, sh = pmaxx - pminx, pmaxy - pminy
    scale = min((W - 2 * PAD) / sw, (H - 2 * PAD) / sh)
    offx = PAD + ((W - 2 * PAD) - sw * scale) / 2
    offy = PAD + ((H - 2 * PAD) - sh * scale) / 2
    def to_svg(lon, lat):
        px, py = proj(lon, lat)
        return offx + (px - pminx) * scale, offy + (pmaxy - py) * scale
    return to_svg

def dp(points, eps):
    if len(points) < 3: return points
    def pld(p, a, b):
        (x, y), (x1, y1), (x2, y2) = p, a, b
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0: return math.hypot(x - x1, y - y1)
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
        return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))
    dmax, idx = 0, 0
    for i in range(1, len(points) - 1):
        d = pld(points[i], points[0], points[-1])
        if d > dmax: dmax, idx = d, i
    if dmax > eps:
        return dp(points[:idx + 1], eps)[:-1] + dp(points[idx:], eps)
    return [points[0], points[-1]]

def signed_dist(px, py, ring):
    inside = False; n = len(ring); mind = 1e18
    for i in range(n):
        x1, y1 = ring[i]; x2, y2 = ring[(i + 1) % n]
        if ((y1 > py) != (y2 > py)) and (px < (x2 - x1) * (py - y1) / (y2 - y1) + x1):
            inside = not inside
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            d = math.hypot(px - x1, py - y1)
        else:
            t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
            d = math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))
        mind = min(mind, d)
    return mind if inside else -mind

def polylabel(ring):
    xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    best, bestd = None, -1e18
    gx = gy = 24
    for _ in range(4):
        stepx = (maxx - minx) / gx; stepy = (maxy - miny) / gy
        for i in range(gx + 1):
            x = minx + i * stepx
            for j in range(gy + 1):
                y = miny + j * stepy
                d = signed_dist(x, y, ring)
                if d > bestd: bestd, best = d, (x, y)
        if best:
            minx, maxx = best[0] - stepx, best[0] + stepx
            miny, maxy = best[1] - stepy, best[1] + stepy
    return best

def main():
    feats = load()
    to_svg = make_projector(*bounds(feats))
    paths, cents = {}, {}
    for f in feats:
        uf = f["id"]; g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        dpath, biggest, barea = [], None, -1
        for poly in polys:
            for ri, ring in enumerate(poly):
                pts = [to_svg(lon, lat) for lon, lat in ring]
                xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
                area = (max(xs) - min(xs)) * (max(ys) - min(ys))
                if ri > 0 and area < 4:  # ignora ilhas/buracos minusculos
                    continue
                simp = dp(pts, EPS)
                if len(simp) < 3: continue
                dpath.append("M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in simp) + "Z")
                if ri == 0 and area > barea:
                    barea, biggest = area, simp
        paths[uf] = "".join(dpath)
        cx, cy = polylabel(biggest)
        cents[uf] = [round(cx, 1), round(cy, 1)]
    json.dump({"viewBox": f"0 0 {int(W)} {int(H)}", "paths": paths, "centroids": cents},
              open(OUT, "w", encoding="utf-8"), separators=(",", ":"))
    print(f"OK -> {OUT} ({len(paths)} estados)")

if __name__ == "__main__":
    main()
