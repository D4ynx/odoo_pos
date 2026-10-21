from odoo import _, fields, models
from odoo.exceptions import UserError


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

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
        ],
        string="Status",
        required=True,
        default="draft",
    )

    def action_confirm(self):
        for purchase in self:
            if purchase.state != "draft":
                raise UserError(_("Only draft purchases can be confirmed."))
            for line in purchase.line_ids:
                self.env["resto.stock.lot"].create(
                    {
                        "ingredient_id": line.ingredient_id.id,
                        "date": purchase.date,
                        "qty": line.qty,
                        "remaining_qty": line.qty,
                        "unit_cost": line.price_unit,
                        "currency_id": purchase.currency_id.id,
                    }
                )
            purchase.state = "confirmed"
