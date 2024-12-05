/** @odoo-module **/

import { useState,useRef, onWillUnmount } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { SaleOrderLineProductField } from '@sale/js/sale_product_field';
import { ProductLabelSectionAndNoteFieldAutocomplete } from "@account/components/product_label_section_and_note_field/product_label_section_and_note_field";


export const codabarService = {
    // Si tu servicio depende de otros servicios, puedes especificarlos aquí
    dependencies: [],

    // Si tienes métodos asíncronos que quieres inicializar, puedes listarlos aquí
    async: [],

    start(env) {
        // Aquí puedes inicializar tu servicio
        let codabar_uom = null;
        let listeners = [];

        return {
            setCodabarUom(value) {
                codabar_uom = value;
                console.log('setCodabarUom codabar_uom = ',value);
                this.notifyListeners();
            },
            getCodabarUom() {
                return codabar_uom;
            },
            addListener(callback) {
                if (typeof callback === 'function') {
                    listeners.push(callback);
                }
            },
            removeListener(callback) {
                listeners = listeners.filter((listener) => listener !== callback);
            },
            notifyListeners() {
                listeners.forEach((callback) => callback(codabar_uom));
            },
        };
    },
};

registry.category('services').add('codabarService', codabarService);


export class ProductLabelSectionAndNoteFieldAutocompleteCodBar extends ProductLabelSectionAndNoteFieldAutocomplete {
    setup() {
        super.setup();
        this.codabarService = useService('codabarService');
    }

    mapRecordToOption(result) {
        const [id, displayName, extraData] = result;
        return {
            value: id,
            label: displayName ? displayName.split("\n")[0] : _t("Sin nombre"),
            displayName: displayName,
            codabar_uom: extraData ? extraData.barcode_uom_id : null,
            classList: this.props.getOptionClassnames({ id, display_name: displayName }),
        };
    }

    onSelect(option, params = {}) {
        if (option.action) {
            return option.action(params);
        }
        const record = {
            id: option.value,
            display_name: option.displayName,
        };
        this.props.update([record], params);
        // Actualizar el servicio con el valor de codabar_uom
        if (option.codabar_uom) {
            this.codabarService.setCodabarUom(option.codabar_uom);
        }

    }



}



export class CustomSaleOrderLineProductField extends SaleOrderLineProductField {
    static components = {
        ...SaleOrderLineProductField.components,
        Many2XAutocomplete: ProductLabelSectionAndNoteFieldAutocompleteCodBar,
    };

    setup() {
        super.setup();
        this.orm = useService('orm');
        this.codabarService = useService('codabarService');
        this.codabar_uom = null;

        this.updateCodabarUom = (codabar_uom) => {
            this.codabar_uom = codabar_uom;
        };

        this.codabarService.addListener(this.updateCodabarUom);

        onWillUnmount(() => {
            this.codabarService.removeListener(this.updateCodabarUom);
        });
    }

    async _onProductTemplateUpdate() {
        await super._onProductTemplateUpdate(...arguments);
        const codabar_uom = this.codabar_uom;
        if (codabar_uom) {
            await this.props.record.update({
                product_uom_id: codabar_uom,
            });
            this.codabar_uom = null;
        }
    }

}

// Registrar el componente
registry.category("fields").add("custom_sale_order_line_product_field", {
    component: CustomSaleOrderLineProductField,
});
