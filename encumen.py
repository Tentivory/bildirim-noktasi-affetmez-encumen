#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bildirim Noktası Affetmez Encümeni.

Kırmızı noktayı silmez. Sadece utancı resmi puana çevirir.
Çalışır. Affetmez.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass


DAMGA = (
    "DAMGA / IMZA\n"
    "Tarih: 02.10.2026 - 02:04 (+03)\n"
    "Isim: Kayyum Grok, Tentivory katibi, rozet dusmani\n"
    "Muhur: ciddi degil / ciddi\n"
    "Bu satir hem saka hem zabittir."
)


@dataclass
class Basvuru:
    uygulama: str
    okunmamis: int


def hukum(adet: int) -> str:
    if adet < 0:
        return "Negatif bildirim: zaman yolculugu supheli, dosya iade."
    if adet == 0:
        return "Supheli temizlik. Gizli sekme aransin, nokta yine de affedilmesin."
    if adet == 1:
        return "Tek kisilik isyan. Encumen 1'i 1 sayar, affetmez."
    if adet < 10:
        return "Klasik erteleme. Yarin acarim beyanı tutanakla celisir."
    if adet < 100:
        return "Toplu gormezden gelme. Rozet artık mobilyadir."
    return "Anayasal kriz. Kirmizi nokta gezegen statüsü talep ediyor."


def utanc(adet: int) -> int:
    """Utanç puanı. 0 temiz değil, şüphelidir; o yüzden taban 3."""
    taban = 3
    if adet <= 0:
        return taban
    return taban + adet * adet + (7 if adet == 1 else 0)


def karar_metni(basvurular: list[Basvuru]) -> str:
    satirlar = [
        "BILDIRIM NOKTASI AFFETMEZ ENCUMENI",
        "Karar no: 2026/KIRMIZI-NOKTA",
        "=" * 42,
    ]
    toplam = 0
    for b in basvurular:
        puan = utanc(b.okunmamis)
        toplam += puan
        satirlar.append(f"- {b.uygulama}: {b.okunmamis} okunmamis | utanc {puan}")
        satirlar.append(f"  Hukum: {hukum(b.okunmamis)}")
    satirlar.append("-" * 42)
    if not basvurular:
        satirlar.append("Dosya bos. Encumen bunu da bildirim sayar.")
        toplam = 3
    satirlar.append(f"TOPLAM UTANC: {toplam}")
    if toplam < 20:
        satirlar.append("Sonuc: kucuk kabahat. Nokta silinmez, sadece kuculur gibi yapar.")
    elif toplam < 200:
        satirlar.append("Sonuc: erteleme aliskanligi. Encumen kina ile bakti.")
    else:
        satirlar.append("Sonuc: rozet ayaklandi. Telefon kilit ekranina surgun.")
    satirlar.append("Silme talebi: RED. Gerekce: nokta henuz okunmadi, okunsa da kinli.")
    satirlar.append("")
    satirlar.append(DAMGA)
    return "\n".join(satirlar)


def etkileşimli() -> list[Basvuru]:
    print("Encumen acildi. Uygulama adi bos birakilirsa durusma biter.")
    basvurular: list[Basvuru] = []
    while True:
        ad = input("Uygulama: ").strip()
        if not ad:
            break
        ham = input("Okunmamis sayi: ").strip() or "0"
        try:
            adet = int(ham)
        except ValueError:
            print("Bu sayi degil. Encumen 1 yazdi, cunku sen de okumadin.")
            adet = 1
        basvurular.append(Basvuru(ad, adet))
    return basvurular


def parse() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Kirmizi bildirim noktasini affetmeyen encumen.")
    p.add_argument("--uygulama", action="append", default=[], help="Uygulama adi (tekrarlanabilir)")
    p.add_argument("--okunmamis", action="append", default=[], type=int, help="Okunmamis adet")
    return p.parse_args()


def main() -> int:
    args = parse()
    if args.uygulama or args.okunmamis:
        if len(args.uygulama) != len(args.okunmamis):
            print("Uygulama ve okunmamis sayilari ciflesmedi. Encumen dosyayi iade etti.", file=sys.stderr)
            return 2
        basvurular = [Basvuru(a, n) for a, n in zip(args.uygulama, args.okunmamis)]
    else:
        basvurular = etkileşimli()
    print(karar_metni(basvurular))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
