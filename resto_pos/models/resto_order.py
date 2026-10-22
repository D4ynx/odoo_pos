from odoo import fields, models


class RestoOrder(models.Model):
    _name = "resto.order"
    _description = "Resto Order"
    _order = "id desc"

    name = fields.Char(
        string="Order",
        required=True,
        default="New",
    )

    table_id = fields.Many2one(
        "resto.table",
        string="Table",
        required=True,
    )

    user_id = fields.Many2one(
        "res.users",
        string="Waiter",
        default=lambda self: self.env.user,
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("inKitchen", "In Kitchen"),
            ("served", "Served"),
            ("paid", "Paid"),
        ],
        string="Status",
        required=True,
        default="draft",
    )
