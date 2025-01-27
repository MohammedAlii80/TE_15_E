odoo.define('account_avatax_sale.tour_account_avatax_sale_optional_products', function (require) {
'use strict';

var tour = require('web_tour.tour');

// This tour relies on data created on the Python test.
tour.register('account_avatax_sale_optional_products', {
    test: true,
    url: '/my/quotes',
},
[
    {
        content: "open the test SO",
        trigger: 'a:containsExact("avatax test")',
    },
    {
        content: "add the optional product",
        trigger: '.js_add_optional_products',
    },
    {
        content: "increase the quantity of the optional product by 1",
        extra_trigger: 'li a:contains("Pricing")',
        trigger: '.js_update_line_json:nth(1)',
    },
    {
        content: "wait for the quantity to be updated",
        extra_trigger: 'input.js_quantity[value="2.0"]',
        trigger: 'li a:contains("Pricing")',
        auto: true,
    },
    {
        content: "delete the optional line",
        trigger: '.js_update_line_json:nth(2)',
    },
    {
        content: "wait for line to be deleted and show up again in optional products",
        trigger: '.js_add_optional_products',
        auto: true,
    },
]);
});

