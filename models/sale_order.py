# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, _
from odoo.addons.sale_stock.models.sale_order import SaleOrder


class sale_order(models.Model):
    _inherit = 'sale.order'

    # def action_confirm(self):
    #     res = super(sale_order, self).action_confirm()
    #     for order in self:
    #         if order.pricelist_id:
    #             for lines in order.order_line.filtered(lambda l: l.price_unit > 0.00):
    #                 pricelist_item = order.pricelist_id.item_ids.filtered(lambda
    #                                                                           l: l.compute_price == 'fixed' and l.applied_on == '1_product' and l.uom_id.id == lines.product_uom.id)
    #                 if pricelist_item:
    #                     each_price = order.pricelist_id.item_ids.search(
    #                         [('product_tmpl_id', '=', lines.product_id.product_tmpl_id.id),
    #                          ('compute_price', '=', 'fixed'), ('applied_on', '=', '1_product'),
    #                          ('pricelist_id', '=', order.pricelist_id.id), ('uom_id', '=', lines.product_uom.id)])
    #                     if not each_price:
    #                         order.pricelist_id.write({'item_ids': [(0, 0, {'applied_on': '1_product',
    #                                                                        'product_tmpl_id': lines.product_id.product_tmpl_id.id,
    #                                                                        'uom_id': lines.product_uom.id,
    #                                                                        'fixed_price': lines.price_unit})]})
    #                     else:
    #                         each_price.fixed_price = lines.price_unit
    #                 else:
    #                     order.pricelist_id.write({'item_ids': [(0, 0, {'applied_on': '1_product',
    #                                                                    'product_tmpl_id': lines.product_id.product_tmpl_id.id,
    #                                                                    'uom_id': lines.product_uom.id,
    #                                                                    'fixed_price': lines.price_unit
    #                                                                    })]})
    #     return res
