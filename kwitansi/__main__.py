"""CLI: python -m kwitansi --seller X --buyer Y --item "Nama:qty:harga" [--html] [-o out]"""
import argparse
import json
import sys

from .core import build_invoice, render_html, render_text


def parse_item(text):
    parts = text.rsplit(":", 2)
    if len(parts) != 3:
        raise ValueError(f"item harus berbentuk Nama:qty:harga, bukan: {text}")
    name, qty, price = parts
    return {"name": name, "qty": int(qty), "price": int(price)}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="kwitansi", description="Make an invoice with automatic terbilang.")
    parser.add_argument("--spec", help="JSON file with seller, buyer, items, number, date")
    parser.add_argument("--seller", default="")
    parser.add_argument("--buyer", default="")
    parser.add_argument("--number", default="INV-001")
    parser.add_argument("--date", default="")
    parser.add_argument("--item", action="append", default=[],
                        help="Item as Nama:qty:harga, repeatable")
    parser.add_argument("--html", action="store_true", help="Output HTML instead of plain text")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    args = parser.parse_args(argv)

    if args.spec:
        with open(args.spec, encoding="utf-8") as handle:
            spec = json.load(handle)
    else:
        try:
            items = [parse_item(text) for text in args.item]
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        if not items:
            print("error: minimal satu --item atau pakai --spec", file=sys.stderr)
            return 2
        spec = {"seller": args.seller, "buyer": args.buyer,
                "number": args.number, "date": args.date, "items": items}
    invoice = build_invoice(spec)
    output = render_html(invoice) if args.html else render_text(invoice)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
