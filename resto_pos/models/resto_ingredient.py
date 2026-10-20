from odoo import api, fields, models


class RestoIngredient(models.Model):
    _name = "resto.ingredient"
    _description = "Resto Ingredient"
    _order = "name"

    name = fields.Char(string="Ingredient Name", required=True)
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure", required=True)
    min_qty = fields.Float(string="Minimum Quantity")
    active = fields.Boolean(string="Active", default=True)

    lot_ids = fields.One2many(
        "resto.stock.lot",
        "ingredient_id",
        string="Stock Lots",
    )

    qty_on_hand = fields.Float(
        string="On Hand",
        compute="_compute_qty_on_hand",
        store=True,
    )

    @api.depends("lot_ids.remaining_qty")
    def _compute_qty_on_hand(self):
        for ingredient in self:
            ingredient.qty_on_hand = sum(ingredient.lot_ids.mapped("remaining_qty"))
