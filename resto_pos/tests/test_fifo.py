from odoo.tests import TransactionCase


class TestFifo(TransactionCase):
    def setUp(self):
        super().setUp()
        kg = self.env.ref("uom.product_uom_kgm")
        self.flour = self.env["resto.ingredient"].create(
            {
                "name": "Test Flour",
                "uom_id": kg.id,
            }
        )
        self.lot_a = self.env["resto.stock.lot"].create(
            {
                "ingredient_id": self.flour.id,
                "date": "2026-10-01",
                "qty": 100,
                "remaining_qty": 100,
                "unit_cost": 2.0,
            }
        )
        self.lot_b = self.env["resto.stock.lot"].create(
            {
                "ingredient_id": self.flour.id,
                "date": "2026-10-05",
                "qty": 50,
                "remaining_qty": 50,
                "unit_cost": 3.0,
            }
        )

    def test_single_lot(self):
        cost = self.flour._consume_fifo(40)
        self.assertEqual(cost, 2 * 40)
        self.assertEqual(self.lot_a.remaining_qty, 60)
        self.assertEqual(self.lot_b.remaining_qty, 50)

    def test_cross_lot(self):
        cost = self.flour._consume_fifo(120)
        self.assertEqual(cost, 2 * 100 + 3 * 20)
        self.assertEqual(self.lot_a.remaining_qty, 0)
        self.assertEqual(self.lot_b.remaining_qty, 30)
