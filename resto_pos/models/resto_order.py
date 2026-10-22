from odoo import _, api, fields, models
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

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders:
            if order.table_id.state == "occupied":
                raise UserError(
                    _("Table %s already has an open order.", order.table_id.name)
                )
            order.table_id.state = "occupied"
        return orders

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
