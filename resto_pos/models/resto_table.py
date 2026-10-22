from odoo import fields, models


class RestoTable(models.Model):
    _name = "resto.table"
    _description = "Resto Table"
    _order = "name"

    name = fields.Char(
        string="Table",
        required=True,
    )

    seats = fields.Integer(
        string="Seats",
        default=4,
    )

    state = fields.Selection(
        [
            ("free", "Free"),
            ("occupied", "Occupied"),
        ],
        string="Status",
        required=True,
        default="free",
    )
