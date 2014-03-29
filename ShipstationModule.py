"""
This is a simple Python 2 module for basic shipstation access.
It was written and tested in IDLE for Python 2.7.6.
It should work for other Python 2.x versions.
It will not work on Python 3, as the urllib2 library has been removed
and the urllib library calls have been drastically changed.

This module will create a connection to shipstation
and retrieve basic resources from the API.
It is built for shipsation API version 1.3.

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



EXAMPLE USE:
from ShipstationModule import *

connection = shipstation('JSON')
connection.login(<Username>,<Password>)

myOrders = connection.getOrders()
## myOrders = connection.getOrders(<Order Number>)

## THESE FUNCTIONS ARE NOT IN THE MODULE.
## THIS IS ONLY AND EXAMPLE TO SHOW YOU WHAT YOU CAN DO.
myData = ParseOrders(myOrders) ## ParseOrders is an imaginary function
WriteDataToExcel(myData) ## WriteDataToExcel is an imaginary function
"""

import urllib2
import urllib
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib2')



class shipstation:
    def __init__(self, responseType='XML'):
        self.connection = None
        
        if responseType == 'XML':
            self.responseType = 'XML'
        elif responseType == 'JSON':
            self.responseType = 'JSON'
        else: ## responseType != ['XML' or 'JSON']
            raise Exception('Invalid responseType, select XML or JSON')

    def login(self, myAccount, myPassword):
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        top_level_url = 'https://data.shipstation.com/1.3/'
        password_mgr.add_password(None, top_level_url, myAccount, myPassword) ##BASIC Realm='local.com'
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        if self.responseType == 'JSON':
            opener.addheaders += [('Accept', 'application/json')] ## set JSON request, XML is the default
        self.connection = opener
        self.login = myAccount ## who you are currently logged in as

    def getCarriers(self):
        opener = self.connection
        data = opener.open('https://data.shipstation.com/1.3/Carriers')
        string = data.read()
        return string

    def getCustomers(self, customerID=None, emailContains=None, skipToPage=0, listLength=100):
        '''
        customerID, emailContains and (skipToPage, listLength) are exclusive call functions.
        If you set skipToPage, you must also set listLength. customerID will override emailContains,
        which will override skipToPage and listLength.
        '''
        opener = self.connection
        if skipToPage != 0:
            listLength = str(listLength)
            pageReference = str(skipToPage*listLength)
            nextURL = 'https://data.shipstation.com/1.3/Customers()?$orderby=Name&$skip={}&$top={}'.format(pageReference, listLength)
            data = opener.open(nextURL)
        elif customerID != None:
            customerID = str(customerID)
            data = opener.open('https://data.shipstation.com/1.3/Customers({})'.format(customerID))
        elif emailContains != None:
            emailContains = str(emailContains)
            data = opener.open("http://data.shipstation.com/1.3/Customers()?$filter=Email%20eq%20'{}'".format(emailContains))
        else:
            data = opener.open('https://data.shipstation.com/1.3/Customers')
        string = data.read()
        return string

    def getMarketplaces(self):
        opener = self.connection
        data = opener.open("https://data.shipstation.com/1.3/Marketplaces")
        xmlstring = data.read()
        return xmlstring

    def getOrderItems(self, orderID=None):
        opener = self.connection
        if orderID != None:
            orderID = str(orderID)
            data = opener.open("https://data.shipstation.com/1.3/OrderItems()?$filter=Order/OrderNumber%20eq%20'{}'".format(orderID))
        else:
            data = opener.open("https://data.shipstation.com/1.3/OrderItems")
        string = data.read()
        return string

    def getOrders(self, nextToken=None, startDate=None, endDate=None):
        '''
        nextToken and (startDate, endDate) are exclusive call functions.
        You must include both startDate and endDate in order for the date range to be called.
        nextToken will override startDate and endDate. dateFormat = 'year-mo-da'.
        '''
        opener = self.connection
        if nextToken != None:
            nextToken = str(nextToken)
            data = opener.open('http://data.shipstation.com/1.3/Orders?$skiptoken={}'.format(nextToken))
        elif startDate != None and endDate != None:
            startDate = str(startDate); endDate = str(endDate)
            data = opener.open("https://data.shipstation.com/1.3/Orders()?$filter=(OrderDate%20ge%20datetime'{}T00:00:00')%20and%20(OrderDate%20le%20datetime'{}T00:00:00')&$expand=OrderItems".format(startDate,endDate))
        else:
            data = opener.open("https://data.shipstation.com/1.3/Orders")
        string = data.read()
        return string

    def getProducts(self, SKU):
        '''
        This function requires a SKU parameter. The SKU type should be a string.
        '''
        opener = self.connection
        data = opener.open("https://data.shipstation.com/1.3/Products()?$filter=SKU%20eq%20'{}'".format(SKU))
        string = data.read()
        return string

    def getShipments(self, orderID=None, startDate=None, endDate=None):
        '''
        orderID and (startDate, endDate) are exclusive call functions.
        You must include both startDate and endDate in order for the date range to be called.
        orderID will override startDate and endDate. dateFormat = 'year-mo-da'.
        '''
        opener = self.connection
        if orderID != None:
            orderID = str(orderID)
            data = opener.open(" https://data.shipstation.com/1.3/Shipments()?$filter=Order/OrderNumber%20eq%20'{}'".format(orderID))
        elif startDate != None and endDate != None:
            startDate = str(startDate); endDate = str(endDate)
            data = opener.open("https://data.shipstation.com/1.3/Shipments()?$filter=(ShipDate%20ge%20datetime'{}T00:00:00')%20and%20(ShipDate%20lt%20datetime'{}T00:00:00')".format(startDate,endDate))
        else:
            data = opener.open('https://data.shipstation.com/1.3/Shipments')
        string = data.read()
        return string

    def getShippingProviders(self):
        opener = self.connection
        data = opener.open('https://data.shipstation.com/1.3/ShippingProviders')
        string = data.read()
        return string

    def getShippingServices(self, provider=None):
        '''
        You must provide the provider number, not the provider name.
        '''
        opener = self.connection
        if provider != None:
            provider = str(provider)
            data = opener.open('https://data.shipstation.com/1.3/ShippingServices()?$filter=(ProviderId%20eq%20{})'.format(provider))
        else:
            data = opener.open('https://data.shipstation.com/1.3/ShippingServices')
        string = data.read()
        return string

    def getStores(self, activeOnly=True):
        opener = self.connection
        if activeOnly == True:
            data = opener.open('https://data.shipstation.com/1.3/Stores()?$filter=Active')
        else: ## activeOnly != True
            data = opener.open('https://data.shipstation.com/1.3/Stores')
        string = data.read()
        return string

    def getWarehouses(self, defaultOnly=True):
        opener = self.connection
        if defaultOnly == True:
            data = opener.open('https://data.shipstation.com/1.3/Warehouses()?$filter=Default%20eq%20true')
        else: ## defaultOnly != True
            data = opener.open('https://data.shipstation.com/1.3/Warehouses')
        string = data.read()
        return string
