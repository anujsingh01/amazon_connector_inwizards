API_ENDPOINT={
    'createFeed': {
        'url_path': '/feeds/2021-06-30/feeds',
        'restricted_resource_path': None,
    },
    'createFeedDocument': {
        'url_path': '/feeds/2021-06-30/documents',
        'restricted_resource_path': None,
    },
    'createRestrictedDataToken': {
        'url_path': '/tokens/2021-03-01/restrictedDataToken',
        'restricted_resource_path': None,
    },
    'getFeed': {
        'url_path': '/feeds/2021-06-30/feeds/{param}',
        'restricted_resource_path': None,
    },
    'getFeedDocument': {
        'url_path': '/feeds/2021-06-30/documents/{param}',
        'restricted_resource_path': None,
    },
    'getMarketplaceParticipations': {
        'url_path': '/sellers/v1/marketplaceParticipations',
        'restricted_resource_path': None,
    },
    'getOrder': {
        'url_path': '/orders/v0/orders/{param}',
        # Amazon requires the path to include the placeholder "{orderID}" to grant the RDT.
        'restricted_resource_path': '/orders/v0/orders/{param}',  #param=orderId
        'restricted_resource_data_elements': ['buyerInfo', 'shippingAddress'],
    },
    'getOrders': {
        'url_path': '/orders/v0/orders',
        'restricted_resource_path': '/orders/v0/orders',
        'restricted_resource_data_elements': ['buyerInfo', 'shippingAddress'],
    },
    'getOrderItems': {
        'url_path': '/orders/v0/orders/{param}/orderItems',
        # Amazon requires the path to include the placeholder "{orderID}" to grant the RDT.
        'restricted_resource_path': '/orders/v0/orders/{param}/orderItems', #param=orderId
        'restricted_resource_data_elements': ['buyerInfo']
    },
    
    'createReport': {
        'url_path': '/reports/2021-06-30/reports/{param}',
        'restricted_resource_path': None,
    },
    'getReportDetail' : {
        'url_path' : '/reports/2021-06-30/reports/{param}', #param=report_id
        'restricted_resource_path': None,
    },
    'getDocumentDetail':{
        'url_path':'/reports/2021-06-30/documents/{param}', #param=document_id
        'restricted_resource_path': None,
    },
    'getAddress':{
        'url_path': '/orders/v0/orders/{param}/address',
        'restricted_resource_path': None,
    },
    'getBuyerInfo': {
        'url_path' : '/orders/v0/orders/{param}/buyerInfo',
        'restricted_resource_path': None,
    },
    'productCrud' : {
        "url_path": "/listings/2021-08-01/items/{param}",
        'restricted_resource_path': None,
    }
}

# Production URL
region_urls = {
    'european': "https://sellingpartnerapi-eu.amazon.com",
    'north_american': "https://sellingpartnerapi-na.amazon.com",
    'east_american': "https://sellingpartnerapi-fe.amazon.com"
}

# Testing URL
sandbox_region_urls = {
    'european': "https://sandbox.sellingpartnerapi-eu.amazon.com",
    'north_american': "https://sandbox.sellingpartnerapi-na.amazon.com",
    'east_american': "https://sandbox.sellingpartnerapi-fe.amazon.com"
}

def seller_url(seller):
    selected_region = (
        region_urls['european'] if seller.is_european_region 
        else region_urls['north_american'] if seller.is_north_america_region 
        else region_urls['east_american']
    )
    
    return selected_region

def sandbox_seller_url(seller):
    selected_region = (
        sandbox_region_urls['european'] if seller.is_european_region 
        else sandbox_region_urls['north_american'] if seller.is_north_america_region 
        else sandbox_region_urls['east_american']
    )
    
    return selected_region



