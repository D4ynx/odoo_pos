from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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

    @api.constrains("ingredient_id", "uom_id")
    def _check_uom_category(self):
        for line in self:
            if line.uom_id.category_id != line.ingredient_id.uom_id.category_id:
                raise ValidationError(
                    _(
                        "The unit of '%s' must be the same kind as its stock unit (%s).",
                        line.ingredient_id.name,
                        line.ingredient_id.uom_id.name,
                    )
                )
