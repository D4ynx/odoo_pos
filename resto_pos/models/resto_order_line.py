from odoo import api, fields, models


class RestoOrderLine(models.Model):
    _name = "resto.order.line"
    _description = "Resto Order Line"

    order_id = fields.Many2one(
        "resto.order",
        string="Order",
        required=True,
        ondelete="cascade",
    )

    menu_item_id = fields.Many2one(
        "resto.menu.item",
        string="Dish",
        required=True,
        ondelete="restrict",
    )

    qty = fields.Integer(string="Quantity", required=True, default=1)

    currency_id = fields.Many2one(
        related="order_id.currency_id",
    )

    price_unit = fields.Monetary(
        string="Unit Price", currency_field="currency_id", required=True
    )

    subtotal = fields.Monetary(
        string="Subtotal",
        currency_field="currency_id",
        compute="_compute_subtotal",
    )

    @api.onchange("menu_item_id")
    def _onchange_menu_item_id(self):
        for line in self:
            line.price_unit = line.menu_item_id.price

    @api.depends("qty", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.price_unit
