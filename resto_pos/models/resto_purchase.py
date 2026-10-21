from odoo import fields, models


class RestoPurchase(models.Model):
    _name = "resto.purchase"
    _description = "Resto Purchase"
    _order = "date desc, id desc"

    partner_id = fields.Many2one(
        "res.partner",
        string="Supplier",
        required=True,
    )

    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.context_today,
    )

    line_ids = fields.One2many(
        "resto.purchase.line",
        "purchase_id",
        string="Purchase Lines",
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
