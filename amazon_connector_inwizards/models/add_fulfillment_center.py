from odoo import _, api, exceptions, fields, models
from ...amazon_connector_inwizards import const

class AddAmazonFulfillmentCenter(models.TransientModel):
    _name = "add.amazon.fulfillment.center"
    
    store_inventory_country_list = [("czech_republic", "Czech Republic"), ("Amazon.fr", "France"), ("Amazon.de", "Germany"), ("Amazon.it", "Italy"), ("Amazon.pl", "Poland"), ("Amazon.es", "Spain")]
    
    seller_id = fields.Many2one('amazon.seller.ept', string='Seller')
    amazon_program = fields.Selection([("pan_eu", "PAN EU"), ("efn", "EFN"), ("mci","MCI"), ("cep", "CEP"), ("efn_mci", "EFN + MCI")])
    amazon_usa_program = fields.Selection([("narf", "NARF")])
    is_european_region = fields.Boolean()
    is_north_america_region = fields.Boolean()
    
    # European Marketplace
    amazon_fr = fields.Boolean(string="Amazon.fr")    
    amazon_nl = fields.Boolean(string="Amazon.nl")
    amazon_pl = fields.Boolean(string="Amazon.pl")
    amazon_de = fields.Boolean(string="Amazon.de")
    amazon_es = fields.Boolean(string="Amazon.es")
    amazon_se = fields.Boolean(string="Amazon.se")
    amazon_com_tr = fields.Boolean(string="Amazon.com.tr")
    amazon_it = fields.Boolean(string="Amazon.it")
    
    # American Marketplace
    amazon_com_mx = fields.Boolean("Amazon.com.mx")
    amazon_ca = fields.Boolean("Amazon.ca")
    amazon_com = fields.Boolean("Amazon.com")
    
    #Fulfillment Center
    amazon_fr_inv = fields.Boolean(string="France")    
    amazon_pl_inv = fields.Boolean(string="Poland")
    amazon_de_inv = fields.Boolean(string="Germany")
    amazon_es_inv = fields.Boolean(string="Spain")
    amazon_com_tr_inv = fields.Boolean(string="Turkey")
    czech_republic_inv = fields.Boolean(string="Czech Republic")
    amazon_it_inv = fields.Boolean(string="Italy")
    
    amazon_uk = fields.Boolean(string="Amazon.co.uk")
    czech_republic = fields.Boolean()
    store_inventory_country = fields.Selection(
        string='Store Inventory Country',
        selection=store_inventory_country_list
    )
    
    def attach_marketplace_with_seller(self, base_marketplace_id,  seller_id):
        code = base_marketplace_id.name.split(".")[-1].upper()
        country_id = self.env["res.country"].search([("amazon_marketplace_code", "=", code)])
        
        seller_id.marketplace_ids = [(0,0, {
            "name": f'{base_marketplace_id.name} ({seller_id.name})',
            "seller_id": seller_id.id,
            "country_id": country_id.id,
            "currency_id": country_id.currency_id.id,
            "market_place_id": base_marketplace_id.api_ref
        })]
    
    @api.onchange("seller_id")
    def onchange_seller_id(self):
        self.is_european_region = self.seller_id.is_european_region
        self.is_north_america_region = self.seller_id.is_north_america_region
    

    @api.onchange("amazon_program")
    def onchange_amazon_program(self):
        if self.amazon_program == "pan_eu":
            self.amazon_fr = True
            self.amazon_nl = True
            self.amazon_pl = True
            self.amazon_de = True
            self.amazon_es = True
            self.amazon_se = True
            self.amazon_com_tr = True
            self.amazon_it = True
        else:
            self.amazon_fr = False
            self.amazon_nl = False
            self.amazon_pl = False
            self.amazon_de = False
            self.amazon_es = False
            self.amazon_se = False
            self.amazon_com_tr = False
            self.amazon_it = False
            
    
    def _create_marketplace(self, base_marketplace_id, warehouse_id, fba_warehouse_ids=None):
        country_name = const.MARKETPLACE_COUNTRY[base_marketplace_id.name.split(".")[-1]]
        country_id = self.env["res.country"].search([("name", "=", country_name)])
        self.env["amazon.instance.ept"].create({
            "name": base_marketplace_id.name,
            "api_ref" : base_marketplace_id.api_ref,
            "seller_central_url" : base_marketplace_id.seller_central_url,
            "region" : base_marketplace_id.region,
            "country_id": country_id.id if country_id else False,
            "company_id":self.env.company.id,
            "warehouse_id":warehouse_id.id if warehouse_id else warehouse_id,
            "stock_update_warehouse_ids": [(6, 0, fba_warehouse_ids)] if fba_warehouse_ids else fba_warehouse_ids,
            "fba_warehouse_id":warehouse_id.id if warehouse_id else warehouse_id,
            "seller_id": self.seller_id.id,
            "amazon_retail_marketplace_id": base_marketplace_id.id,
            "merchant_id": self.seller_id.merchant_id
        })
        
        self.attach_marketplace_with_seller(base_marketplace_id,  self.seller_id)
    
    
    def create_marketplace(self):
        if self.is_european_region:
            warehouse_obj = self.env["stock.warehouse"]
            self._create_warehouses_and_marketplaces(warehouse_obj)
        elif self.is_north_america_region:
            warehouse_obj = self.env["stock.warehouse"]
            self._create_warehouses_and_marketplaces_for_us(warehouse_obj)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Account',
            'view_mode': 'form',
            'context': {'default_seller_id': self.seller_id.id},
            'res_model': 'amazon.info.account',
            'target' : 'new'
        }
            
    def _create_warehouses_and_marketplaces_for_us(self, warehouse_obj):
        if self.amazon_usa_program:
            self._create_usa_warehouse("amazon_us")
        else:
            self._create_usa_warehouse(None)
            
            
    def _create_usa_warehouse(self, warehouse):
        if warehouse == "amazon_us":
            warehouse_id = self.env["stock.warehouse"].create({
                "name" : f"FBA Amazon.us ({self.seller_id.name})",
                "code": "us",
                "company_id": self.env.company.id,
                "seller_id": self.seller_id.id,
                "fulfillment_center_ids": [(0, 0, {'center_code': code, "seller_id": self.seller_id.id}) for code in const.us_fulfillment_center_code["Amazon.com"]],
                "is_fba_warehouse": True
            })
            
            for marketplace in const.us_marketplace_inv:
                base_market_place_id = self.env["amazon.retail.marketplace"].search([("name", "=", marketplace)])
                self._create_marketplace(base_market_place_id, warehouse_id)
        else:
            selected_us_marketplace = {
                'Amazon.com': self.amazon_com,
                'Amazon.ca': self.amazon_ca,
                'Amazon.com.mx': self.amazon_com_mx, 
            }
            
            for market, is_enabled in selected_us_marketplace.items():
                if is_enabled:
                    warehouse_id = self.env["stock.warehouse"].create({
                        "name" : f"FBA {market} ({self.seller_id.name})",
                        "code": market.split(".")[-1],
                        "company_id": self.env.company.id,
                        "seller_id": self.seller_id.id,
                        "fulfillment_center_ids": None if market != 'Amazon.ca' else [(0, 0, {'center_code': code, "seller_id": self.seller_id.id}) for code in const.us_fulfillment_center_code[market]],
                        "is_fba_warehouse": True
                    })
                    base_market_place_id = self.env["amazon.retail.marketplace"].search([("name", "=", market)])
                    self._create_marketplace(base_market_place_id, warehouse_id)
                    
                    
    def _create_warehouses_and_marketplaces(self, warehouse_obj):
        if self.amazon_program == "pan_eu":
            self._create_pan_eu_marketplaces(warehouse_obj)
        elif self.amazon_program == "efn":
            self._create_efn_marketplaces(warehouse_obj)
        elif self.amazon_program == "cep":
            self._create_cep_marketplaces(warehouse_obj)
        elif self.amazon_program in ["mci", "efn_mci"]:
            self._create_mci_efn_mci_marketplaces(warehouse_obj)

    def _create_pan_eu_marketplaces(self, warehouse_obj):
        for center in const.pen_eu_fulfillment_center:
            if center not in ["Amazon.nl", "Amazon.se"]:
                warehouse_id = self._create_warehouse(warehouse_obj, center)
                base_marketplace_id = self._get_marketplace_id(center)
                self._create_marketplace(base_marketplace_id, warehouse_id)
            else:
                base_marketplace_id = self._get_marketplace_id(center)
                warehouse_id = warehouse_obj.search([('code', '=', 'de')])
                self._create_marketplace(base_marketplace_id, warehouse_id)
                
        if self.amazon_uk:
            self._create_amazon_uk_marketplace(warehouse_obj)

        # if self.czech_republic:
        #     self._create_czech_republic_marketplace(warehouse_obj)

    def _create_efn_marketplaces(self, warehouse_obj):
        warehouse_id = self._create_warehouse(warehouse_obj, self.store_inventory_country)
        amazon_markets = self._get_amazon_markets()
        
        for market, is_enabled in amazon_markets.items():
            if is_enabled:
                base_marketplace_id = self._get_marketplace_id(market)
                self._create_marketplace(base_marketplace_id, warehouse_id)

    def _create_cep_marketplaces(self, warehouse_obj):
        fba_warehouse_ids = [self._create_warehouse(warehouse_obj, center).id for center in const.CEP]
        amazon_markets = self._get_amazon_markets()

        for market, is_enabled in amazon_markets.items():
            if is_enabled:
                base_marketplace_id = self._get_marketplace_id(market)
                self._create_marketplace(base_marketplace_id, None, fba_warehouse_ids)

    def _create_mci_efn_mci_marketplaces(self, warehouse_obj):
        fba_warehouse_ids = [
            self._create_warehouse(warehouse_obj, warehouse).id
            for warehouse, is_enabled in self._get_amazon_fulfillment_centers().items()
            if is_enabled
        ]
        amazon_markets = self._get_amazon_markets()

        for market, is_enabled in amazon_markets.items():
            if is_enabled:
                base_marketplace_id = self._get_marketplace_id(market)
                if market == "Amazon.co.uk":
                    warehouse_id = warehouse_obj.search([('code', '=', 'uk')]) or self._create_warehouse(warehouse_obj, market)
                    self._create_marketplace(base_marketplace_id, warehouse_id)
                else:
                    self._create_marketplace(base_marketplace_id, None, fba_warehouse_ids)

    def _create_warehouse(self, warehouse_obj, center):
        center_code = const.fulfillment_center_code.get(center, [])
        return warehouse_obj.create({
            "name": f'FBA {center} ({self.seller_id.name})',
            "code": "crz" if center == 'czech_republic' else center.split(".")[1],
            "company_id": self.env.company.id,
            "seller_id": self.seller_id.id,
            "fulfillment_center_ids": [(0, 0, {'center_code': code, "seller_id": self.seller_id.id}) for code in center_code],
            "is_fba_warehouse": True
        })

    def _create_amazon_uk_marketplace(self, warehouse_obj):
        warehouse_id = self._create_warehouse(warehouse_obj, "Amazon.uk")
        base_marketplace_id = self._get_marketplace_id("Amazon.co.uk")
        self._create_marketplace(base_marketplace_id, warehouse_id)

    # def _create_czech_republic_marketplace(self, warehouse_obj):
    #     warehouse_id = self._create_warehouse(warehouse_obj, "czech_republic")
    #     self.env["amazon.instance.ept"].create({
    #         "name": "Czech Republic",
    #         "company_id": self.env.company.id,
    #         "warehouse_id": warehouse_id.id,
    #         "fba_warehouse_id": warehouse_id.id,
    #         "seller_id": self.seller_id.id,
    #     })
       
    #     country_id = self.env["res.country"].search([("code", "=", "CZ")])
    #     self.seller_id.marketplace_ids = [(0,0, {
    #         "name": f'Czech Republic ({self.seller_id.name})',
    #         "seller_id": self.seller_id.id,
    #         "country_id": country_id.id,
    #         "currency_id": country_id.currency_id.id
    #     })]
        

       

    def _get_marketplace_id(self, center):
        return self.env["amazon.retail.marketplace"].search([("name", "=", center.strip())])

    def _get_amazon_markets(self):
        return {
            'Amazon.fr': self.amazon_fr,
            'Amazon.nl': self.amazon_nl,
            'Amazon.pl': self.amazon_pl,
            'Amazon.de': self.amazon_de,
            'Amazon.es': self.amazon_es,
            'Amazon.se': self.amazon_se,
            'Amazon.com.tr': self.amazon_com_tr,
            'Amazon.it': self.amazon_it,
            'Amazon.co.uk': self.amazon_uk
        }

    def _get_amazon_fulfillment_centers(self):
        return {
            'Amazon.fr': self.amazon_fr_inv,
            'Amazon.pl': self.amazon_pl_inv,
            'Amazon.de': self.amazon_de_inv,
            'Amazon.es': self.amazon_es_inv,
            'Amazon.com.tr': self.amazon_com_tr_inv,
            'Amazon.it': self.amazon_it_inv,
            'czech_republic': self.czech_republic_inv
        }

                        