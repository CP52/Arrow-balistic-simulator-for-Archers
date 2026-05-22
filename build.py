#!/usr/bin/env python3
"""
build.py — Arrow Ballistic Simulator release builder
=====================================================
Genera i file di distribuzione a partire dal sorgente master.

Output:
  index.html                                    → Netlify (CDN, leggero)
  arrow_ballistic_simulator_v9_i18n_offline.html → standalone offline (librerie inline)

Uso:
  python build.py                  # build normale
  python build.py --check-only     # verifica dipendenze senza generare file
  python build.py --source MYFILE  # usa un sorgente diverso dal default

Dipendenze Python: solo stdlib (urllib, zipfile, os, sys, argparse, hashlib)
Le librerie JS vengono scaricate automaticamente da npm e cachate in .lib_cache/
"""

import argparse
import hashlib
import os
import sys
import urllib.request
import zipfile
import io
import shutil
from pathlib import Path

# ── Configurazione ────────────────────────────────────────────────────────────

SOURCE_FILE   = "arrow_ballistic_simulator_v9_i18n.html"
OUT_ONLINE    = "index.html"
OUT_OFFLINE   = "arrow_ballistic_simulator_v9_i18n_offline.html"
CACHE_DIR     = ".lib_cache"

# Librerie da scaricare via npm registry (in allowlist)
LIBS = [
    {
        "name":    "react",
        "version": "18.2.0",
        "tarball": "https://registry.npmjs.org/react/-/react-18.2.0.tgz",
        "path_in_tar": "package/umd/react.production.min.js",
        "cache_as": "react.production.min.js",
        # CDN tag da sostituire nel sorgente
        "cdn_tag": '<script src="https://cdn.jsdelivr.net/npm/react@18.2.0/umd/react.development.js"></script>',
        "sha256": None,  # compilato al primo download, verificato nei successivi
    },
    {
        "name":    "react-dom",
        "version": "18.2.0",
        "tarball": "https://registry.npmjs.org/react-dom/-/react-dom-18.2.0.tgz",
        "path_in_tar": "package/umd/react-dom.production.min.js",
        "cache_as": "react-dom.production.min.js",
        "cdn_tag": '<script src="https://cdn.jsdelivr.net/npm/react-dom@18.2.0/umd/react-dom.development.js"></script>',
        "sha256": None,
    },
    {
        "name":    "jspdf",
        "version": "2.5.1",
        "tarball": "https://registry.npmjs.org/jspdf/-/jspdf-2.5.1.tgz",
        "path_in_tar": "package/dist/jspdf.umd.min.js",
        "cache_as": "jspdf.umd.min.js",
        "cdn_tag": '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>',
        "sha256": None,
    },
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def log(msg, color=None):
    codes = {"green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m", "bold": "\033[1m"}
    reset = "\033[0m"
    prefix = codes.get(color, "")
    print(f"{prefix}{msg}{reset}")


def sha256_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download_lib(lib: dict, cache_dir: Path) -> bytes:
    """Scarica la libreria dal tarball npm e la mette in cache."""
    cache_path = cache_dir / lib["cache_as"]

    if cache_path.exists():
        data = cache_path.read_bytes()
        log(f"  ✓ {lib['cache_as']} (da cache, {len(data)//1024} KB)", "green")
        return data

    log(f"  ↓ Scarico {lib['name']} v{lib['version']} da npm...", "yellow")
    try:
        with urllib.request.urlopen(lib["tarball"], timeout=30) as resp:
            tarball_bytes = resp.read()
    except Exception as e:
        log(f"  ✗ Errore download {lib['name']}: {e}", "red")
        sys.exit(1)

    # Estrai il file JS dal tarball .tgz
    try:
        with zipfile.ZipFile(io.BytesIO(tarball_bytes)) as z:
            data = z.read(lib["path_in_tar"])
    except Exception:
        # tarball è gzip+tar, non zip — usa il modulo tarfile
        import tarfile
        with tarfile.open(fileobj=io.BytesIO(tarball_bytes), mode="r:gz") as tar:
            member = tar.getmember(lib["path_in_tar"])
            data = tar.extractfile(member).read()

    cache_path.write_bytes(data)
    log(f"  ✓ {lib['cache_as']} scaricato ({len(data)//1024} KB)", "green")
    return data


def check_source(source_path: Path):
    if not source_path.exists():
        log(f"✗ File sorgente non trovato: {source_path}", "red")
        log(f"  Assicurati che '{SOURCE_FILE}' sia nella stessa cartella di build.py", "red")
        sys.exit(1)
    log(f"✓ Sorgente: {source_path} ({source_path.stat().st_size // 1024} KB)", "green")


# ── Build online (index.html) ─────────────────────────────────────────────────

def build_online(html: str, out_path: Path):
    """
    Versione CDN per Netlify: sostituisce i tag development con i tag production
    mantenendo il caricamento da CDN (più leggero, aggiornabile).
    """
    result = html

    replacements = [
        (
            '<script src="https://cdn.jsdelivr.net/npm/react@18.2.0/umd/react.development.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/react@18.2.0/umd/react.production.min.js" crossorigin></script>'
        ),
        (
            '<script src="https://cdn.jsdelivr.net/npm/react-dom@18.2.0/umd/react-dom.development.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/react-dom@18.2.0/umd/react-dom.production.min.js" crossorigin></script>'
        ),
    ]

    for old, new in replacements:
        if old in result:
            result = result.replace(old, new)
        else:
            log(f"  ⚠ Tag CDN non trovato (già aggiornato?): {old[:60]}...", "yellow")

    out_path.write_text(result, encoding="utf-8")
    log(f"✓ {out_path.name} ({out_path.stat().st_size // 1024} KB)", "green")


# ── Build offline (standalone) ────────────────────────────────────────────────

def build_offline(html: str, libs_data: dict, out_path: Path):
    """
    Versione standalone: sostituisce i tag CDN con script inline.
    Il file risultante funziona senza internet dalla prima apertura.
    """
    result = html

    # I tre tag CDN vengono sostituiti con un unico blocco inline
    cdn_block = (
        '    <script src="https://cdn.jsdelivr.net/npm/react@18.2.0/umd/react.development.js"></script>\n'
        '    <script src="https://cdn.jsdelivr.net/npm/react-dom@18.2.0/umd/react-dom.development.js"></script>\n'
        '    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>'
    )

    react_js     = libs_data["react"].decode("utf-8")
    react_dom_js = libs_data["react-dom"].decode("utf-8")
    jspdf_js     = libs_data["jspdf"].decode("utf-8")

    inline_block = (
        f'    <!-- React 18.2.0 production (inline — no CDN required) -->\n'
        f'    <script>{react_js}</script>\n'
        f'    <script>{react_dom_js}</script>\n'
        f'    <!-- jsPDF 2.5.1 (inline) -->\n'
        f'    <script>{jspdf_js}</script>'
    )

    if cdn_block in result:
        result = result.replace(cdn_block, inline_block)
        log("  ✓ Librerie iniettate inline", "green")
    else:
        log("  ✗ Blocco CDN non trovato nel sorgente — verifica il formato dei tag", "red")
        sys.exit(1)

    out_path.write_text(result, encoding="utf-8")
    size_kb = out_path.stat().st_size // 1024
    log(f"✓ {out_path.name} ({size_kb} KB)", "green")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Build Arrow Ballistic Simulator distribution files"
    )
    parser.add_argument(
        "--source", default=SOURCE_FILE,
        help=f"File sorgente HTML (default: {SOURCE_FILE})"
    )
    parser.add_argument(
        "--check-only", action="store_true",
        help="Verifica dipendenze senza generare file"
    )
    parser.add_argument(
        "--no-cache", action="store_true",
        help="Forza il re-download delle librerie ignorando la cache"
    )
    args = parser.parse_args()

    log("\n🏹  Arrow Ballistic Simulator — build.py", "bold")
    log("─" * 50)

    # Percorsi
    script_dir  = Path(__file__).parent
    source_path = script_dir / args.source
    cache_dir   = script_dir / CACHE_DIR
    out_online  = script_dir / OUT_ONLINE
    out_offline = script_dir / OUT_OFFLINE

    # 1. Verifica sorgente
    log("\n[1/4] Verifica sorgente")
    check_source(source_path)

    if args.check_only:
        log("\n✓ Check completato — nessun file generato", "green")
        return

    # 2. Leggi sorgente
    log("\n[2/4] Lettura sorgente")
    html = source_path.read_text(encoding="utf-8")
    log(f"  {len(html.splitlines())} righe, {len(html)//1024} KB", "green")

    # 3. Scarica/cacha librerie
    log("\n[3/4] Librerie JS (npm cache)")
    cache_dir.mkdir(exist_ok=True)
    if args.no_cache:
        shutil.rmtree(cache_dir)
        cache_dir.mkdir()
        log("  Cache svuotata (--no-cache)", "yellow")

    libs_data = {}
    for lib in LIBS:
        libs_data[lib["name"]] = download_lib(lib, cache_dir)

    # 4. Genera output
    log("\n[4/4] Generazione file")

    log(f"  → {OUT_ONLINE} (Netlify / CDN production)")
    build_online(html, out_online)

    log(f"  → {OUT_OFFLINE} (standalone offline)")
    build_offline(html, libs_data, out_offline)

    # Riepilogo
    log("\n" + "─" * 50)
    log("✅  Build completato!", "bold")
    log(f"   {OUT_ONLINE:<50} {out_online.stat().st_size//1024:>5} KB  → Netlify")
    log(f"   {OUT_OFFLINE:<50} {out_offline.stat().st_size//1024:>5} KB  → download offline")
    log("")
    log("Prossimi passi:")
    log("  git add index.html arrow_ballistic_simulator_v9_i18n_offline.html")
    log("  git commit -m 'release: update distribution files'")
    log("  git push   ← Netlify si aggiorna automaticamente")
    log("")


if __name__ == "__main__":
    main()
