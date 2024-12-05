# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import ValidationError
from odoo import api, fields, models, tools, _

class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(
            self, products, quantity, currency=None, uom=None, date=False, compute_price=True, **kwargs):
        """Sobrescribe el método para considerar la UOM en el cálculo del precio."""
        self.ensure_one()
        currency = currency or self.currency_id or self.env.company.currency_id
        currency.ensure_one()

        if not products:
            return {}

        if not date:
            date = fields.Datetime.now()

        # Obtiene todas las reglas potencialmente aplicables considerando la UOM
        rules = self._get_applicable_rules(products, date, uom=uom, **kwargs)

        results = {}
        for product in products:
            suitable_rule = self.env['product.pricelist.item']

            product_uom = product.uom_id
            target_uom = uom or product_uom  # Si no se especifica UOM, usar la del producto

            # Calcula la cantidad en UOM del producto
            if target_uom != product_uom:
                qty_in_product_uom = target_uom._compute_quantity(
                    quantity, product_uom, raise_if_failure=False
                )
            else:
                qty_in_product_uom = quantity

            for rule in rules:
                if rule._is_applicable_for(product, qty_in_product_uom, uom=target_uom):
                    suitable_rule = rule
                    break

            if compute_price:
                price = suitable_rule._compute_price(
                    product, quantity, target_uom, date=date, currency=currency)
            else:
                # Omite el cálculo de precio si solo se requiere la regla
                price = 0.0
            results[product.id] = (price, suitable_rule.id)

        return results

    def _get_applicable_rules_domain(self, products, date, uom=None, **kwargs):
        """Extiende el dominio para incluir 'uom_id'."""
        domain = super()._get_applicable_rules_domain(products, date, **kwargs)

        if uom:
            domain += ['|', ('uom_id', '=', False), ('uom_id', '=', uom.id)]
        else:
            domain += [('uom_id', '=', False)]

        return domain


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    uom_id = fields.Many2one('uom.uom', 'Unidad de Medida')
    uom_ids_allowed = fields.Many2many('uom.uom', compute='_compute_uom_ids_allowed', string='UdM Permitidos')

    @api.depends('product_id',"product_tmpl_id")
    def _compute_uom_ids_allowed(self):
        for item in self:
            if item.product_tmpl_id:
                uom_records = item.product_tmpl_id.sale_uom_ids
                if item.product_tmpl_id.uom_id not in uom_records:
                    uom_records = uom_records | item.product_tmpl_id.uom_id
                item.uom_ids_allowed = uom_records
            else:
                item.uom_ids_allowed = self.env['uom.uom']

    @api.onchange('product_id',"product_tmpl_id")
    def _compute_uom_ids_allowed_onchange(self):
        self._compute_uom_ids_allowed()


    def _is_applicable_for(self, product, qty_in_product_uom, uom=None):
        res = super()._is_applicable_for(product, qty_in_product_uom)

        if not res:
            return False

        if self.uom_id:
            if uom:
                if self.uom_id != uom:
                    return False
            else:
                if self.uom_id != product.uom_id:
                    return False

        return True
    #
    #
    # def _compute_price(self, product, quantity, uom, date, currency=None):
    #     """
    #     Sobrescribe el cálculo de precios para verificar si aplica a un producto y una unidad de medida específica.
    #     """
    #     if self:
    #         self.ensure_one()
    #         product.ensure_one()
    #         uom.ensure_one()
    #
    #     # Verificar si la regla aplica al producto específico y su unidad de medida
    #     if (self.product_id and self.product_id != product) or (self.product_tmpl_id and self.product_tmpl_id != product.product_tmpl_id) or (self.uom_id and self.uom_id != uom):
    #         # Si no aplica, usar la lógica original
    #         print("ES ANTERIOR ORGINAL!!!!!!")
    #         myprice = super()._compute_price(product, quantity, uom, date, currency)
    #         print(" myprice : ",myprice )
    #         return myprice
    #
    #     print("PASSOOOO!!!!!!")
    #     # Continuar con la lógica personalizada si coincide el producto y la unidad de medida
    #     currency = currency or self.currency_id or self.env.company.currency_id
    #     currency.ensure_one()
    #
    #     product_uom = product.uom_id
    #     convert = lambda p: product_uom._compute_price(p, uom) if product_uom != uom else p
    #
    #     if self.compute_price == 'fixed':
    #         return convert(self.fixed_price)
    #     elif self.compute_price == 'percentage':
    #         base_price = self._compute_base_price(product, quantity, uom, date, currency)
    #         return base_price - (base_price * (self.percent_price / 100))
    #     elif self.compute_price == 'formula':
    #         base_price = self._compute_base_price(product, quantity, uom, date, currency)
    #         print("base_price >> ",base_price)
    #         price_limit = base_price
    #         price = base_price - (base_price * (self.price_discount / 100))
    #         print("price >> ",price)
    #         if self.price_round:
    #             price = tools.float_round(price, precision_rounding=self.price_round)
    #         if self.price_surcharge:
    #             price += convert(self.price_surcharge)
    #         if self.price_min_margin:
    #             price = max(price, price_limit + convert(self.price_min_margin))
    #         if self.price_max_margin:
    #             price = min(price, price_limit + convert(self.price_max_margin))
    #         return price
    #     else:
    #         myprice= self._compute_base_price(product, quantity, uom, date, currency)
    #         print(" myprice : ",myprice )
    #         return myprice
    #
    #
    # def _compute_price1(self, product, quantity, uom, date, currency=None):
    #     """
    #     Override to include unit of measure in price calculation.
    #     """
    #     if self:
    #         self.ensure_one()
    #         product.ensure_one()
    #         uom.ensure_one()
    #         currency = currency or self.currency_id or self.env.company.currency_id
    #         currency.ensure_one()
    #     if self.uom_id and self.uom_id == uom and self.product_tmpl_id == product.product_tmpl_id:
    #         print(self.uom_id)
    #         print(uom)
    #         print(product)
    #         print(self.product_id)
    #         print(self.product_tmpl_id)
    #         product_uom = self.uom_id
    #         if product_uom != uom:
    #             convert = lambda p: product_uom._compute_price(p, uom)
    #         else:
    #             convert = lambda p: p
    #         print('self.compute_price = ',self.compute_price)
    #         if self.compute_price == 'fixed':
    #             if uom.id == self.uom_id.id:
    #                 price = convert(self.fixed_price)
    #             else:
    #                 price = self._compute_base_price(product, quantity, uom, date, currency)
    #         elif self.compute_price == 'percentage':
    #             if uom.id == self.uom_id.id:
    #                 base_price = self._compute_base_price(product, quantity, uom, date, currency)
    #                 price = (base_price - (base_price * (self.percent_price / 100))) or 0.0
    #             else:
    #                 price = self._compute_base_price(product, quantity, uom, date, currency)
    #         elif self.compute_price == 'formula':
    #             if uom.id == self.uom_id.id:
    #                 base_price = self._compute_base_price(product, quantity, uom, date, currency)
    #                 price_limit = base_price
    #                 price = (base_price - (base_price * (self.price_discount / 100))) or 0.0
    #                 if self.price_round:
    #                     price = tools.float_round(price, precision_rounding=self.price_round)
    #                 if self.price_surcharge:
    #                     price += convert(self.price_surcharge)
    #                 if self.price_min_margin:
    #                     price = max(price, price_limit + convert(self.price_min_margin))
    #                 if self.price_max_margin:
    #                     price = min(price, price_limit + convert(self.price_max_margin))
    #             else:
    #                 price = self._compute_base_price(product, quantity, uom, date, currency)
    #
    #         else:  # empty self, or extended pricelist price computation logic
    #             price = self._compute_base_price(product, quantity, uom, date, currency)
    #         return price
    #     else:
    #         price = super(ProductPricelistItem, self)._compute_price(product, quantity, uom, date, currency)
    #         print("my price -= ",price)
    #         return price
