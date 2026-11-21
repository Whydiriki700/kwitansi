"""Terbilang (Indonesian number words) and invoice rendering."""
import html

UNITS = ["", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh",
         "delapan", "sembilan", "sepuluh", "sebelas"]
SCALES = [(10 ** 12, "triliun"), (10 ** 9, "miliar"), (10 ** 6, "juta"),
          (10 ** 3, "ribu")]


def terbilang(n):
    n = int(n)
    if n == 0:
        return "nol"
    if n < 0:
        return "minus " + terbilang(-n)
    if n < 12:
        return UNITS[n]
    if n < 20:
        return terbilang(n - 10) + " belas"
    if n < 100:
        words = terbilang(n // 10) + " puluh"
        return words + (" " + terbilang(n % 10) if n % 10 else "")
    if n < 200:
        return "seratus" + (" " + terbilang(n - 100) if n > 100 else "")
    if n < 1000:
        words = terbilang(n // 100) + " ratus"
        return words + (" " + terbilang(n % 100) if n % 100 else "")
    for scale, word in SCALES:
        if n >= scale:
            head = n // scale
            if scale == 1000 and head == 1:
                head_words = "seribu"
            else:
                head_words = terbilang(head) + " " + word
            rest = terbilang(n % scale) if n % scale else ""
            return (head_words + " " + rest).strip()
    return ""


def format_rupiah(n):
    return "Rp " + f"{int(n):,}".replace(",", ".")


def build_invoice(spec):
    items = []
    total = 0
    for raw in spec["items"]:
        qty = int(raw["qty"])
        price = int(raw["price"])
        amount = qty * price
        total += amount
        items.append({"name": raw["name"], "qty": qty, "price": price,
                      "amount": amount})
    return {
        "number": spec.get("number", "INV-001"),
        "date": spec.get("date", ""),
        "seller": spec.get("seller", ""),
        "buyer": spec.get("buyer", ""),
        "items": items,
        "total": total,
        "terbilang": terbilang(total).capitalize() + " rupiah",
    }


def render_text(inv):
    lines = ["=" * 48, f"INVOICE {inv['number']}", "=" * 48]
    if inv["date"]:
        lines.append(f"Tanggal : {inv['date']}")
    lines.append(f"Penjual : {inv['seller']}")
    lines.append(f"Pembeli : {inv['buyer']}")
    lines.append("-" * 48)
    for item in inv["items"]:
        lines.append(f"{item['name']}")
        lines.append(f"  {item['qty']} x {format_rupiah(item['price'])} = {format_rupiah(item['amount'])}")
    lines.append("-" * 48)
    lines.append(f"TOTAL: {format_rupiah(inv['total'])}")
    lines.append(f"Terbilang: {inv['terbilang']}")
    lines.append("=" * 48)
    return "\n".join(lines) + "\n"


def render_html(inv):
    rows = "\n".join(
        f"<tr><td>{html.escape(item['name'])}</td><td class='n'>{item['qty']}</td>"
        f"<td class='n'>{format_rupiah(item['price'])}</td>"
        f"<td class='n'>{format_rupiah(item['amount'])}</td></tr>"
        for item in inv["items"])
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>Invoice {html.escape(inv['number'])}</title>
<style>
body {{ font-family: Georgia, serif; margin: 40px auto; max-width: 720px; color: #1a1a1a; }}
h1 {{ font-size: 22px; letter-spacing: 2px; margin-bottom: 4px; }}
.meta {{ color: #555; margin-bottom: 24px; }}
table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
th, td {{ border-bottom: 1px solid #ccc; padding: 8px 6px; text-align: left; }}
td.n, th.n {{ text-align: right; }}
.total {{ font-size: 18px; font-weight: bold; }}
.terbilang {{ font-style: italic; color: #333; }}
</style>
</head>
<body>
<h1>INVOICE {html.escape(inv['number'])}</h1>
<div class="meta">
Tanggal: {html.escape(inv['date'])}<br>
Penjual: {html.escape(inv['seller'])}<br>
Pembeli: {html.escape(inv['buyer'])}
</div>
<table>
<tr><th>Item</th><th class="n">Qty</th><th class="n">Harga</th><th class="n">Jumlah</th></tr>
{rows}
</table>
<p class="total">TOTAL: {format_rupiah(inv['total'])}</p>
<p class="terbilang">Terbilang: {html.escape(inv['terbilang'])}</p>
</body>
</html>
"""
