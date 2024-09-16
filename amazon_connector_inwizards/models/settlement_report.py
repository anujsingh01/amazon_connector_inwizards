from odoo import models, fields,api
import random
import string
import requests
import csv
import io
import json
import xmltodict
from io import StringIO
import base64
from datetime import datetime 
from ...amazon_connector_inwizards import amazon_api



class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    settlement_report_id = fields.Many2one('settlement.report', string='Settlement Report')
    
    
class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement'

    settlement_report_id = fields.Many2one('settlement.report', string='Settlement Report')    
    
class SettlementReport(models.Model):
    _name = 'settlement.report'
    _description = 'Settlement Report'
    
    @api.model
    def _generate_random_name(self, length=8):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(length))

    already_processed_report_id = fields.Many2one('settlement.report', string='Already Processed Report')
    amz_settlement_ref = fields.Char(string='Amazon Settlement Ref')
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')
    company_id = fields.Many2one('res.company', string='Company')
    create_date = fields.Datetime(string='Created on', readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    # display_name = fields.Char(string='Display Name')
    end_date = fields.Date(string='End Date',readonly=True)
    has_message = fields.Boolean(string='Has Message')
    id = fields.Integer(string='ID')
    instance_id = fields.Many2one('amazon.instance.ept', string='Marketplace',required=True)
    invoice_count = fields.Integer(string='Invoice Count')
    is_fees = fields.Boolean(string='Is Fee')
    message_attachment_count = fields.Integer(string='Attachment Count')
    message_follower_ids = fields.One2many('mail.followers', 'res_id', string='Followers')
    message_has_sms_error = fields.Boolean(string='Message Delivery error')
    message_has_error_counter = fields.Integer(string='Number of errors')
    message_ids = fields.One2many('mail.message', 'res_id', string='Messages')
    message_is_follower = fields.Boolean(string='Is Follower')
    message_needaction = fields.Boolean(string='Action Needed')
    message_needaction_counter = fields.Integer(string='Number of Actions')
    message_partner_ids = fields.Many2many('res.partner', string='Followers (Partners)')
    name = fields.Char(string='Name', default=lambda self: self._generate_random_name(),readonly=True)
    rating_ids = fields.One2many('rating.rating', 'res_id', string='Ratings')
    reimbursement_invoice_ids = fields.Many2one('account.move', string='Reimbursement Invoice')
    report_document_id = fields.Char(string='Report Document ID',readonly=True)
    report_id = fields.Char(string='Report ID',readonly=True)
    report_request_id = fields.Char(string='Report Request ID')
    report_type = fields.Char(string='Report Type',readonly=True)
    requested_date = fields.Datetime(string='Requested Date', default=fields.Datetime.now)
    seller_id = fields.Many2one('amazon.seller.ept', string='Seller')
    start_date = fields.Date(string='Start Date',readonly=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string='State', default='submitted')
    statement_id = fields.Many2one('account.bank.statement', string='Bank Statement')
    statement_line_ids = fields.One2many('account.bank.statement.line', 'settlement_report_id', string='Settlement Lines')
    user_id = fields.Many2one('res.users', string='Settled User')
    website_message_ids = fields.One2many('mail.message', 'res_id', string='Website Messages')
    write_date = fields.Datetime(string='Last Updated on', readonly=True)
    write_uid = fields.Many2one('res.users', string='Last Updated by', readonly=True)
    
    def process_statement(self):
        print("process_statement", self)
        amazon_account_id = self.env["amazon.info.account"].search([], limit=1)
        access_token = amazon_account_id.generate_access_token()
        
        seller_url = amazon_api.seller_url(self.seller_id)
        url = f"{seller_url}/reports/2021-06-30/documents/{self.report_document_id}"

        headers = {
            'x-amz-access-token': access_token
        }
        response = requests.get(url, headers=headers)
        response_data = response.json()
        
        csv_url = response_data.get('url')

        if csv_url:
            csv_response = requests.get(csv_url)
            xml_data = csv_response.text

            # # Debug: Print the raw XML data
            # print("XML Data:\n", xml_data)

            # Parse the XML data
            data_dict = xmltodict.parse(xml_data)
            
            # Extract the main sections
            envelope = data_dict.get('AmazonEnvelope', {})
            message = envelope.get('Message', {})
            settlement_report = message.get('SettlementReport', {})
            settlement_data = settlement_report.get('SettlementData', {})
            transactions = settlement_report.get('OtherTransaction', [])

            # Convert settlement data to dictionary
            settlement_info = {
                'amazon_settlement_id': settlement_data.get('AmazonSettlementID'),
                'total_amount': settlement_data.get('TotalAmount', {}).get('#text'),
                'currency': settlement_data.get('TotalAmount', {}).get('@currency'),
                'start_date': settlement_data.get('StartDate'),
                'end_date': settlement_data.get('EndDate'),
                'deposit_date': settlement_data.get('DepositDate')
            }

            # Convert transactions to list of dictionaries
            transaction_list = []
            if isinstance(transactions, dict):
                transactions = [transactions]  # Convert single transaction to list

            for transaction in transactions:
                transaction_info = {
                    'amazon_order_id': transaction.get('AmazonOrderID'),
                    'transaction_type': transaction.get('TransactionType'),
                    'posted_date': transaction.get('PostedDate'),
                    'amount': transaction.get('Amount', {}).get('#text'),
                    'currency': transaction.get('Amount', {}).get('@currency'),
                    'merchant_fulfillment_id': transaction.get('MerchantFulfillmentID'),
                    'marketplace_name': transaction.get('MarketplaceName')
                }
                transaction_list.append(transaction_info)

            # Update the model with the parsed data
            
            settlement_data_info=[{
                'settlement_id': settlement_info['amazon_settlement_id'],
                'start_date': settlement_info['start_date'],
                'end_date': settlement_info['end_date'],
                'deposit_date': settlement_info['deposit_date'],
                'total_amount': settlement_info['total_amount'],
                'currency': settlement_info['currency'],
                'transactions': transaction_list
            }]
            
            # print("settlement_data_info........",settlement_data_info)
            
            journal = self.env['account.journal'].search([('type', '=', 'bank')], limit=1)
    
            if not journal.suspense_account_id:
                print("please select suspense_account_id")
                pass
                # raise UserError('Please set a suspense account on the selected journal.')
             
            #Store value in account bank statement..
                
            for settlement_data in settlement_data_info:
                # Extract the starting balance and filter out 'Payable to Amazon' transactions
                starting_balance = 0.0
                filtered_transactions = []
                for transaction in settlement_data['transactions']:
                    if transaction['transaction_type'] == 'Payable to Amazon':
                        starting_balance = float(transaction['amount'])
                    else:
                        filtered_transactions.append(transaction)

                # Create the bank statement record
                
                settlement_id_str = str(settlement_data.get('settlement_id', ''))
                name_value = f"Amazon Settlement - {settlement_id_str}"
                
                statement_vals = {
                    'name': name_value,
                    'date': settlement_data['deposit_date'],
                    'balance_start': starting_balance,
                    'balance_end_real': float(settlement_data['total_amount']),
                    'journal_id': journal.id,
                    'settlement_report_id': self.id
                }
                bank_statement = self.env['account.bank.statement'].create(statement_vals)
                
                # Create the bank statement line records
                for index, transaction in enumerate(filtered_transactions, start=1):
                    # tran_type = f"{transaction['transaction_type']}{self.name} {index}"
                    posted_date= transaction['posted_date']
                    transaction_type = str(transaction['transaction_type'])
                    name = str(self.name)
                    tran_type = f"{transaction_type} {posted_date} {name} {index}"
                    line_vals = {
                        'statement_id': bank_statement.id,
                        'date': transaction['posted_date'],
                        'name':tran_type,
                        'amount': float(transaction['amount']),
                        'journal_id': journal.id,
                        'settlement_report_id': self.id
                    }
                    self.env['account.bank.statement.line'].create(line_vals)  
                    
                if filtered_transactions:
                    csv_file = self.generate_csv_from_json(filtered_transactions)
                
                    attachment_id = self.env["ir.attachment"].create({
                        "name": "amazon_statement_report_"+str(datetime.now())+".csv",
                        "type" : "binary",
                        "datas" : csv_file,
                        "mimetype" : "text/csv",
                        "res_model": "settlement.report",
                        "res_name": self.name,
                        "company_id":self.env.company.id,
                    })
                    
                    attachment = self.env["settlement.report"].browse(self.id)
                    values_to_update = {
                        "attachment_id": attachment_id.id,
                        "state": "done"
                    }
                    attachment.write(values_to_update)
                     
                    
                                            

    def view_statement(self):
        bank_account_id = self.env["account.bank.statement"].search([("settlement_report_id", "=", self.id)])
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Bank Statement',
            'res_model': 'account.bank.statement',
            'view_mode': 'form',
            'target': 'current',
            'domain': [('settlement_report_id', '=', self.id)],
            'res_id' : bank_account_id.id if bank_account_id else None
        }
        return action        
    
    @api.model
    def generate_csv_from_json(self, data):
        # Parse the JSON data
        # data = json.loads(json_data)
        
        # Create a StringIO buffer
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
    
    def download_statement(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model=ir.attachment&id={self.attachment_id.id}&field=datas&filename_field=name&download=true',
            'target': 'self',
        }      

    
