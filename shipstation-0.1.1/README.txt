shipstation 0.1.1

Connect Python applications with the ShipStation API

Wrapper over the urllib2 and urllib libraries for communicating with the Shipstation API.

Simple Use: Drag the shipstation folder to your Python Library frameworks folder; or place the shipstation folder in the same directory as your python application file.


Resources Available:
Carriers
Customers
Marketplaces
OrderItems
Orders
Products
Shipments
ShippingProviders
ShippingServices
Stores
Warehouses





EXAMPLE USES:
from shipstation import *

connection = shipstation('JSON')
connection.login(<Username>,<Password>)

myOrders = connection.getOrders()
## myOrders will now be a JSON object pulled from the shipstation API



import shipstation

connection = shipstation.shipstation()
connection.login(<Username>,<Password>)

myOrders = connection.getOrders(<Order Number>)
## myOrders will now be an XML object pulled from the shipstation API