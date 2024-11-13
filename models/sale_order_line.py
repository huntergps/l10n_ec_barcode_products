# -*- coding: UTF-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # barcode_uom_id = fields.Many2one('uom.uom', string='Barcode UoM')

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     # Llamar al método original para mantener la funcionalidad estándar
    #     print(self.barcode_uom_id)
        # if self.product_id:
        #     if self.barcode_uom_id:
        #         # Si barcode_uom_id está definido, asignarlo a product_uom_id
        #         self.product_uom = self.barcode_uom_id
        #     else:
        #         # De lo contrario, asignar la unidad de medida estándar del producto
        #         self.product_uom = self.product_id.uom_id


    # @api.onchange('product_id')
    # def onchange_product_id(self):
    #     if not self.product_id:
    #         return
    #     self._product_id_change()
    #
    # def _product_id_change(self):
    #     if not self.product_id:
    #         return
    #     if self.env.context.get('l10n_ec_barcode'):
    #         self.product_uom = self.product_id.uom_id.id
