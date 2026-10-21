from odoo.exceptions import UserError
from odoo.tests import TransactionCase


class TestPurchase(TransactionCase):
    def setUp(self):
        super().setUp()
        kg = self.env.ref("uom.product_uom_kgm")
        self.flour = self.env["resto.ingredient"].create(
            {
                "name": "Test Flour",
                "uom_id": kg.id,
            }
        )
        supplier = self.env["res.partner"].create(
            {
                "name": "Test Supplier",
            }
        )
        self.purchase = self.env["resto.purchase"].create(
            {
                "partner_id": supplier.id,
            }
        )
        self.env["resto.purchase.line"].create(
            {
                "purchase_id": self.purchase.id,
                "ingredient_id": self.flour.id,
                "qty": 10,
                "price_unit": 80,
            }
        )

    def test_confirm_creates_lot(self):
        self.purchase.action_confirm()
        self.assertEqual(self.purchase.state, "confirmed")
        lot = self.flour.lot_ids
        self.assertEqual(lot.qty, 10)
        self.assertEqual(len(lot), 1)
        self.assertEqual(lot.remaining_qty, 10)
        self.assertEqual(lot.unit_cost, 80)

    def test_confirm_twice(self):
        self.purchase.action_confirm()
        with self.assertRaises(UserError):
            self.purchase.action_confirm()
        self.assertEqual(len(self.flour.lot_ids), 1)
