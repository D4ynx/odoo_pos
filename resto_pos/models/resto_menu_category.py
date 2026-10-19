from odoo import fields
from odoo import models


class RestoMenuCategory(models.Model):
    _name = "resto.menu.category"
    _description = "Resto Menu Category"
    _order = "name"

    name = fields.Char(string="Category Name", required=True)
