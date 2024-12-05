# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _



class Barcode(models.Model):
    _name = 'product.barcode'
    _description = "Product Barcode"


    @tools.ormcache()
    def _get_default_uom_id(self):
        print("self.env.context.get('default_product_uom') =", self.env.context.get('default_product_uom'))

        # Verifica si existe un UoM predeterminado en el contexto
        if self.env.context.get('default_product_uom'):
            return self.env.context.get('default_product_uom')

        # Devuelve la unidad de medida del producto, si está disponible
        if self.product_id:
            return self.product_id.uom_id.id

        # Si no se encuentra nada, devuelve la unidad de medida predeterminada de Odoo
        return False

    product_id = fields.Many2one('product.product', related='product_tmpl_id.product_variant_id')
    barcode = fields.Char(string='Barcode',required=True)
    product_tmpl_id = fields.Many2one('product.template')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    product_uom = fields.Many2one(
        'uom.uom', 'Unidad de Medida',
        default=_get_default_uom_id, required=True)
    uom_name = fields.Char(string='Nombre de Unidad de Medida', related='product_uom.name', readonly=True)

    uom_ids_allowed = fields.Many2many('uom.uom', compute='_compute_uom_ids_allowed', string='UdM Permitidos', store=True)

    @api.depends('product_id')
    def _compute_uom_ids_allowed(self):
        for line in self:
            if line.product_id:
                uom_records = line.product_id.sale_uom_ids
                if line.product_id.uom_id not in uom_records:
                    uom_records |= line.product_id.uom_id
                line.uom_ids_allowed = uom_records



    _sql_constraints = [
        ('uniq_barcode', 'unique(barcode)', "Un código de barras solo se puede asignar a un producto!"),
    ]
