from odoo import fields
from odoo import models


class RestoMenuItem(models.Model):
    _name = "resto.menu.item"
    _description = "Resto Menu Item"
    _order = "name"

    name = fields.Char(string="Menu Item Name", required=True)
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    price = fields.Monetary(string="Price", currency_field="currency_id", required=True)

    category_ids = fields.Many2many(
        "resto.menu.category",
        string="Menu Categories",
    )

    active = fields.Boolean(string="Active", default=True)

    recipe_line_ids = fields.One2many(
        "resto.recipe.line",
        "menu_item_id",
        string="Recipe",
    )
