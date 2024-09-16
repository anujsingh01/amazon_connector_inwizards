from odoo import _, api, exceptions, fields, models
import requests
import json
import time
from io import StringIO,BytesIO
import base64
import csv
from datetime import datetime 
import http.client
import json
from odoo.exceptions import UserError
import random
import pandas as pd
# from amazon_connector_inwizards import amazon_api
from ...amazon_connector_inwizards import amazon_api
import base64
import os
from werkzeug.urls import url_encode, url_join, url_parse
from ...amazon_connector_inwizards import utils



class OperationsFBAFBM(models.TransientModel):
    _name = "amazon.process.import.export"
    

    amazon_program = fields.Selection(
        [],
        string='Amazon Program',
        readonly=True
    )
    
    amazon_selling = fields.Selection(
       [ ('FBM', 'FBM'),('FBA', 'FBA'),('Both', 'FBA & FBM')],
        string='Fulfillment By',
        readonly=True,
        default = 'Both'
    )
    
    amz_video_url = fields.Html(
        string='Amz Video Url',
        readonly=True
    )
    
    auto_create_product = fields.Boolean(
        string='Auto create product?',
        readonly=False,
        store=True
    )
    
    both_operations = fields.Selection(
        selection=[
            ('amz_import_products', 'Map Products'),
            ('amz_sync_active_products', 'Import Products'),
            ('amz_export_price_from_odoo_to_amazon', 'Export Prices'),
            ('amz_list_settlement_report', 'Download Settlement Reports'),
            ('amz_request_rating_report', 'Import Rating Report'),
            ('amz_vcs_tax_report', 'Import VCS(VAT Calculation Service) Report'),
            ('amz_manually_create_settlement_report', 'Manually Create Settlement Report'),
        ],
        string='FBM & FBA Operations',
        readonly=False,
        store=True
    )
    
    check_order_status = fields.Boolean(
        string='Check Order Status',
        readonly=False,
        store=True
    )
    
    choose_file = fields.Binary(
        string='Choose File',
        readonly=False,
        store=True
    )
    
    country_code = fields.Char(
        string='Country Code',
        readonly=False,
        store=True
    )
    
    create_date = fields.Datetime(
        string='Create Date',
        readonly=True
    )
    
    create_uid = fields.Many2one(
        'res.users', string='Created by',
        readonly=True
    )
    
    delimiter = fields.Selection([("tab", "Tab"), ("semicolon", "Semicolon"), ("comma", "Comma")], 
        string='Delimiter',
        readonly=False,
        store=True
    )
    
    # display_name = fields.Char(
    #     string='Display Name',
    #     readonly=True
    # )
    
    efn_eu_instance_id = fields.Many2one(
        'amazon.instance.ept', string='EFN Marketplace(UK)',
        readonly=False,
        store=True
    )
    
    export_inventory = fields.Boolean(
        string='Export Inventory',
        readonly=False,
        store=True
    )
    
    export_product_price = fields.Boolean(
        string='Export Product Price',
        readonly=False,
        store=True
    )
    
    fba_operations = fields.Selection(
        selection=[
            ('amz_import_fba_pending_orders', 'Import FBA Pending Orders'),
            ('amz_check_cancel_orders_fba', 'Mark Cancel Orders'),
            ('amz_shipment_report', 'Import FBA Shipped Orders'),
            ('amz_stock_adjustment_report', 'Import FBA Stock Adjustment'),
            ('amz_removal_order_report', 'Import FBA Removal Orders'),
            ('amz_customer_return_report', 'Import FBA Customer Returns'),
            ('amz_removal_order_request', 'Create Removal Order Plan'),
            ('amz_import_inbound_shipment', 'Import Inbound Shipment'),
            ('amz_create_inbound_shipment_plan', 'Create Inbound Shipment Plan'),
            ('amz_fba_live_inventory_report', 'Import FBA Inventory'),
            # Add other selection options here
        ],
        string='FBA Operations',
        readonly=False,
        store=True
    )
    
    fbm_order_updated_after_date = fields.Datetime(
        string='FBM Order Updated After Date',
        readonly=False,
        store=True
    )
    
    fbm_order_updated_before_date = fields.Datetime(
        string='FBM Order Updated Before Date',
        readonly=False,
        store=True
    )
    
    file_name = fields.Char(
        string='File Name',
        readonly=False,
        store=True
    )
    
    from_warehouse_id = fields.Many2one(
        'stock.warehouse', string='From Warehouse',
        readonly=False,
        store=True
    )
    
    import_fba_pending_sale_order = fields.Boolean(
        string='Import FBA Pending Sale Order',
        readonly=False,
        store=True
    )
    
    instance_id = fields.Many2one(
        'amazon.instance.ept', string='Marketplace',
        readonly=False,
        store=True
    )
    
    instance_ids = fields.Many2many(
        'amazon.instance.ept', string='Instance IDs',
        readonly=False,
        store=True
    )
    
    is_another_soft_create_fba_inventory = fields.Boolean(
        string='Another Soft Create FBA Inventory',
        readonly=False,
        store=True
    )
    
    is_split_report = fields.Boolean(
        string='Is Split Report',
        readonly=False,
        store=True
    )
    
    is_vcs_enabled = fields.Boolean(
        string='Is VCS Enabled',
        readonly=False,
        store=True
    )
    
    list_settlement_report = fields.Boolean(
        string='List Settlement Report',
        readonly=False,
        store=True
    )
    
    mci_efn_instance_id = fields.Many2one(
        'amazon.instance.ept', string='Marketplace(EU)',
        readonly=False,
        store=True
    )
    
    operations = fields.Selection(
        selection=[
            ('amz_fbm_export_stock_from_odoo_to_amazon', 'Export Stock'),
            ('amz_fbm_update_track_number_and_ship_status', 'Export Shipment Info/Update Order Status'),
            ('amz_check_cancel_orders_fbm', 'Mark Cancel Orders'),
            ('amz_import_fbm_shipped_orders', 'Import FBM Shipped Orders'),
            ('amz_import_fbm_missing_unshipped_orders', 'Import UnShipped Orders'),
        ],
        string='FBM Operations',
        readonly=False,
        store=True
    )
    
    order_removal_instance_id = fields.Many2one(
        'amazon.instance.ept', string='Removal Marketplace',
        readonly=False,
        store=True
    )
    
    pan_eu_instance_id = fields.Many2one(
        'amazon.instance.ept', string='Marketplace(UK)',
        readonly=False,
        store=True
    )
    
    report_end_date = fields.Datetime(
        string='Report End Date',
        readonly=False,
        store=True
    )
    
    report_start_date = fields.Datetime(
        string='Report Start Date',
        readonly=False,
        store=True
    )
    
    seller_id = fields.Many2one(
        'amazon.seller.ept', string='Amazon Seller',
        readonly=False,
        store=True
    )
    
    selling_on = fields.Selection(
        selection=[
            ('FBM', 'FBM'),
            ('FBA', 'FBA'),
            ('fba_fbm', 'FBA & FBM'),
        ],
        string='Selling On',
        readonly=False,
        store=True
    )
    
    ship_to_address = fields.Many2one("res.partner", 
        string='Ship to Address',
        readonly=False,
        store=True
    )
    
    shipment_id = fields.Char(
       string='Shipment',
        readonly=False,
        store=True
    )
    
    split_report_by_days = fields.Selection([('3', '3'),('7', '7'),('15', '15')],
        string='Split Report by Days',
        readonly=False,
        store=True
    )
    
    update_price_in_pricelist = fields.Boolean(
        string='Update Price in Pricelist',
        readonly=False,
        store=True
    )
    
    updated_after_date = fields.Datetime(
        string='Updated After Date',
        readonly=False,
        store=True
    )
    
    us_amazon_program = fields.Selection(
        selection=[
        ],
        string='Amz Fba Us Program',
        readonly=False,
        store=True
    )
    
    us_region_instance_id = fields.Many2one(
        'amazon.instance.ept', string='Marketplace(US)',
        readonly=False,
        store=True
    )
    
    user_warning = fields.Text(
        string='Note',
        readonly=False,
        store=True
    )
    
    write_date = fields.Datetime(
        string='Write Date',
        readonly=True
    )
    
    write_uid = fields.Many2one(
        'res.users', string='Last Updated by',
        readonly=True
    )

    fbm_order_update_after_date = fields.Datetime(
        string='FBM Order Update After Date',
        readonly=False,
        store=True
    )

    
    def download_sample_attachment(self):
        # Path to your sample file in the current directory
        file_name = 'import_product_sample.xls'
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        # Read the file content
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        # Encode file content to base64
        file_data_base64 = base64.b64encode(file_data)

        # Create an attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'import_product_sample.xls',
            'type': 'binary',
            'datas': file_data_base64,
            'store_fname': 'import_product_sample.xls',
            'mimetype': 'application/vnd.ms-excel'
        })

        # Return the attachment download action
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
    
    # Function to create a report request
    def create_report(self, access_token, marketplace_ids, report_type="GET_MERCHANT_LISTINGS_ALL_DATA"):
        
        account = self.env["amazon.info.account"].search([("seller_id", "=", self.seller_id.id)])
        operation = "createReport"
        seller = self.seller_id
        path_parameter=''
        payload = {
            "reportType": report_type,
            "marketplaceIds": [marketplace_ids]
        }
        
        report_response = utils.make_sp_api_request(account, operation, seller, path_parameter, payload, "POST")
        return report_response.get('reportId')
        
    
    @api.model
    def generate_csv_from_json(self, data):
        buffer = StringIO()
        writer = csv.writer(buffer)
        
        # Write the header
        if data:
            header = data[0].keys()
            writer.writerow(header)
        
        # Write the rows
        for item in data:
            writer.writerow(item.values())
        
        # Get the CSV content
        csv_content = buffer.getvalue()
        buffer.close()

        # Encode the CSV content in base64
        csv_encoded = base64.b64encode(csv_content.encode('utf-8'))
        return csv_encoded
    
    
    def amz_sync_active_products(self):
        
        print("self...",self)
        # #Get list of all product from report type.
        
        # access token and refresh token
        amazon_account_id = self.env["amazon.info.account"].search([], limit=1)
        
        # refresh_token = amazon_account_id.refresh_token
        access_token = amazon_account_id.generate_access_token()
        marketplace_ids = self.instance_id.api_ref  # Amazon Marketplace ID
        # marketplace_ids = 'A21TJRUUN4KGV'  # Amazon Marketplace ID
        seller_id = self.seller_id.id  # Replace with your actual Seller ID
        
        # Request the report
        if self.selling_on == "fba_fbm" and self.both_operations == "amz_sync_active_products":
            report_id = self.create_report(access_token, marketplace_ids)

            if report_id:
                print("Report requested successfully. Report ID:", report_id)
                
                while True:
                    try:
                        time.sleep(50)  # Wait for the report to be processed
                        report_status = self.check_report_status(access_token, report_id)
                        
                        if report_status['processingStatus'] == 'DONE':
                            document_id = report_status['reportDocumentId']
                            
                            document_info = self.download_report(access_token, document_id)
                            download_url = document_info['url']
                            report_content = requests.get(download_url).content.decode('utf-8')
                            
                            # Convert TSV data to JSON
                            json_report_data = self.convert_tsv_to_json(report_content)
                            
                            print("Report Data in JSON Format:", json.dumps(json_report_data, indent=4))
                            items = json.loads(json.dumps(json_report_data, indent=4))
                            
                            # Filter active product list
                            
                            # seller_id = self.env["amazon.seller.ept"].search([], limit=1).id
                            active_items = list(filter(lambda item: item.get('status') == 'Active', items))
                            
                            active_product_listing_id = self.env["active.product.listing.report.ept"].create({
                                "report_id" : report_id,
                                "report_document_id": document_id,
                                "seller_id" : seller_id,
                                "auto_create_product" : self.auto_create_product,
                                "fulfillment_by" : "FBM",
                                "state" : "IN_PROGRESS",
                                "instance_id": self.instance_id.id,
                                "live_product_json":active_items
                            })
                            
                            if active_items and active_product_listing_id:
                                csv_file = self.generate_csv_from_json(active_items)
                            
                                attachment_id = self.env["ir.attachment"].create({
                                    "name": "active_product_listing_"+str(datetime.now())+".csv",
                                    "type" : "binary",
                                    "datas" : csv_file,
                                    "mimetype" : "text/csv",
                                    "res_model": "active.product.listing.report.ept",
                                    "res_name": active_product_listing_id.name,
                                    "company_id":self.env.company.id,
                                })
                                
                                active_product_listing_id.attachment_id = attachment_id.id
                            
                            if active_product_listing_id.auto_create_product:
                                for item in active_items:
                                    if not self.env["amazon.product.ept"].search([("seller_sku", "=", item["seller-sku"])]) :
                                        if not self.env["product.product"].search([("default_code", "=", item["seller-sku"])]) :
                                            
                                            product_id = self.env["product.product"].create({
                                                "name" : item["item-name"],
                                                # "default_code" : item["seller-sku"]
                                                "default_code" :item["seller-sku"]
                                            })
                                            
                                            map_product_id = self.env["map.amazon.product"].create({
                                                "name" : item["item-name"],
                                                "product_id" : product_id.id,
                                                "Prod_int_ref" : product_id.default_code,
                                                "amazon_sku": item["seller-sku"],
                                                "marketplace" : self.instance_id.id,
                                                "fulfillment" : "FBM",
                                                "description" : "Importing product."
                                            })

                                            record = self.env["product.product"].search([("id", "=", product_id.id)]).write({'map_sku_id': [(4, map_product_id.id)]})

                                            
                                            self.env["amazon.product.ept"].create({
                                                "name" : item["item-name"],
                                                "seller_sku" : item["seller-sku"],
                                                "product_id": product_id.id,
                                                "instance_id": self.instance_id.id,
                                                "fulfillment_by" : "FBM",
                                                "standard_product_id_type" : "ASIN",
                                                "product_asin": item["asin1"]
                                            })
                                            
                                            #pricing list 
                                            
                                            if not self.env["product.pricelist"].search([("instance_id", "=", self.instance_id.id)]):
                                                # print("product list id",self.env["product.pricelist"].search([], limit=1).id)    
                                                #create product
                                                product_pricelist_item = self.env["product.pricelist"].create({
                                                        "name": f"Marketplace {self.instance_id.name}",
                                                        "instance_id": self.instance_id.id,
                                                        "seller_id":seller_id
                                                    }) 
                                                
                                                if not self.env["product.pricelist.item"].search([("amazon_sku", "=", item["seller-sku"])]):
                                                    product_pricelist_item_data = self.env["product.pricelist.item"].create({
                                                        "pricelist_id": product_pricelist_item.id,
                                                        "product_tmpl_id" : product_id.product_tmpl_id.id,
                                                        "min_quantity" : 1,
                                                        "fixed_price":0,
                                                        "maximum_retail_price":0,
                                                        "amazon_sku":item["seller-sku"]
                                                    }) 
                                                
                                            else:
                                                product_pricelist_item_data = self.env["product.pricelist.item"].create({
                                                        "pricelist_id": self.env["product.pricelist"].search([("instance_id", "=", self.instance_id.id)]).id,
                                                        "product_tmpl_id" : product_id.product_tmpl_id.id,
                                                        "min_quantity" : 1,
                                                        "fixed_price":0,
                                                        "maximum_retail_price":0,
                                                        "amazon_sku":item["seller-sku"]
                                                    }) 
         
                                        else:
                                            product_id = self.env["product.product"].search([("default_code", "=", item["seller-sku"])])
                                            self.env["amazon.product.ept"].create({
                                                "name" : item["item-name"],
                                                "seller_sku" : item["seller-sku"],
                                                "product_id": product_id.id,
                                                "instance_id": self.instance_id.id,
                                                "fulfillment_by" : "FBM",
                                            })   
                                    

                            else:
                                for item in active_items:
                                    
                                    if not self.env["amazon.product.ept"].search([("seller_sku", "=", item["seller-sku"])]) :
                                        create_log = self.env["common.log.lines.ept"].create({
                                            "order_ref" : report_id,
                                            "active_product_listing_report_ept_id" : active_product_listing_id.id,
                                            "mismatch_details":True,
                                            "message":"Product not Found in odoo database.",
                                            "error_log":item,
                                            "default_code": item["seller-sku"]
                                        })
                                        
                                        record = self.env["active.product.listing.report.ept"].search([("id", "=", active_product_listing_id.id)]).write({'log_count': 1})
                                        
                            break                
                        else:
                            print("Report processing is not complete. Status:", report_status['processingStatus'])
                            
                    except Exception as e:

                        document_id = report_status['reportDocumentId']
                        # seller_id = self.env["amazon.seller.ept"].search([], limit=1).id
                        
                        active_product_listing_id = self.env["active.product.listing.report.ept"].create({
                                "report_id" : report_id,
                                "report_document_id": document_id,
                                "seller_id" : seller_id,
                                "fulfillment_by" : "FBM",
                                "state" : "processed",
                                "auto_create_product" : self.auto_create_product,
                                "instance_id": self.instance_id.id,
                                "log_count":1
                            })  
                        
                        create_log = self.env["common.log.lines.ept"].create({
                                "order_ref" : report_id,
                                "active_product_listing_report_ept_id" : active_product_listing_id.id,
                                "mismatch_details":True,
                                "message":"Importing Product",
                                "error_log":str(e)
                            })  
                        break     
                    
            else:
                print("Failed to request the report.")
                

    # Function to check report status
    def check_report_status(self, access_token, report_id):
        
        account = self.env["amazon.info.account"].search([("seller_id", "=", self.seller_id.id)])
        operation = "getReportDetail"
        seller = self.seller_id
        path_parameter = report_id
       
        report_response = utils.make_sp_api_request(account, operation, seller, path_parameter, None, "GET")
        return report_response
        
    # Function to download the report
    def download_report(self, access_token, document_id):
        
        account = self.env["amazon.info.account"].search([("seller_id", "=", self.seller_id.id)])
        operation = "getDocumentDetail"
        seller = self.seller_id
        path_parameter = document_id

        report_response = utils.make_sp_api_request(account, operation, seller, path_parameter, None, "GET")
        return report_response

    # Function to convert TSV to JSON
    def convert_tsv_to_json(self, tsv_data):
        lines = tsv_data.split('\n')
        headers = lines[0].split('\t')
        json_data = []

        for line in lines[1:]:
            if line.strip():  # Skip empty lines
                values = line.split('\t')
                json_data.append(dict(zip(headers, values)))

        return json_data
    
    # -----------------------------ravi--------------------------------------------

    def import_export_processes(self):
        if self.selling_on == "fba_fbm":

            if self.both_operations == 'amz_sync_active_products': # Import Products
                return self.amz_sync_active_products()
            
            elif self.both_operations == 'amz_import_products': # Map Products
                return self.map_product_to_amazon()
                
                
            elif self.both_operations == 'amz_export_price_from_odoo_to_amazon': # Export Price
                return self.amz_export_price_from_odoo_to_amazon()
            
            elif self.both_operations == 'amz_list_settlement_report': # Download Settelment Statement
                report_start_date = self.report_start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
                # print("report_start_date",report_start_date)
                report_end_date = self.report_end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
                # print("report_end_date",report_end_date)
                return self.amz_list_settlement_report(report_start_date,report_end_date,seller_obj=False)

            elif self.both_operations == 'amz_request_rating_report': # Import rating Report  
                pass
            elif self.both_operations == 'amz_vcs_tax_report': # Import VCS
                print("self.....",self)
                # return self.inport_vat_tax_report()
                # return self.amz_import_fbm_shipped_orders(current_date=False,seller_obj=False,seller_marketplace_data=False)
                pass
            
            elif self.both_operations == 'amz_manually_create_settlement_report': # Manually Create Settlement report
                byte_data = self.choose_file
                # Decode base64
                decoded_bytes = base64.b64decode(byte_data)

                # Decode bytes to string
                decoded_string = decoded_bytes.decode('utf-8')

                # Split the string into lines
                lines = decoded_string.strip().split('\n')

                # Extract headers
                headers = lines[0].split()
                data_lines = lines[1:]

                # Function to parse a line into a dictionary
                def parse_line(line, headers):
                    # Split line into values by whitespace
                    values = line.split()
                    
                    # Handle cases where the number of values is less than the number of headers
                    if len(values) < len(headers):
                        values.extend([''] * (len(headers) - len(values)))
                    
                    # Create a dictionary from headers and values
                    return dict(zip(headers, values))

                # Parse data lines into a list of dictionaries
                data = []
                for line in data_lines:
                    # Split the line by whitespace and handle multiple spaces
                    parts = line.split(maxsplit=len(headers) - 1)
                    
                    if len(parts) < len(headers):
                        parts.extend([''] * (len(headers) - len(parts)))
                    
                    row = dict(zip(headers, parts))
                    data.append(row)

                # Convert to JSON
                first_record = data[0]
                print("first_record",first_record)
                # print(first_record["settlement-start-date"])
                # print(first_record["total-amount"])
                
                #old code .....
                # settlement_start_date = datetime.strptime(first_record["settlement-start-date"], '%d.%m.%Y')
                # settlement_end_time = datetime.strptime(first_record["settlement-end-date"], '%H:%M:%S').time()
                # combined_settlement_datetime = datetime.combine(settlement_start_date.date(), settlement_end_time)
                # formatted_settlement = combined_settlement_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
                # # Convert total-amount and currency
                # total_amount_date = datetime.strptime(first_record["total-amount"], '%d.%m.%Y')
                # currency_time = datetime.strptime(first_record["currency"], '%H:%M:%S').time()
                # combined_total_amount_datetime = datetime.combine(total_amount_date.date(), currency_time)
                # formatted_total_amount = combined_total_amount_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
                # print(formatted_settlement)
                # print(formatted_total_amount)
                #old code....
                
                #new code....
                formatted_start_date = convert_datetime_format(first_record['settlement-start-date'])
                # print("formatted_start_date",formatted_start_date)
                formatted_end_date = convert_datetime_format(first_record['settlement-end-date'])
                # print("formatted_end_date",formatted_end_date)
                dt = datetime.fromisoformat(formatted_end_date.replace('Z', '+00:00'))
                formatted_end_date=dt.strftime('%Y-%m-%d')+"T23:59:58Z"
                # print("formatted_end_date",formatted_end_date)
                # formatted_start_date="2024-05-29T07:43:57Z"
                # formatted_end_date="2024-07-10T23:59:58Z"
                #new code....
                
                return self.amz_list_settlement_report(formatted_start_date,formatted_end_date,seller_obj=False)
                
        elif self.selling_on == "FBM":

            if self.operations == 'amz_fbm_export_stock_from_odoo_to_amazon':   # Export stock
                return self.amz_fbm_export_stock_from_odoo_to_amazon(seller_obj=False,seller_id = False,seller_marketplace_data=False)
            
            elif self.operations == 'amz_fbm_update_track_number_and_ship_status': # Export Shipment Info
                pass
            elif self.operations == 'amz_check_cancel_orders_fbm':  # Marks Cancel Orders  
                pass
            elif self.operations == 'amz_import_fbm_shipped_orders':  # Import FBM shipped order
                return self.amz_import_fbm_shipped_orders(current_date=False,seller_obj=False,seller_marketplace_data=False)
            elif self.operations == 'amz_import_fbm_missing_unshipped_orders':  # Import unshipped order
                return self.amz_import_fbm_missing_unshipped_orders(current_date=False,seller_obj=False,seller_marketplace_data=False)
            
        elif self.selling_on == "FBA":
            
            if self.fba_operations == 'amz_import_fba_pending_orders': # Import FBA Pending report
                self.amz_import_fba_unshipped_orders(current_date=False,seller_obj=False,seller_marketplace_data=False)
                
            elif self.fba_operations == 'amz_check_cancel_orders_fba': # Marks cancel Order
                self.amz_fba_cancel_order()
                
            elif self.fba_operations == 'amz_shipment_report': # Import FBA Shipped Order
                self.amz_fba_shipment_report()
                
                
            elif self.fba_operations == 'amz_stock_adjustment_report': # Import FBA Stock Adjustment
                pass
            elif self.fba_operations == 'amz_removal_order_report': # Import FBA Removal Order
                pass
            elif self.fba_operations == 'amz_customer_return_report': # Import FBA Customer Returns
                pass
            elif self.fba_operations == 'amz_removal_order_request': # Create Removal Order Plan
                pass
            elif self.fba_operations == 'amz_import_inbound_shipment': # Import Inbound adjustment
                pass
            elif self.fba_operations == 'amz_create_inbound_shipment_plan': # Create Inbound Shipped Plan
                pass
            elif self.fba_operations == 'amz_removal_order_request': # Import FBA Inventory
                pass
            
    def amz_fba_shipment_report(self):
        pass
            
    def amz_fba_cancel_order(self):
        
        if not self.updated_after_date:
            return UserError("FBA Order Update After Date is not set.")
        
        # marketplace_ids = [instance.api_ref for instance in self.instance_ids]
        marketplace_ids = ['ATVPDKIKX0DER']
        
        last_updated_after = self.updated_after_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        account = self.env["amazon.info.account"].search([("seller_id", "=", self.seller_id.id)])
        operation = "getOrder"
        seller = self.seller_id
        
        for marketplace_id in marketplace_ids:
            path_parameter = f"?LastUpdatedAfter={last_updated_after}&MarketplaceIds={marketplace_id}"
            report_response = utils.make_sp_api_request(account, operation, seller, path_parameter, None, "GET")
            orders = report_response.get('payload', [])['Orders']
  
            # Filter orders by fulfillmentChannel and status
            fba_unshipped_orders = [order for order in orders if order['FulfillmentChannel'] == 'AFN' and order['OrderStatus'] == 'Canceled']

            for order in fba_unshipped_orders:
                cancel_order = self.env["sale.order"].search([("amz_order_id", "=", order['AmazonOrderId'])])
                cancel_order.action_cancel()

            
    def amz_import_fba_unshipped_orders(self,current_date,seller_obj,seller_marketplace_data):

        fba_order_update_after_date = self.updated_after_date or current_date
   
        
        if not fba_order_update_after_date:
            return UserError("FBA Order Update After Date is not set.")
        
        if not seller_obj :
            seller_obj = self.seller_id
            
        # marketplace_ids = [instance.api_ref for instance in self.instance_ids]
        # marketplace_ids = ['ATVPDKIKX0DER']
        
        if not seller_marketplace_data:
            marketplace_ids = [instance.api_ref for instance in self.instance_ids]           #self.instance_id.api_ref  # Amazon Marketplace ID
        else:
            marketplace_ids = [instance.api_ref for instance in seller_marketplace_data]  
            
            
        last_updated_after = fba_order_update_after_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        account = self.env["amazon.info.account"].search([("seller_id", "=", seller_obj.id)])
        operation = "getOrder"
        # seller = self.seller_id
        # path_parameter = f"?LastUpdatedAfter={last_updated_after}&MarketplaceIds={marketplace_id}"
        
        for marketplace_id in marketplace_ids:
            path_parameter = f"?LastUpdatedAfter={last_updated_after}&MarketplaceIds={marketplace_id}"
            order_response = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
  
            if  len(order_response['payload']['Orders']):
                orders = order_response.json().get('payload', [])['Orders']

                # Filter orders by fulfillmentChannel and status
                fba_unshipped_orders = [order for order in orders if order['FulfillmentChannel'] == 'AFN' and order['OrderStatus'] == 'Unshipped']
                
                for order in fba_unshipped_orders:
                    operation = "getOrderItems"
                    amazon_order_id = order['AmazonOrderId']
                    path_parameter = amazon_order_id
                    order_item_response = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
                    order_item_response = order_item_response.get('payload', [])['OrderItems']
                    
                    operation = "getAddress"
                    order_address_response = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
                    order_address_response = order_address_response.json().get('payload', {})['ShippingAddress']
                    
                    operation = "getBuyerInfo"
                    order_buyer_response = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
                    
                    self._fba_unshipped_sale_order(order, order_item_response, order_address_response, order_buyer_response)
                    
                
    def _fba_unshipped_sale_order(self, order, items, address, buyer_info):
        partner = self._get_or_create_customer(buyer_info, address)
        marketplace_id = self.env["amazon.instance.ept"].search([("api_ref", "=", order["MarketplaceId"])])
        sale_order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'amz_order_id': order['AmazonOrderId'],
            'amz_OrderStatus': order['OrderStatus'],
            'amz_fulfillment_by':'FBA',
            'amz_instance_id':marketplace_id.id,
            'is_fba_pending_order': True,
            'order_line': [(0, 0, {
                'product_id': self._get_product_id(item['ASIN']),
                'product_uom_qty': item['QuantityOrdered'],
                'price_unit': float(item['ItemPrice']['Amount']),
                'tax_id': self._get_tax_id(item['ItemTax']['Amount']),
            }) for item in items],
        })           
                
            
    def map_product_to_amazon(self):
        try:
            
            file_content = base64.b64decode(self.choose_file)
            # You need to know the file type, let's assume it's an Excel file
            excel_data = pd.read_excel(BytesIO(file_content))

            # Convert to JSON
            json_data = excel_data.to_json(orient='records')
            for excel_data in json.loads(json_data):
                
                if self.auto_create_product == True: 
                    if not self.env["product.product"].search([("name", "=",excel_data["Title"])]):
                        # then create
                        odoo_product = self.env["product.product"].create({
                            "name" : excel_data["Title"],
                            "default_code" : excel_data["Internal Reference"]
                        })
                    
                odoo_product = self.env['product.product'].search([('default_code', '=', excel_data["Internal Reference"])])
                amazon_marketplace = self.env['amazon.instance.ept'].search([('name', '=', excel_data["Marketplace"])])

                if odoo_product:
                    
                    #create map product.... add data in map amazon product
                    if not self.env["map.amazon.product"].search([("Prod_int_ref", "=",excel_data["Internal Reference"]),("amazon_sku", "=",excel_data["Seller SKU"])]) :
                        map_product_id = self.env["map.amazon.product"].create({
                            "name" : excel_data["Title"],
                            "product_id" : odoo_product.id,
                            "Prod_int_ref" : excel_data["Internal Reference"],
                            "amazon_sku": excel_data["Seller SKU"],
                            "marketplace" : amazon_marketplace.id,
                            "fulfillment" : excel_data["Fulfillment"] ,
                            "description" : "MAP Product"
                        })
                        record = self.env["product.product"].search([("id", "=", odoo_product.id)]).write({'map_sku_id': [(4, map_product_id.id)]})
                        
                        # add data in amazon prodcut
                        if not self.env["amazon.product.ept"].search([("seller_sku", "=",excel_data["Seller SKU"])]) :
                            
                            self.env["amazon.product.ept"].create({
                                "name" : odoo_product.name,
                                "seller_sku" : excel_data["Seller SKU"],
                                "product_id": odoo_product.id,
                                "instance_id": amazon_marketplace.id,
                                "fulfillment_by" : "FBM",
                                # "standard_product_id_type" : "ASIN",
                                # "product_asin": excel_data["asin1"]
                            })
                            
                            
                        # add product in pricelist section.
                            
                        if not self.env["product.pricelist"].search([("instance_id", "=", amazon_marketplace.id)]):

                            product_pricelist_item = self.env["product.pricelist"].create({
                                    "name": f"Marketplace {amazon_marketplace.name}",
                                    "instance_id": amazon_marketplace.id,
                                    "seller_id":self.seller_id.id
                                }) 
                            
                            if not self.env["product.pricelist.item"].search([("amazon_sku", "=", excel_data["Seller SKU"])]):
                                product_pricelist_item_data = self.env["product.pricelist.item"].create({
                                    "pricelist_id": product_pricelist_item.id,
                                    "product_tmpl_id" : odoo_product.product_tmpl_id.id,
                                    "min_quantity" : 1,
                                    "fixed_price":0,
                                    "maximum_retail_price":0,
                                    "amazon_sku":excel_data["Seller SKU"]
                                }) 
                            
                        else:
                            product_pricelist_item_data = self.env["product.pricelist.item"].create({
                                    "pricelist_id": self.env["product.pricelist"].search([("instance_id", "=", amazon_marketplace.id)]).id,
                                    "product_tmpl_id" : odoo_product.product_tmpl_id.id,
                                    "min_quantity" : 1,
                                    "fixed_price":0,
                                    "maximum_retail_price":0,
                                    "amazon_sku":excel_data["Seller SKU"]
                                })  
                              
                        
        except Exception as e:
            print(f"Exception occurred {str(e)}")                   
                
                
    def amz_fbm_export_stock_from_odoo_to_amazon(self,seller_obj,seller_id,seller_marketplace_data):
        
        # seller = self.seller_id
        if not seller_obj :
            seller_obj = self.seller_id
   
            
        amazon_products = self.env['amazon.product.ept'].search([('fulfillment_by', '=', 'FBM')])
        products_to_update = []
        account = self.env["amazon.info.account"].search([("seller_id", "=", seller_obj.id)])
        operation = "productCrud"
        # marketplace_ids = [instance.api_ref for instance in self.instance_ids]  

        if not seller_marketplace_data:
            marketplace_ids = [instance.api_ref for instance in self.instance_ids]           #self.instance_id.api_ref  # Amazon Marketplace ID
        else:
            marketplace_ids = [instance.api_ref for instance in seller_marketplace_data]  
          
                  

        # sellerId = account.seller_key
        if not seller_id:
            seller_id = self.seller_id.merchant_id 
        
        for product in amazon_products:

            sku = product.seller_sku
            product_data = {
                "sku": sku,
                "productType": "PRODUCT" ,
                "quantity": product.fix_stock_value,
                "marketplace_ids": marketplace_ids  # Assuming marketplace_ids is a list of strings
            }
            products_to_update.append(product_data)
        
        for product in products_to_update:
            sku = product['sku']
            quantity = product['quantity']
            marketplace_ids = product['marketplace_ids']
            payload = json.dumps({
                "productType": product['productType'],
                "patches": [
                    {
                        "op": "replace",
                        "path": "/attributes/fulfillment_availability",
                        "value": [
                            {
                                "fulfillment_channel_code": "DEFAULT",
                                "quantity": quantity,
                                "marketplace_id": marketplace_id
                            }
                            for marketplace_id in marketplace_ids
                        ]
                    }
                ]
            })
            
            for marketplace_id in marketplace_ids:
                path_parameter = f"{seller_id}/{sku}/?marketplaceIds={marketplace_id}&issueLocale=en_IN"
                utils.make_sp_api_request(account, operation, seller_obj, path_parameter, payload, "PATCH")
            

    def amz_import_fbm_missing_unshipped_orders(self,current_date,seller_obj,seller_marketplace_data):
        
        fbm_order_update_after_date = self.fbm_order_update_after_date or current_date
        

        if not fbm_order_update_after_date:
           
            return UserError("FBM Order Update After Date is not set.")
        
        # if not self.fbm_order_update_after_date:
        #     return UserError("FBM Order Update After Date is not set.")
        if not seller_obj :
            seller_obj = self.seller_id
        
        # marketplace_ids = [instance.api_ref for instance in self.instance_ids]
        
        if not seller_marketplace_data:
            marketplace_ids = [instance.api_ref for instance in self.instance_ids]           #self.instance_id.api_ref  # Amazon Marketplace ID
        else:
            marketplace_ids = [instance.api_ref for instance in seller_marketplace_data]  
            
        # marketplace_ids = ['ATVPDKIKX0DER']
        
        account = self.env["amazon.info.account"].search([("seller_id", "=", seller_obj.id)])
        operation = 'getOrder'
        last_updated_after = fbm_order_update_after_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        
    
        
        for marketplace_id in marketplace_ids:
            
            path_parameter = f"?LastUpdatedAfter={last_updated_after}&MarketplaceIds={marketplace_id}"
            response_orders = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
            if response_orders.get('payload', [])['Orders']:
                orders = response_orders.get('payload', [])['Orders']

                # Filter orders by fulfillmentChannel and status
                filtered_orders = [order for order in orders if order['FulfillmentChannel'] == 'MFN' and order['OrderStatus'] == 'Unshipped']
                for order in filtered_orders:
                    amazon_order_id = order['AmazonOrderId']
                    operation = "getOrderItems"
                    path_parameter = amazon_order_id
                    
                    item_response = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
                    if item_response.get('payload', [])['OrderItems']:
                        items = item_response.get('payload', [])['OrderItems']
                        
                    operation = 'getBuyerInfo' 
                    buyer_info = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
                    
                    operation = 'getAddress'
                    address = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
                    
                    if order and items and  address and buyer_info:
                        self._create_sale_order(order, items, address, buyer_info)
                        


    def _create_sale_order(self, order, items, address, buyer_info):
        
        partner = self._get_or_create_customer(buyer_info, address)
        country = self.env['res.country'].browse(self._get_country_id(address['CountryCode']))
        
        sale_order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'amz_order_id': order['AmazonOrderId'],
            'amz_OrderStatus': order['getMarketplaceParticipationsOrderStatus'],
            'amz_fulfillment_by':'FBM',
            'order_line': [(0, 0, {
                'name': item['ASIN'],
                'product_id': self._get_product_id(item['ASIN']),
                'product_uom_qty': item['QuantityOrdered'],
                'price_unit': float(item['ItemPrice']['Amount']),
                'tax_id': [(6, 0, [self._get_tax_id((float(item['ItemTax']['Amount']) / float(item['ItemPrice']['Amount'])) * 100, country)])],
            }) for item in items],
        })

        sale_order.action_confirm()
        self._create_delivery_order(sale_order)
        self._create_invoice(sale_order)

    def _get_or_create_customer(self, buyer_info, address):
        
        partner = self.env['res.partner'].search([('email', '=', buyer_info['BuyerEmail'])], limit=1)
        if not partner:
            partner = self.env['res.partner'].create({
                'name': buyer_info['BuyerName'],
                'email': buyer_info['BuyerEmail'],
                'street': address['AddressLine1'],
                'city': address['City'],
                'state_id': self._get_state_id(address['StateOrRegion']),
                'zip': address['PostalCode'],
                'country_id': self._get_country_id(address['CountryCode']),
                'phone': address['Phone'],
            })
        return partner

    def _get_product_id(self, asin):
        
        amazon_product = self.env['amazon.product.ept'].search([('product_asin', '=', asin)], limit=1)
        # if amazon_product:
        #     return amazon_product.product_id.id
        # else:
        #     # Create the product if not found in AmazonProductEPT (you may need to adjust fields)
        #     product = self.env['product.product'].create({
        #         'name': asin,
        #         'default_code': asin,
        #     })
        return amazon_product.product_id.id



    def _get_or_create_tax_group(self, country):
        tax_group = self.env['account.tax.group'].search([
            ('name', '=', f"Amazon Tax Group {country.name}")
        ], limit=1)
        
        if not tax_group:
            tax_group = self.env['account.tax.group'].create({
                'name': f"Amazon Tax Group {country.name}",
                'country_id': country.id,
            })
        
        return tax_group


    def _get_tax_id(self, tax_amount,country):
        # Ensure tax group creation or retrieval
        tax_group = self._get_or_create_tax_group(country)
        
        # Convert tax_amount to float and round
        tax_amount_float = round(float(tax_amount), 2)
        
        tax = self.env['account.tax'].search([
            ('amount', '=', tax_amount_float),
            ('type_tax_use', '=', 'sale'),
            ('country_id', '=', country.id),
            ('tax_group_id', '=', tax_group.id),
        ], limit=1)
        
        if not tax:
            # Ensure the tax group has the correct country_id
            if tax_group.country_id.id != country.id:
                tax_group.write({'country_id': country.id})
            
            tax = self.env['account.tax'].create({
                'name': f"Tax {tax_amount_float}%",
                'amount': tax_amount_float,
                'amount_type': 'percent',
                'type_tax_use': 'sale',
                'company_id': self.env.company.id,
                'country_id': country.id,
                'tax_group_id': tax_group.id,
            })
        
        return tax.id

        

    def _get_state_id(self, state_name):
        state = self.env['res.country.state'].search([('code', '=', state_name)], limit=1)
        return state.id

    def _get_country_id(self, country_code):
        country = self.env['res.country'].search([('code', '=', country_code)], limit=1)
        return country.id

    def _create_delivery_order(self, sale_order):
        existing_picking = self.env['stock.picking'].search([
            ('origin', '=', sale_order.name),
            ('picking_type_id', '=', self.env.ref('stock.picking_type_out').id)
        ], limit=1)
        
        if existing_picking:
            return existing_picking

        picking_type = self.env.ref('stock.picking_type_out')
        picking = self.env['stock.picking'].create({
            'partner_id': sale_order.partner_id.id,
            'origin': sale_order.name,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': sale_order.partner_id.property_stock_customer.id,
            'picking_type_id': picking_type.id,  # Set the picking type
            'move_type': 'direct',
            'scheduled_date': fields.Datetime.now(),
            'priority': '0',
            'company_id': sale_order.company_id.id,
            
            'move_ids_without_package': [(0, 0, {
                'name': line.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': sale_order.partner_id.property_stock_customer.id,
            }) for line in sale_order.order_line],
        })
        # picking.action_confirm()
        # picking.action_assign()
        # picking.button_validate()
        return picking
    


    def _create_invoice(self, sale_order):

        country = sale_order.partner_id.country_id

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': sale_order.partner_id.id,
            'amz_order_id': sale_order['amz_order_id'],
            'invoice_origin': sale_order.name,
            'invoice_line_ids': [(0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
                'tax_ids': [(6, 0, line.tax_id.ids)],
            }) for line in sale_order.order_line],
        })


        sale_order.write({'invoice_ids': [(4, invoice.id)]})

        # Fetch required fields from account.move.line
        account_move_lines = self.env['account.move.line'].sudo().search_read(
            [('move_id', '=', invoice.id), ('display_type', '=', "product")],
            ['id']
        )

        # Fetch required fields from sale.order.line
        sale_order_lines = self.env['sale.order.line'].sudo().search_read(
            [('order_id', '=', sale_order.id)],
            ['id']
        )

        # Zip the data to merge
        merged_data = [
            {"Account_id": acc_line['id'], "order_id": order_line['id']}
            for acc_line, order_line in zip(account_move_lines, sale_order_lines)
        ]

        # Bulk insertion
        if merged_data:
            query = """
                INSERT INTO sale_order_line_invoice_rel (invoice_line_id, order_line_id)
                VALUES {}
            """.format(", ".join("(%s, %s)" % (values["Account_id"], values["order_id"]) for values in merged_data))

            # Execute the query
            self.env.cr.execute(query)
            # Commit the transaction
            self.env.cr.commit()

        if sale_order.state != 'sale':
            sale_order.action_confirm()
        invoice.action_post()


    def amz_import_fbm_shipped_orders(self,current_date,seller_obj,seller_marketplace_data):
        
        fbm_order_update_after_date = self.fbm_order_update_after_date or current_date

        if not fbm_order_update_after_date:

            return UserError("FBM Order Update After Date is not set.")
        
        # if not self.fbm_order_update_after_date:
        #     return UserError("FBM Order Update After Date is not set.")
        
        # marketplace_ids = [instance.api_ref for instance in self.instance_ids]
        # marketplace_ids = ['ATVPDKIKX0DER']
        
        if not seller_marketplace_data:
            marketplace_ids = [instance.api_ref for instance in self.instance_ids]           #self.instance_id.api_ref  # Amazon Marketplace ID
        else:
            marketplace_ids = [instance.api_ref for instance in seller_marketplace_data]  
            
        
        if not seller_obj :
            seller_obj = self.seller_id
            
        account = self.env["amazon.info.account"].search([("seller_id", "=", seller_obj.id)])
        operation = 'getOrder'
        last_updated_after = fbm_order_update_after_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        for marketplace_id in marketplace_ids:
            
            path_parameter = f"?LastUpdatedAfter={last_updated_after}&MarketplaceIds={marketplace_id}"
            response_orders = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
            if response_orders.get('payload', [])['Orders']:
                orders = response_orders.get('payload', [])['Orders']

                # Filter orders by fulfillmentChannel and status
                filtered_orders = [order for order in orders if order['FulfillmentChannel'] == 'MFN' and order['OrderStatus'] == 'Shipped']
                for order in filtered_orders:
                    amazon_order_id = order['AmazonOrderId']
                    operation = "getOrderItems"
                    path_parameter = amazon_order_id
                    
                    item_response = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
                    if item_response.get('payload', [])['OrderItems']:
                        items = item_response.get('payload', [])['OrderItems']
                        
                    operation = 'getBuyerInfo' 
                    buyer_info = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
                    
                    operation = 'getAddress'
                    address = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
                    
                    if order and items and  address and buyer_info:
                        self._create_sale_order(order, items, address, buyer_info)
                        

    def _create_sale_order_shipped_order(self, order, items, address, buyer_info):

        partner = self._get_or_create_customer(buyer_info, address)
        country = self.env['res.country'].browse(self._get_country_id(address['CountryCode']))
        sale_order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'amz_order_id': order['AmazonOrderId'],
            'amz_OrderStatus': order['OrderStatus'],
            'amz_fulfillment_by': 'FBM',
            'order_line': [(0, 0, {
                'product_id': self._get_product_id(item['ASIN']),
                'product_uom_qty': item['QuantityOrdered'],
                'price_unit': float(item['ItemPrice']['Amount']),
                'tax_id': [(6, 0, [self._get_tax_id((float(item['ItemTax']['Amount']) / float(item['ItemPrice']['Amount'])) * 100, country)])],
            }) for item in items],
        })

        sale_order.action_confirm()
        picking = self._create_delivery_order_shipped_order(sale_order)
        self._create_invoice(sale_order)

        update_picking = self.env['stock.picking'].sudo().search([('id','=',picking.id)]).write({'state': 'done'})
   
        return picking


    def _create_delivery_order_shipped_order(self, sale_order):
        existing_picking = self.env['stock.picking'].search([
            ('origin', '=', sale_order.name),
            ('picking_type_id', '=', self.env.ref('stock.picking_type_out').id)
        ], limit=1)
        
        if existing_picking:
            return existing_picking

        picking_type = self.env.ref('stock.picking_type_out')
        picking = self.env['stock.picking'].create({
            'partner_id': sale_order.partner_id.id,
            'origin': sale_order.name,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': sale_order.partner_id.property_stock_customer.id,
            'picking_type_id': picking_type.id,  # Set the picking type
            'move_type': 'direct',
            'scheduled_date': fields.Datetime.now(),
            'priority': '0',
            'company_id': sale_order.company_id.id,
            
            'move_ids_without_package': [(0, 0, {
                'name': line.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': sale_order.partner_id.property_stock_customer.id,
            }) for line in sale_order.order_line],
        })
        picking.action_confirm()
        picking.action_assign()
        picking.button_validate()
        return picking

     
    def amz_export_price_from_odoo_to_amazon(self):
        try:
            
            for InstanceId in self.instance_ids:
                if self.env["product.pricelist"].search([("instance_id", "=", InstanceId.id)]).id :
                    
                    ProductpriceListId= self.env["product.pricelist"].search_read([("instance_id", "=", InstanceId.id)],["id","seller_id","instance_id"])[0]
                    Pricelistitem= self.env["product.pricelist.item"].search_read([("pricelist_id", "=", ProductpriceListId["id"])],["id","amazon_sku","fixed_price","maximum_retail_price"])

                    seller_id = self.env["amazon.seller.ept"].search_read([("id", "=", ProductpriceListId["seller_id"][0])],["merchant_id"])[0]["merchant_id"]
                    instance_id = ProductpriceListId["instance_id"]
                    instance_id= self.env["amazon.instance.ept"].search_read([("id", "=", instance_id[0])],["api_ref"])[0]["api_ref"]
                    
                    account = self.env["amazon.info.account"].search([("seller_id", "=", self.seller_id.id)])
                    operation = "productCrud"
                    seller = self.seller_id
                    
      
                    for updateprice in Pricelistitem:
                        
                        amazon_sku = updateprice["amazon_sku"]
                        path_parameter = f"{seller_id}/{amazon_sku}?marketplaceIds={instance_id}&issueLocale=en_IN"
                        
                        payload = json.dumps({
                        "productType": "PRODUCT",
                        "patches": [
                            {
                            "op": "replace",
                            "path": "/attributes/purchasable_offer",
                            "value": [
                                {
                                "marketplace_id": instance_id,
                                "our_price": [
                                    {
                                    "schedule": [
                                        {
                                        "value_with_tax": updateprice["fixed_price"]
                                        }
                                    ]
                                    }
                                ],
                                "maximum_retail_price": [
                                    {
                                    "schedule": [
                                        {
                                        "value_with_tax":  updateprice["maximum_retail_price"]
                                        }
                                    ]
                                    }
                                ]
                                }
                            ]
                            }
                        ]
                        })
                        utils.make_sp_api_request(account, operation, seller, path_parameter, payload, "PATCH")
            return True            
                        
        except Exception as e:
            print(f"Exception occurred {str(e)}")                  
        
    def amz_list_settlement_report(self,report_start_date,report_end_date,seller_obj=False):
        
        if not seller_obj :
            seller_obj = self.seller_id
        
        account = self.env["amazon.info.account"].search([("seller_id", "=", seller_obj.id)])
        operation = "createReport"
        # seller = self.seller_id
        path_parameter = f"?reportTypes=GET_V2_SETTLEMENT_REPORT_DATA_XML&createdSince={report_start_date}&createdUntil={report_end_date}"
            
        settlement_report = utils.make_sp_api_request(account, operation, seller_obj, path_parameter, None, "GET")
        
        if settlement_report["reports"]:
            for reportdata in settlement_report["reports"]:
                #Check report is already exist or not.
                if not self.env["settlement.report"].search([("report_id", "=",reportdata["reportId"])]) :
                    
                    #create settlement report 
                    self.env["settlement.report"].create({
                        "report_type" : reportdata["reportType"],
                        "end_date": reportdata["dataEndTime"],
                        "start_date": reportdata["dataStartTime"],
                        "instance_id": self.env["amazon.instance.ept"].search_read([("api_ref", "=", reportdata["marketplaceIds"][0])],["id"])[0]["id"],
                        "report_document_id" : reportdata["reportDocumentId"],
                        "report_id": reportdata["reportId"],
                        "seller_id": self.seller_id.id
                    })
                    
            
    @api.onchange('selling_on')
    def onchange_selling_on(self):
        if self.selling_on == 'FBM':
            self.amazon_selling = 'FBM'
        elif self.selling_on == 'FBA':
            self.amazon_selling = 'FBA'  
        elif self.selling_on == 'fba_fbm':
            self.amazon_selling = 'Both'                  


def convert_datetime_format(datetime_str):
    # Parse the original datetime string
    dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    # Convert to desired format
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')                

