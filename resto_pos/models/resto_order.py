from odoo import _, fields, models
from odoo.exceptions import UserError


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

    line_ids = fields.One2many(
        "resto.order.line",
        "order_id",
        string="Order Lines",
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
            ("kitchen", "In Kitchen"),
            ("served", "Served"),
            ("paid", "Paid"),
        ],
        string="Status",
        required=True,
        default="draft",
    )

    def action_send_to_kitchen(self):
        for order in self:
            if order.state != "draft":
                raise UserError(_("Only draft orders can be sent to the kitchen."))
            order.state = "kitchen"

    def action_serve(self):
        for order in self:
            if order.state != "kitchen":
                raise UserError(_("Only orders in kitchen can be served"))
            order.state = "served"
