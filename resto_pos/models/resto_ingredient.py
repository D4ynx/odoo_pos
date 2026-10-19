from odoo import fields, models


class RestoIngredient(models.Model):
    _name = "resto.ingredient"
    _description = "Resto Ingredient"

    name = fields.Char(string="Ingredient Name", required=True)
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure", required=True)
    min_qty = fields.Float(string="Minimum Quantity")
    active = fields.Boolean(string="Active", default=True)
