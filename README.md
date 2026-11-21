# kwitansi

Invoices for Indonesian sellers and freelancers, with the one feature
everyone here actually needs: automatic terbilang, the total spelled out
in Indonesian words.

Give it a seller, a buyer, and a list of items. kwitansi totals them,
formats the money as Rupiah, and writes the line Indonesian buyers expect
to see: "Terbilang: Tiga ratus sembilan puluh sembilan ribu rupiah".

## Usage

From arguments:

```
python -m kwitansi --seller "Toko Berkah" --buyer "Budi" --number INV-007 --date 2026-11-22 --item "Template Pro:1:299000" --item "Konsultasi:2:50000"
```

From a JSON spec file, with an HTML invoice you can print or send:

```
python -m kwitansi --spec invoice.json --html -o invoice.html
```

The spec is a small JSON object with seller, buyer, number, date, and an
items list of name, qty, and price.

## Terbilang

The number words engine handles everything from nol to trillions,
including the special forms seratus, seribu, and sebelas:

- 115 becomes "seratus lima belas"
- 2500750 becomes "dua juta lima ratus ribu tujuh ratus lima puluh"
- 1500000 becomes "satu juta lima ratus ribu"

## Tests

```
python -m unittest discover -s tests
```

Zero dependencies. Python 3.9+. MIT license.
