from odoo import fields, models


class RestoStockLot(models.Model):
    _name = "resto.stock.lot"
    _description = "Resto Stock Lot"
    _order = "date, id"

    ingredient_id = fields.Many2one(
        "resto.ingredient",
        string="Ingredient",
        required=True,
        ondelete="restrict",
    )

    date = fields.Date(string="Date", required=True, default=fields.Date.context_today)
    qty = fields.Float(string="Quantity", required=True)
    remaining_qty = fields.Float(string="Remaining Quantity", required=True)

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    unit_cost = fields.Monetary(
        string="Unit Cost", currency_field="currency_id", required=True
    )

    uom_id = fields.Many2one(
        related="ingredient_id.uom_id",
        string="Unit",
    )
