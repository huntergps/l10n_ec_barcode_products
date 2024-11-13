# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_barcode = fields.One2many('product.barcode', 'product_tmpl_id',string='Codigos de Barra del Producto')
    company_barcode_id = fields.Many2one('res.company', 'company', default=lambda self: self.env.user.company_id)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        products = super(ProductTemplate, self).name_search(name=name, args=args, operator=operator, limit=limit)
        if name:
            barcodes = self.env['product.barcode'].sudo().search([('barcode', operator, name)])
            if barcodes:
                barcode_products = barcodes.mapped('product_tmpl_id')
                if barcode_products:
                    barcode_results = [
                        (
                            product.id,
                            f"[{product.default_code}] {product.name} {barcode.product_uom.name} ({barcode.barcode})",
                            {
                                'barcode_uom_id': [barcode.product_uom.id, barcode.product_uom.name]
                            }
                        )
                        for product, barcode in zip(barcode_products, barcodes)
                    ]
                    return barcode_results + products
        return products


class ProductInherit(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        products = super(ProductInherit, self).name_search(name=name, args=args, operator=operator, limit=limit)
        if name:
            barcodes = self.env['product.barcode'].sudo().search([('barcode', operator, name)])
            if barcodes:
                barcode_products = barcodes.mapped('product_tmpl_id')
                if barcode_products:
                    barcode_results = [
                        (
                            product.id,
                            f"[{product.default_code}] {product.name} {barcode.product_uom.name} ({barcode.barcode})",
                            {
                                'barcode_uom_id': [barcode.product_uom.id, barcode.product_uom.name]
                            }
                        )
                        for product, barcode in zip(barcode_products, barcodes)
                    ]
                    return barcode_results + products
        return products
