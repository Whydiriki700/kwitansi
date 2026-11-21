import sys, unittest
sys.path.insert(0, ".")
from kwitansi.core import build_invoice, format_rupiah, render_html, render_text, terbilang

class TerbilangTests(unittest.TestCase):
    def test_small(self):
        self.assertEqual(terbilang(0), "nol")
        self.assertEqual(terbilang(7), "tujuh")
        self.assertEqual(terbilang(11), "sebelas")
        self.assertEqual(terbilang(19), "sembilan belas")
        self.assertEqual(terbilang(75), "tujuh puluh lima")
    def test_hundreds(self):
        self.assertEqual(terbilang(100), "seratus")
        self.assertEqual(terbilang(115), "seratus lima belas")
        self.assertEqual(terbilang(999), "sembilan ratus sembilan puluh sembilan")
    def test_thousands(self):
        self.assertEqual(terbilang(1000), "seribu")
        self.assertEqual(terbilang(2500), "dua ribu lima ratus")
    def test_big(self):
        self.assertEqual(terbilang(1500000), "satu juta lima ratus ribu")
        self.assertEqual(terbilang(1000000000), "satu miliar")
        self.assertEqual(terbilang(2500750), "dua juta lima ratus ribu tujuh ratus lima puluh")

class InvoiceTests(unittest.TestCase):
    SPEC = {"number": "INV-007", "date": "2026-11-22", "seller": "Toko Berkah",
            "buyer": "Budi",
            "items": [{"name": "Template Pro", "qty": 1, "price": 299000},
                      {"name": "Konsultasi", "qty": 2, "price": 50000}]}
    def test_total_and_terbilang(self):
        inv = build_invoice(self.SPEC)
        self.assertEqual(inv["total"], 399000)
        self.assertEqual(inv["terbilang"], "Tiga ratus sembilan puluh sembilan ribu rupiah")
    def test_format_rupiah(self):
        self.assertEqual(format_rupiah(1500000), "Rp 1.500.000")
    def test_render_text(self):
        text = render_text(build_invoice(self.SPEC))
        self.assertIn("TOTAL: Rp 399.000", text)
        self.assertIn("Terbilang:", text)
    def test_render_html(self):
        page = render_html(build_invoice(self.SPEC))
        self.assertIn("INVOICE INV-007", page)
        self.assertIn("Tiga ratus sembilan puluh sembilan ribu rupiah", page)

if __name__ == "__main__":
    unittest.main()
