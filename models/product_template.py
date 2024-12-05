# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_barcode = fields.One2many('product.barcode', 'product_tmpl_id',string='Codigos de Barra del Producto')
    company_barcode_id = fields.Many2one('res.company', 'company', default=lambda self: self.env.user.company_id)

    pricelist_items = fields.One2many('product.pricelist.item','product_tmpl_id', string="PVP de Venta",copy=False)



    pricelist_item_ids = fields.Many2many(
        comodel_name='product.pricelist.item',
        string="Precios de Venta",
        compute='_compute_item_count',
        copy=False)

    def open_pricelist_rules(self):
        self.ensure_one()
        domain = ['|',
            ('product_tmpl_id', '=', self.id),
            ('product_id', 'in', self.product_variant_ids.ids),
        ]
        return {
            'name': _('Price Rules'),
            'view_mode': 'list,form',
            'views': [(self.env.ref('product.product_pricelist_item_tree_view_from_product').id, 'list')],
            'res_model': 'product.pricelist.item',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
            'context': {
                'default_product_tmpl_id': self.id,
                'default_applied_on': '1_product',
                'product_without_variants': self.product_variant_count == 1,
                'search_default_visible': True,
            },
        }

    def _compute_item_count(self):
        for template in self:
            pricelist_item_ids = template.env['product.pricelist.item'].search([
                '&',
                '|', ('product_tmpl_id', '=', template.id), ('product_id', 'in', template.product_variant_ids.ids),
                ('pricelist_id.active', '=', True),
            ])
            template.pricelist_item_ids = pricelist_item_ids
            template.pricelist_item_count = len(pricelist_item_ids)



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
