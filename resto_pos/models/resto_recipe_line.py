from odoo import fields, models


class RestoRecipeLine(models.Model):
    _name = "resto.recipe.line"
    _description = "Resto Recipe Line"

    menu_item_id = fields.Many2one(
        "resto.menu.item",
        string="Menu Item",
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
        "uom.uom",
        string="Unit",
        required=True,
    )
