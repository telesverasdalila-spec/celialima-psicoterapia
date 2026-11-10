#!/usr/bin/env python3
"""Mescla capa + corpo do manual em PDF final."""

from pathlib import Path
from pypdf import PdfReader, PdfWriter

A4_W, A4_H = 595.28, 841.89

def normalize_page_to_a4(page):
    box = page.mediabox
    w, h = float(box.width), float(box.height)
    if abs(w - A4_W) > 0.1 or abs(h - A4_H) > 0.1:
        page.scale_to(A4_W, A4_H)
    return page

def merge(cover_pdf, body_pdf, out_pdf):
    writer = PdfWriter()
    cover = PdfReader(cover_pdf).pages[0]
    writer.add_page(normalize_page_to_a4(cover))
    for page in PdfReader(body_pdf).pages:
        writer.add_page(normalize_page_to_a4(page))
    writer.add_metadata({
        '/Title': 'Manual de Implementação — Projeto Célia Lima',
        '/Author': 'Dalila Teles Veras',
        '/Creator': 'Dalila Teles Veras',
        '/Subject': 'Manual técnico: site institucional + blog terapêutico + livro PDF para Célia Lima',
        '/Keywords': 'Célia Lima, manual, implementação, case study, portfólio, Next.js, Python, Vercel',
    })
    with open(out_pdf, 'wb') as f:
        writer.write(f)
    print(f"[ok] PDF final: {out_pdf}")
    print(f"     Total de páginas: {len(writer.pages)}")
    print(f"     Tamanho: {Path(out_pdf).stat().st_size / 1024:.1f} KB")

if __name__ == '__main__':
    merge(
        cover_pdf='/home/z/my-project/download/manual-celia-capa.pdf',
        body_pdf='/home/z/my-project/download/manual-celia-corpo.pdf',
        out_pdf='/home/z/my-project/download/Manual-Implementacao-Celia-Lima.pdf',
    )
