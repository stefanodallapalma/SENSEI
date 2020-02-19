class Vendor:
    
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
    def dream_market_rating(self):
        """Returns the positive rating of the dreammarket"""
        return self._dream_market_rating

    @dream_market_rating.setter
    def dream_market_rating(self, value):
        """Set the positive rating of the dreammarket"""
        self._dream_market_rating = value
    

    @property
    def last_seen(self):
        """Returns the last seen moment of the vendor"""
        return self._last_seen

    @last_seen.setter
    def last_seen(self, value):
        """Set the last seen moment of the vendor"""
        self._last_seen = value
    
    
    @property
    def since(self):
        """Returns the registration moment of the vendor"""
        return self._since

    @since.setter
    def since(self, value):
        """Set the registration moment of the vendor"""
        self._since = value
    
    
    @property
    def ships_from(self):
        """Returns where the vendor ships from"""
        return self._name

    @ships_from.setter
    def ships_from(self, value):
        """Set where the vendor ships from"""
        self._ships_from = value
    
    
    @property
    def rating(self):
        """Returns the rating of the vendor"""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Set the rating of the vendor"""
        self._rating = value
    
    
    @property
    def orders_finalized(self):
        """Returns how may orders are finalized"""
        return self._orders_finalized

    @orders_finalized.setter
    def orders_finalized(self, value):
        """Set how may orders are finalized"""
        self._orders_finalized = value
    
    
    @property
    def finalized_early(self):
        return self._finalized_early

    @finalized_early.setter
    def finalized_early(self, value):
        self._finalized_early = value
    
    
    @property
    def profile(self):
        """Returns the profile of the vendor"""
        return self._profile

    @profile.setter
    def profile(self, value):
        """Set the profile of the vendor"""
        self._profile = value
    
    
    @property
    def terms_conditions(self):
        """Returns the terms and conditions of the vendor"""
        return self._terms_conditions

    @terms_conditions.setter
    def terms_conditions(self, value):
        """Set the terms and conditions of the vendor"""
        self._terms_conditions = value
    
    
    @property
    def pgp(self):
        """Returns the pgp of the vendor"""
        return self._pgp

    @pgp.setter
    def pgp(self, value):
        """Set the pgp of the vendor"""
        self._pgp = value


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
        
        i = 1
        for rat in self.dream_market_rating:
            to_string += "\nDream Market Rating " + str(i) + ": " + str(rat)
            i += 1
        
        to_string += "\nLast Seen: " + self.last_seen
        to_string += "\nSince: " + self.since
        to_string += "\nShips From: " + self.ships_from
        
        i = 1
        for rat in self.rating:
            to_string += "\nRating " + str(i) + ": " + str(rat)
            i += 1
        
        to_string += "\nOrder Finalized: " + str(self.orders_finalized)
        to_string += "\nFinalized Early: " + self.finalized_early
        to_string += "\nProfile: " + self.profile
        to_string += "\nTerms and Conditions: " + self.terms_conditions
        
        return to_string