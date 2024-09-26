# -*- coding: utf-8 -*-
{
    'name': "Amazon Connector",
    'summary': "Connect odoo with amazon",
    'description': """
        This module enables seamless integration between Amazon Seller Central and Odoo, allowing Amazon sellers to manage their orders, inventory, and shipments directly from Odoo.
        Key Feature :-
            Import Amazon orders (FBA and FBM) into Odoo automatically.
            Synchronize inventory levels between Odoo and Amazon.
            Track order fulfillment statuses and manage shipping information.
            Automate invoice generation for Amazon orders.
            Supports multiple Amazon marketplace accounts.
            Real-time stock updates from Odoo to Amazon.
            Manage both FBA and FBM orders from a single interface in Odoo.
    """,
    'category': 'Sale',
    'author': 'Inwizards Technology Pvt Ltd',
    'price' : '450',
    'currency' : 'EUR', 
    'maintainer' : '',
    'website': 'https://www.inwizards.com/',  
    "license": "AGPL-3",
    'depends': ['base', 'sale', 'stock', 'board', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/amazon_data.xml',
        'data/auto_increament_sequence.xml',
        'data/default_amazon_transaction_type.xml',
        'data/country_code_update.xml',
        
        'views/subscription.xml',
        'views/dashboard.xml',
        'views/views.xml',
        'views/setting.xml',
        'views/templates.xml',
        'views/add_amazon_product.xml',
        'views/product.xml',
        'views/rating.xml',
        'views/fbm.xml',
        'views/fba.xml',
        'views/logs.xml',
        'views/feed_submission_history.xml',
        'views/fba_customer_return_report.xml',
        'views/fba_inbound_shippment_plans.xml',
        'views/fba_inbound_shipments.xml',
        'views/fba_removal_orders.xml',
        'views/fba_amazon_removal_order_report_history.xml',
        'views/fba_amazon_fba_live_stock_report_ept.xml',
        'views/fba_amazon_stock_adjustment_report_history.xml',
        'views/operation_fba_dbm.xml',
        'views/seller.xml',
        'views/marketplace.xml',
        'views/auto_sale_workflow.xml',
        'views/amazon_stock_adjustment_config.xml',
        'views/removal_order_config_ept.xml',
        'views/add_fulfillment_center.xml',
        'views/stock_warehouse.xml',
        'views/marketplace_settings.xml',
        'views/sale.xml', 
        'views/pricelist.xml',
        'views/account_chart.xml',
        'views/settlement_report.xml',
        'views/product_sku.xml',
        'views/marketplace_list.xml',
        'views/menuitem.xml',
        'views/fbm_cron_configuration_wizard_view.xml',
        'views/fba_cron_configuration_wizard_view.xml',
        'views/global_cron_job.xml',
        'data/service.xml',
        
    ],
    'assets': {
        'web.assets_backend': [
            '/amazon_connector_inwizards/static/src/components/amazon_dashboard.js',
            '/amazon_connector_inwizards/static/src/components/amazon_dashboard.xml',
            '/amazon_connector_inwizards/static/src/components/custom.css',
            'amazon_connector_inwizards/static/src/components/amazon_dashboard.js',
            'amazon_connector_inwizards/static/src/components/amazon_dashboard.xml',           
        ],
    },
    
    "images" : ['static/description/banner.gif'],
        
}











