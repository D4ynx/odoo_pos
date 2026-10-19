from odoo import fields, models


class RestoMenuItem(models.Model):
    _name = "resto.menu.item"
    _description = "Resto Menu Item"
    _order = "name"

    name = fields.Char(string="Menu Item Name", required=True)
    price = fields.Float(string="Price", required=True)
    active = fields.Boolean(string="Active", default=True)
