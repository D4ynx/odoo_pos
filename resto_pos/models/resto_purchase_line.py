from odoo import fields, models


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
