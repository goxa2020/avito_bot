from sqlalchemy import Column, Integer, Boolean, Text, Double, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """id: Autoincrement
    user_id: Integer
    user_first_name: Text
    user_link: Text
    is_admin: Boolean
    admin_inviter_id: Integer"""
    __tablename__ = 'users'
    __allow_unmapped__ = True

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', Double, unique=True)
    # TODO: user_id must be str, not double
    user_first_name = Column('user_first_name', Text)
    user_link = Column('user_link', Text)
    is_admin = Column('is_admin', Boolean)
    admin_inviter_id = Column('admin_inviter_id', Integer)

    def __str__(self):
        return f'id: {self.id}, user_id: {self.user_id}, user_first_name: {self.user_first_name}, is_admin: {self.is_admin}, ' \
               f'{f"admin_inviter_id: {self.admin_inviter_id}" if self.is_admin else ""}'


class Ad(Base):
    """ad_id: Autoincrement
    user_id: Integer
    owner: User
    product_name: Text
    amount: Integer
    price: Integer
    town: Text
    description: Text
    picture_id: Integer
    posted: Boolean
    post_id: Integer
    is_pinned: Boolean"""
    __tablename__ = 'ads'
    __allow_unmapped__ = True

    ad_id = Column('ad_id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', ForeignKey('users.user_id'))
    owner: User = relationship('User', backref='users')
    product_name = Column('product_name', Text)
    amount = Column('amount', Integer)
    price = Column('price', Integer)
    town = Column('town', Text)
    description = Column('description', Text)
    picture_id = Column('picture_id', Text)
    posted = Column('posted', Boolean, default=False)
    post_id = Column('post_id', Integer)
    is_pinned = Column('is_pinned', Boolean, default=False)

    def __str__(self):
        return f'ad_id: {self.ad_id}, user_id: {self.user_id}, product_name: {self.product_name}, amount: {self.amount}, ' \
               f'price: {self.price}, town: {self.town}, description: {self.description}, picture_id: {self.picture_id}, ' \
               f'posted: {self.posted}, {f"post_id: {self.post_id}," if self.posted else ""} is_pinned: {self.is_pinned},\n' \
               f'owner: {self.owner}'
