class Feedback:
    
    @property
    def date(self):
        """Returns the date of the feedback"""
        return self._date

    @date.setter
    def date(self, value):
        """Set the date of the feedback"""
        self._date = value
    

    @property
    def rating(self):
        """Returns the rating of the feedback"""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Set the rating of the feedback"""
        self._rating = value
    

    @property
    def message(self):
        """Returns the message of the feedback"""
        return self._message

    @message.setter
    def message(self, value):
        """Set the message of the feedback"""
        self._message = value


    @property
    def buyer(self):
        """Returns the buyer of the feedback"""
        return self._buyer

    @buyer.setter
    def buyer(self, value):
        """Set the buyer of the feedback"""
        self._buyer = value
    

    @property
    def buyer_order_count(self):
        """Returns the buyer order count of the feedback"""
        return self._buyer_order_count

    @buyer_order_count.setter
    def buyer_order_count(self, value):
        """Set the buyer order count of the feedback"""
        self._buyer_order_count = value


    @property
    def price(self):
        """Returns the price of the feedback"""
        return self._price

    @price.setter
    def price(self, value):
        """Set the price of the feedback"""
        self._price = value
    