class Product:
    
    @property
    def timestamp(self):
        """Timestamp"""
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, value):
        """Set timestamp"""
        self._timestamp = value

    @property
    def market(self):
        """Darkweb Market"""
        return self._market

    @market.setter
    def market(self, value):
        """Set darkweb market"""
        self._market = value
    
    
    @property
    def name(self):
        """Returns the vendor name"""
        return self._name

    @name.setter
    def name(self, value):
        """Set the vendor name"""
        self._name = value


    @property
    def category(self):
        """Returns the main category of the product"""
        return self._category

    @category.setter
    def category(self, value):
        """Set the main category of the product"""
        self._category = value
    

    @property
    def subcategory(self):
        """Returns the subcategory of the product"""
        return self._subcategory

    @subcategory.setter
    def subcategory(self, value):
        """Set the subcategory of the product"""
        self._subcategory = value
    
    
    @property
    def vendor(self):
        """Returns the vendor username from the market"""
        return self._vendor

    @vendor.setter
    def vendor(self, value):
        """Set the vendor username from the market"""
        self._vendor = value
    
    
    @property
    def price_eur(self):
        """Returns the price from the market"""
        return self._price_eur

    @price_eur.setter
    def price_eur(self, value):
        """Set the price from the market"""
        self._price_eur = value
    
    
    @property
    def price_btc(self):
        """Returns the price of the product in bitcoin"""
        return self._price_btc

    @price_btc.setter
    def price_btc(self, value):
        """Set the price of the product in bitcoin"""
        self._price_btc = value
    
    
    @property
    def stock(self):
        """Returns the price of the product in bitcoin"""
        return self._stock

    @stock.setter
    def stock(self, value):
        """Set the price of the product in bitcoin"""
        self._stock = value
    
    
    @property
    def shipping_options(self):
        """Returns the shipping options in a list"""
        return self._shipping_options

    @shipping_options.setter
    def shipping_options(self, value):
        """Set the shipping options in a list"""
        self._shipping_options = value
    
    
    @property
    def product_class(self):
        """Returns the class of the product"""
        return self._product_class

    @product_class.setter
    def product_class(self, value):
        """Set the class of the product"""
        self._product_class = value
    
    
    @property
    def escrow_type(self):
        """Returns the escrow type"""
        return self._escrow_type

    @escrow_type.setter
    def escrow_type(self, value):
        """Set the escrow type"""
        self._escrow_type = value
    
    
    @property
    def ships_from(self):
        """Returns where the product ships from"""
        return self._ships_from

    @ships_from.setter
    def ships_from(self, value):
        """Set where the product ships from"""
        self._ships_from = value


    @property
    def ships_to(self):
        """Returns where the product ships to"""
        return self._ships_to

    @ships_to.setter
    def ships_to(self, value):
        """Set where the product ships to"""
        self._ships_to = value


    @property
    def items_sold(self):
        """Returns the items sold"""
        return self._items_sold

    @items_sold.setter
    def items_sold(self, value):
        """Set the items sold"""
        self._items_sold = value
    

    @property
    def orders_sold_since(self):
        """Returns the date since when the orders are sold"""
        return self._orders_sold_since

    @orders_sold_since.setter
    def orders_sold_since(self, value):
        """Set the date since when the orders are sold"""
        self._orders_sold_since = value
    

    @property
    def details(self):
        """Returns the description from the product"""
        return self._details

    @details.setter
    def details(self, value):
        """Set the description from the product"""
        self._details = value
    

    @property
    def terms_and_conditions(self):
        """Returns terms and conditions of the product"""
        return self._terms_and_conditions

    @terms_and_conditions.setter
    def terms_and_conditions(self, value):
        """Set terms and conditions of the product"""
        self._terms_and_conditions = value


    @property
    def feedback(self):
        """Returns the feedback of the vendor in a list"""
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        """Set the feedback of the vendor in a list"""
        self._feedback = value


    def __str__(self):
        to_string = "Name: " + self.name
        to_string += "\nCategory: " + self.category
        to_string += "\nSubcategory: " + self.subcategory
        to_string += "\nVendor: " + self.vendor
        to_string += "\nEUR: " + str(self.price_eur)
        to_string += "\nBTC: " + str(self.price_btc)
        to_string += "\nStock: " + self.stock

        i = 1
        for option in self.shipping_options:
            to_string += "\nShipping option " + str(i) + ": " + option
            i += 1

        to_string += "\nProduct class: " + self.product_class
        to_string += "\nEscrow Type: " + self.escrow_type
        to_string += "\nShips From: " + self.ships_from

        i = 1
        for to in self.ships_to:
            to_string += "\nShips To " + str(i) + ": " + to
            i += 1

        to_string += "\nItems sold: " + str(self.items_sold)
        to_string += "\nOrders sold since: " + str(self.orders_sold_since)
        to_string += "\nDetails: " + self.details
        to_string += "\nTerms and conditions: " + self.terms_and_conditions

        return to_string