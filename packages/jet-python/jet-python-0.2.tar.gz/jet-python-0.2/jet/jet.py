# -*- coding: utf-8 -*-
from datetime import datetime, time
import requests
import pytz
from dateutil.parser import parse as parse_date


UTC = pytz.timezone('UTC')

__all__ = ['Jet', 'JetAuthenticationError', 'JetException']


class JetException(Exception):
    pass


class JetAuthenticationError(JetException):
    pass


def isoformat(d):
    "Convert a date to datetime ISO format used by jet"
    datetime.combine(d, time(0, 0)).replace(
        tzinfo=UTC
    ).isoformat()
    current_time = datetime.utcnow().time()
    return datetime.combine(d, current_time).replace(tzinfo=UTC).strftime(
        '%Y-%m-%dT%H:%M:%S.0000000-00:00'
    )


class Jet(object):
    """
    Jet.com API Client
    """

    base_url = "https://merchant-api.jet.com/api"

    def __init__(self, user, secret, merchant_id):
        self.user = user
        self.secret = secret
        self.merchant_id = merchant_id
        self.token = None
        self.token_expires_on = None
        self.get_token()

    def get_token(self):
        token_data = requests.post(
            self.base_url + '/token',
            json={
                'user': self.user,
                'pass': self.secret,
            }
        ).json()
        if 'id_token' not in token_data:
            raise JetAuthenticationError(". ".join(
                token_data.get('errors', [])
            ))
        self.token = token_data['id_token']
        self.token_expires_on = parse_date(
            token_data['expires_on']
        )
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'bearer %s' % (
            self.token
        )

    def send_request(self, method, url, **kwargs):
        caller = getattr(self.session, method)
        response = caller(self.base_url + url, **kwargs)
        # TODO: logging debug the body and response content
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return True

    @property
    def products(self):
        return Product(self)

    @property
    def orders(self):
        return Order(self)

    @property
    def returns(self):
        return Return(self)

    @property
    def fulfillment_nodes(self):
        return FulfillmentNode(self)


class FulfillmentNode(object):
    def __init__(self, client):
        self.client = client

    def all(self):
        urls = self.client.send_request(
            'get',
            '/fulfillment-nodes',
        )['fulfillment_nodes']
        return [
            self.get_node(url.rsplit('/')[-1])
            for url in urls
        ]

    def get_node(self, node_id):
        """
        Return a fulfillment node
        """
        return self.client.send_request(
            'get',
            '/fulfillment-nodes/' + node_id,
        )


class Product(object):
    """
    The Products API is used to perform specific actions
    to a single product and is good for isolated changes.

    For retailers with large catalogs, use the Catalog API
    """
    def __init__(self, client):
        self.client = client

    def update_price(self, sku, price):
        """
        At Jet, the price the retailer sets is not the same as the price
        the customer pays. The price set for a SKU will be the price the
        retailer gets paid for selling the products. However, the price
        that is set will influence how competitive your product offer
        matches up compared to other product offers for the same SKU.

        TODO: Implement support for fulfillment nodes

        https://developer.jet.com/docs/merchant-sku-price
        """
        return self.client.send_request(
            'put',
            '/merchant-skus/' + sku + '/price',
            json={'price': price}
        )

    def get_sku(self, sku):
        """
        Retrieve information about SKUs
        """
        return self.client.send_request(
            'get',
            '/merchant-skus/' + sku,
        )

    def get_price(self, sku):
        """
        Retrieve price information of SKU
        """
        return self.client.send_request(
            'get',
            '/merchant-skus/' + sku + '/price',
        )

    def get_inventory(self, sku):
        """
        Retrieve inventory information of SKU
        """
        return self.client.send_request(
            'get',
            '/merchant-skus/' + sku + '/inventory',
        )

    def get_skus(self, page=1, per_page=10):
        """
        Retrieve multiple SKUs at once
        """
        urls = self.client.send_request(
            'get',
            '/merchant-skus',
            params={
                "offset": (page - 1) * per_page,
                "limit": per_page,
            }
        )['sku_urls']
        return [
            self.get_sku(url.rsplit('/')[-1])
            for url in urls
        ]

    def all_skus(self):
        """
        Returns all of the skus by iterating over the pages
        """
        per_page = 100
        for page in range(1, 1000):
            skus = self.get_skus(page, per_page)
            for sku in skus:
                yield sku
            if len(skus) < per_page:
                break

    def create(self, sku, data):
        """
        Create a new product
        """
        return self.client.send_request(
            'put',
            '/merchant-skus/' + sku,
            json=data
        )

    def update_inventory(self, sku, data):
        """
        Update inventory for products.

        Data should be a dictionary with the fuflillment_node_id
        as the key and inventory quantity as the value
        """
        return self.client.send_request(
            'patch',
            '/merchant-skus/' + sku + '/inventory',
            json={
                'fulfillment_nodes': [
                    {
                        'fulfillment_node_id': node_id,
                        'quantity': quantity,
                    }
                    for node_id, quantity in data.items()
                ]
            }
        )


class Order(object):
    """
    Order Management
    """

    def __init__(self, client):
        self.client = client

    def get_recent_order_ids(self, status, cancelled=None, fulfillment_node=None):
        """
        Access the first 1000 orders in a certain status. Orders will only
        be available by status for 90 days after order creation.

        Status can be one of the following:

        * 'created' -       The order has just been placed. Jet.com allows a
                            half hour for fraud check and customer cancellation.
                            Retailers NOT fulfill orders that are created.
        * 'ready' -         The order is ready to be fulfilled by the retailer
        * 'acknowledged'    The order has been accepted by the retailer and
                            is awaiting fulfillment
        * 'inprogress' -    The order is partially shipped
        * 'complete' -      The order is completely shipped or cancelled. All units have
                            been accounted for

        Returns a list of recent order ids
        """
        params = {}

        if cancelled is not None:
            params['isCancelled'] = 'true' if cancelled else 'false'

        if fulfillment_node:
            params['fulfillment_node'] = fulfillment_node

        order_urls = self.client.send_request(
            'get',
            '/orders/%s' % status,
            params=params
        )['order_urls']
        return [
            url.rsplit('/')[-1] for url in order_urls
        ]

    def get(self, order_id):
        """
        Retreive an order with the given ID
        """
        return self.client.send_request(
            'get',
            '/orders/withoutShipmentDetail/%s' % order_id,
        )

    def acknowledge(self, order_id, order_items, status='accepted',
                    alt_order_id=None):
        """
        The order acknowledge call is utilized to allow a retailer to accept or
        reject an order. If there are any skus in the order that cannot be
        fulfilled then you will reject the order.

        Valid statuses are:

        * rejected - other
        * rejected - fraud
        * rejected - item level error
        * rejected - ship from location not available
        * rejected - shipping method not supported
        * rejected - unfulfillable address
        * accepted

        :param alt_order_id: Option merchant supplied order ID.
        :param order_items: A dictionary with order_item_id as the key
                            and the status as value.

                            {
                                'a35bd1f8a8ab4481a0cccda6e2012e13': 'fulfillable'
                            }
        """
        body = {
            'acknowledgement_status': status,
            'order_items': [{
                'order_item_acknowledgement_status': item_status,
                'order_item_id': item_id,
            } for item_id, item_status in order_items.items()]
        }
        if alt_order_id is not None:
            body['alt_order_id'] = alt_order_id
        return self.client.send_request(
            'put',
            '/orders/%s/acknowledge' % order_id,
            json=body
        )

    def ship(self, order_id, shipments):
        """
        The order shipped call is utilized to provide Jet with the SKUs
        that have been shipped or cancelled in an order, the tracking information,
        carrier information and any additional returns information for the order.
        """
        body = {"shipments": []}
        for shipment in shipments:
            if isinstance(shipment, Shipment):
                body['shipments'].append(shipment.to_dict())
            else:
                body['shipments'].append(shipment)
        return self.client.send_request(
            'put',
            '/orders/%s/shipped' % order_id,
            json=body
        )


class Return(object):
    """
    Returns Management
    """

    def __init__(self, client):
        self.client = client

    def get_return_ids(self, status):
        return self.client.send_request(
            'get',
            '/returns/%s' % status,
        )

    def get(self, return_id):
        """
        Retreive an return with the given ID
        """
        return self.client.send_request(
            'get',
            '/returns/state/%s' % return_id,
        )

    def complete(self, return_id, order_id,
                 items, agree_to_return_charge,
                 alt_order_id=None,
                 return_charge_feedback=None):
        body = {
            'merchant_order_id': order_id,
            'items': items,
            'agree_to_return_charge': agree_to_return_charge,
        }
        if alt_order_id:
            body['alt_order_id'] = alt_order_id
        return self.client.send_request(
            'put',
            '/returns/%s/complete' % return_id,
            json=body
        )


class Shipment(object):
    """
    A shipment object corresponding to an order.

    For carrier codes and shipment methods, refer the link
    below:

    https://developer.jet.com/docs/ship-order
    """

    def __init__(self, shipment_id,
                 tracking_number=None,
                 ship_from_zip_code=None,
                 shipment_date=None,
                 expected_delivery_date=None,
                 shipment_method='Other',
                 carrier='Other',
                 pick_up_date=None,
                 ):
        self.shipment_id = shipment_id
        self.ship_from_zip_code = ship_from_zip_code
        self.tracking_number = tracking_number
        self.shipment_date = shipment_date
        self.expected_delivery_date = expected_delivery_date
        self.shipment_method = shipment_method
        self.carrier = carrier
        self.pick_up_date = pick_up_date

        self.items = []

    def to_dict(self):
        rv = {
            'alt_shipment_id': self.shipment_id,
            'shipment_items': self.items,
        }
        if self.tracking_number:
            rv['shipment_tracking_number'] = self.tracking_number
        if self.shipment_method:
            rv['response_shipment_method'] = self.shipment_method
        if self.ship_from_zip_code:
            rv['ship_from_zip_code'] = self.ship_from_zip_code
        if self.carrier:
            rv['carrier'] = self.carrier
        if self.shipment_date:
            rv['response_shipment_date'] = isoformat(self.shipment_date)
        if self.expected_delivery_date:
            rv['expected_delivery_date'] = isoformat(
                self.expected_delivery_date
            )
        if self.pick_up_date:
            rv['carrier_pick_up_date'] = isoformat(
                self.pick_up_date
            )
        return rv

    def add_item(self, sku, quantity, cancel_quantity=None):
        """
        Add an item to the shipment
        """
        rv = {
            'merchant_sku': sku,
            'response_shipment_sku_quantity': quantity,
        }

        if cancel_quantity is not None:
            rv['response_shipment_cancel_qty'] = cancel_quantity

        self.items.append(rv)
