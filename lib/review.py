# lib/department.py
from __init__ import CURSOR, CONN


class Review:
    
    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, restarant_id, customer_id, star_rating, id=None):
        self.id = id
        self.restaurant_id = restarant_id
        self.customer_id = customer_id
        self.star_rating = star_rating

    def __repr__(self):
        return f"<Review {self.id}: {self.restaurant_id}, {self.customer_id}, {self.star_rating}>"

    @property
    def restaurant_id(self):
        return self._restaurant_id

    @restaurant_id.setter
    def restaurant_id(self, restaurant_id):
        if isinstance(restaurant_id, int):
            self._restaurant_id = restaurant_id
        else:
            raise ValueError(
                "Restaurant id must be an integer."
            )

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        if isinstance(customer_id, int):
            self._customer_id = customer_id
        else:
            raise ValueError(
                "Customer id must be an integer."
            )
        
    @property
    def star_rating(self):
        return self._star_rating

    @star_rating.setter
    def star_rating(self, star_rating):
        if isinstance(star_rating, int):
            self._star_rating = star_rating
        else:
            raise ValueError(
                "Star Rating must be an integer."
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Reviews instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            restaurant_id INTEGER,
            customer_id INTEGER,
            star_rating INTEGER,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """  # Closing parenthesis was missing here
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Reviews instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and location values of the current Review instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO reviews (restaurant_id, customer_id, star_rating)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.restaurant_id, self.customer_id, self.star_rating))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, restaurant_id, customer_id, star_rating):
        """ Initialize a new Review instance and save the object to the database """
        review = cls(restaurant_id, customer_id, star_rating)
        review.save()
        return review

   