from sqlalchemy import Column, Integer, Boolean, Text, Double
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """id: Autoincrement
    user_id: Integer
    user_first_name: Text
    is_admin: Boolean
    admin_inviter_id: Integer"""
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Double)
    user_first_name = Column('user_first_name', Text)
    is_admin = Column('is_admin', Boolean)
    admin_inviter_id = Column('admin_inviter_id', Integer)

    def __str__(self):
        return f'{self.id} {self.user_id} {self.user_first_name} {self.is_admin} {(self.admin_inviter_id if self.is_admin else "")}'


class Ad(Base):
    """ad_id: Autoincrement
    user_id: Integer
    user_first_name: Text
    user_link: Text
    user_mention: Text
    product_name: Text
    amount: Integer
    price: Integer
    town: Text
    description: Text
    picture_id: Integer
    posted: Boolean
    post_id: Integer"""
    __tablename__ = 'ads'

    ad_id = Column('ad_id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', Double)
    user_first_name = Column('user_first_name', Text)
    user_link = Column('user_link', Text)
    user_mention = Column('user_mention', Text)
    product_name = Column('product_name', Text)
    amount = Column('amount', Integer)
    price = Column('price', Integer)
    town = Column('town', Text)
    description = Column('description', Text)
    picture_id = Column('picture_id', Text)
    posted = Column('posted', Boolean, default=False)
    post_id = Column('post_id', Integer)

    def __str__(self):
        return f'{self.ad_id} {self.user_id} {self.user_first_name} {self.user_link} {self.product_name} {self.amount} ' \
               f'{self.price} {self.town} {self.description} {self.picture_id} {self.posted} {self.post_id}'
