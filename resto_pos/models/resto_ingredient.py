from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


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

    @api.constrains("uom_id")
    def _check_uom_locked(self):
        for ingredient in self:
            if ingredient.lot_ids:
                raise ValidationError(
                    _(
                        "You cannot change the unit of %s because it already has stock lots. Archive it and create a new ingredient instead.",
                        ingredient.name,
                    )
                )

    def _consume_fifo(self, qty):
        self.ensure_one()
        if qty > self.qty_on_hand:
            raise UserError(
                _(
                    "Not enough %s in stock: need %s, have %s.",
                    self.name,
                    qty,
                    self.qty_on_hand,
                )
            )
        needed = qty
        cost = 0
        for lot in self.lot_ids:
            take = min(lot.remaining_qty, needed)
            lot.remaining_qty -= take
            cost += take * lot.unit_cost
            needed -= take
            if needed == 0:
                break
        return cost
