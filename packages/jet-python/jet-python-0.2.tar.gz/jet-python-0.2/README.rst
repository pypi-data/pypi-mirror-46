=============================
Python API client for Jet.com
=============================

.. image:: https://badge.fury.io/py/jet-python.png
    :target: http://badge.fury.io/py/jet-python

.. image:: https://travis-ci.org/fulfilio/jet-python.png?branch=master
    :target: https://travis-ci.org/fulfilio/jet-python

Python Jet.com API Client

Installation
------------

.. code-block::

    pip install jet-python



Usage
-----

Get an authenticated jet client
```````````````````````````````

.. code-block:: python

    from jet import Jet
    jet = Jet(
        user='0CXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        secret='NXXXXXXXXXXXXXXXXXXXXXXXXj+',
        merchant_id='d4fe23456789876545678656787652',
    )

Fetch 10 products at a time
```````````````````````````

.. code-block:: python

  skus = jet.products.get_skus(page=1)


Find ready to ship orders
```````````````````````````

.. code-block:: python

    order_ids = jet.orders.get_recent_order_ids(
        status='ready'
    )


Acknowledge an order
```````````````````````````

.. code-block:: python

    jet.orders.acknowledge(order_id)


Mark an order as shipped
````````````````````````

This involved a nested data structure. To make this easier
this module provides a convenient higher level data
structure called `jet.Shipment`

.. code-block:: python


    from jet import Shipment

    shipment = Shipment(
        shipment_id='CS1234',
        tracking_number='1Z12324X12342435',
        ship_from_zip_code='91789',
        shipment_date=date.today(),
        carrier='UPS',
        shipment_method='Other'
    )

    for item in items:
        shipment.add_item(
            sku='iphone-xs',
            quantity=2,
        )

    jet.orders.ship(order_id, [shipment])


Features
--------

* TODO


Integration Approval API calls
------------------------------

.. code-block:: python


    from jet import Jet
    jet = Jet('XXX', 'XXX', 'XXXX')
    jet.products.update_price('IPHONE-8', 79.99)

    # Fulfillment node id prodived by approval workflow
    jet.products.update_inventory('IPHONE-8', {'998bb45c821d4d5a84e73d68004f898b': 5})

    # Get orders
    order_ids = jet.orders.get_recent_order_ids('ready')

    # Acknowledge an order
    jet.orders.acknowledge(
        '6b07db3d2e5643479242527332782dee',
        {'a35bd1f8a8ab4481a0cccda6e2012e13': 'fulfillable'}
    )

    # Acknowledge order
    jet.orders.acknowledge(
        'e0d9e28d650d44daaa55f297847c0ab2',
        order_items={'69585063be2a46ccb5dbf75823a3e7c1': 'fulfillable'}
    )

    # Cancelling an order
    shipment = Shipment(shipment_id='CS1234')
    shipment.add_item("RBE750-GOL", quantity=0, cancel_quantity=1)
    jet.orders.ship('e0d9e28d650d44daaa55f297847c0ab2', [shipment])
