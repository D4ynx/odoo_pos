from odoo import fields, models


class RestoMenuItem(models.Model):
    _name = "resto.menu.item"
    _description = "Resto Menu Item"
    _order = "name"

    name = fields.Char(string="Menu Item Name", required=True)
    price = fields.Monetary(string="Price", currency_field="currency_id", required=True)
    active = fields.Boolean(string="Active", default=True)

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
