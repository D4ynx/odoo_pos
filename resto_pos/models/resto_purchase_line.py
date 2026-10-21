from odoo import api, fields, models


class RestoPurchaseLine(models.Model):
    _name = "resto.purchase.line"
    _description = "Resto Purchase Line"

    purchase_id = fields.Many2one(
        "resto.purchase",
        string="Purchase",
        required=True,
        ondelete="cascade",
    )

    ingredient_id = fields.Many2one(
        "resto.ingredient",
        string="Ingredient",
        required=True,
        ondelete="restrict",
    )

    qty = fields.Float(string="Quantity", required=True)

    uom_id = fields.Many2one(
        related="ingredient_id.uom_id",
        string="Unit",
    )

    currency_id = fields.Many2one(
        related="purchase_id.currency_id",
    )

    price_unit = fields.Monetary(
        string="Unit Price", currency_field="currency_id", required=True
    )
    subtotal = fields.Monetary(
        string="Subtotal",
        currency_field="currency_id",
        compute="_compute_subtotal",
    )

    @api.depends("qty", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.price_unit
