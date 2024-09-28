import json
import logging
from contextlib import contextmanager
from pprint import pformat

import requests
from werkzeug.urls import url_encode, url_join, url_parse

from odoo import _
from odoo.exceptions import UserError, ValidationError

from ..amazon_odoo_linker import const, amazon_api
import requests
from datetime import timedelta
from datetime import datetime

_logger = logging.getLogger(__name__)

class AmazonRateLimitError(Exception):
    """ When the API rate limit of Amazon is reached. """

    def __init__(self, operation):
        self.operation = operation
        super().__init__()



def exchange_authorization_code(authorization_code, account):
        """ Exchange the LWA authorization code for the LWA refresh token and save it on the account.

        :param str authorization_code: The authorization code to exchange with the LWA refresh token.
        :param recordset account: The account for which a refresh token must be exchanged, as an
                                `amazon.account` record.
        :return: None
        """
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
        }
        endpoint = const.PROXY_ENDPOINTS['authorization']
        response_content = make_proxy_request(endpoint, account.env, payload=data)
        account.refresh_token = response_content['refresh_token']


def make_proxy_request(endpoint, env, payload=None):
        """ Make a request to the Amazon proxy at the specified endpoint.

        :param str endpoint: The proxy endpoint to be reached by the request.
        :param Environment env: An `odoo.api.Environment`.
        :param dict payload: The Amazon-specific payload of the request.
        :return: The JSON-formatted content of the response.
        :rtype: dict
        :raise ValidationError: If a `RequestException` occurs.
        """
        url = url_join(const.PROXY_URL, endpoint)
        ICP = env['ir.config_parameter']
        data = {
            'db_uuid': ICP.sudo().get_param('database.uuid'),
            'db_enterprise_code': ICP.sudo().get_param('database.enterprise_code'),
            'amazon_data': json.dumps(payload or {}),
        }
        try:
            response = requests.post(url, data=data, timeout=60)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                response_content = response.json()
                error_code = response_content.get('error')
                error_description = response_content.get('error_description')
                _logger.exception(
                    "Invalid API request (error code: %s, description: %s) with data:\n%s",
                    error_code, error_description, pformat(data)
                )
                raise ValidationError(
                    _("Error code: %s; description: %s", error_code, error_description)
                )
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.warning("Could not establish the connection to the proxy.", exc_info=True)
            raise ValidationError(_("Could not establish the connection to the proxy."))
        return response.json()
    
def refresh_access_token(account):
        """ Request a new LWA access token if it is expired and save it on the account.

        :param recordset account: The account for which an access token must be requested, as an
                                `amazon.account` record.
        :return: None
        """
        if datetime.utcnow() > account.access_token_expiry - timedelta(minutes=5):
            payload = {
                'grant_type': 'refresh_token',
                'refresh_token': account.refresh_token,
            }
            endpoint = const.PROXY_ENDPOINTS['authorization']
            response_content = make_proxy_request(endpoint, account.env, payload=payload)
            
            print("response_content", response_content)
            account.access_token = response_content['access_token']
            account.write({
                'access_token': response_content['access_token'],
                'access_token_expiry': datetime.utcnow() + timedelta(
                    seconds=response_content['expires_in']
                ),
            })
            
            return response_content['access_token']
        
def make_sp_api_request(account, operation, seller, path_parameter='', payload=None, method='GET'):
    # import pdb;pdb.set_trace()
    account.ensure_one()

    path = amazon_api.API_ENDPOINT[operation]['url_path'].format(param=path_parameter)
    domain = amazon_api.seller_url(seller)
    url = url_join(domain, path)

    payload = payload or {}

    # Refresh the credentials used to sign the request.
    if amazon_api.API_ENDPOINT[operation]['restricted_resource_path'] is None:  # No RDT is required
        refresh_access_token(account)
        access_token = account.access_token
    else:
        refresh_restricted_data_token(account)
        access_token = account.restricted_data_token

    # Build the request headers
    host = url_parse(domain).netloc
    now = datetime.now()
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8',
        'host': host,
        'x-amz-access-token': access_token,
        'x-amz-date': now.strftime('%Y%m%dT%H%M%SZ'),
    }
    
    try:
        if method == 'GET':
            response = requests.get(url, params=payload, headers=headers, timeout=60)
        elif method == 'POST':  # 'POST'
            response = requests.post(url, json=payload, headers=headers, timeout=60)
        elif method == 'PATCH':
            response = requests.patch(url, json=payload, headers=headers, timeout=60)
        elif method == 'DELETE':
            response = requests.delete(url, json=payload, headers=headers, timeout=60)  
              
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            if response.status_code == 429:
                raise AmazonRateLimitError(operation)
            else:
                errors = response.json().get('errors')
                error_code = errors and errors[0].get('code')
                error_message = errors and errors[0].get('message')
                _logger.exception(
                    "Invalid API request (error code: %s, description: %s) with data:\n%s",
                    error_code, error_message, pformat(payload)
                )
                raise ValidationError(_(
                    "The communication with the API failed.\nError code: %s; description: %s"
                ) % (error_code, error_message))
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        _logger.exception("Unable to reach endpoint at %s", url)
        raise ValidationError(_("Could not establish the connection to the API."))
    json_response = response.json()
    _logger.info("SPAPI response for operation %s: %s", operation, pformat(json_response))
    return json_response


def refresh_restricted_data_token(account):
    """ Request a new Restricted Data Token (RDT) if it is expired and save it on the account.

    The request includes the restricted path of all restricted operation to avoid refreshing the RDT
    for each new operation.

    :param recordset account: The account for which a Restricted Data Token must be requested, as an
                              `amazon.account` record.
    :return: None
    """
    if datetime.utcnow() > account.restricted_data_token_expiry - timedelta(minutes=5):
        all_restricted_operations = [
            k for k, map in amazon_api.API_ENDPOINT.items() if map['restricted_resource_path']
        ]
        OPERATIONS_MAPPING = amazon_api.API_ENDPOINT
        payload = {
            'restrictedResources': [{
                'method': 'GET',
                'path': OPERATIONS_MAPPING[operation]['restricted_resource_path'],
                'dataElements': OPERATIONS_MAPPING[operation]['restricted_resource_data_elements'],
            } for operation in all_restricted_operations]
        }
        response_content = make_sp_api_request( account, 'createRestrictedDataToken', account.seller_id, payload=payload, method='POST')
        account.write({
            'restricted_data_token': response_content['restrictedDataToken'],
            'restricted_data_token_expiry': datetime.utcnow() + timedelta(
                seconds=response_content['expiresIn']
            ),
        })