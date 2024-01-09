from typing import Optional
from uuid import uuid4
from datetime import datetime, timezone

from flask import url_for
import sqlalchemy as sa
import sqlalchemy.orm as so
import inflection

from app import db
from .order_status import OrderStatus


class BaseModel:
    id: so.Mapped[str] = so.mapped_column(
        sa.String(36), primary_key=True, index=True, default=lambda: str(uuid4())
    )
    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Customer(BaseModel, db.Model):
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(120))
    phone: so.Mapped[str] = so.mapped_column(sa.String(24))
    orders: so.WriteOnlyMapped["Order"] = so.relationship(back_populates="customer")


class PickupLocation(BaseModel, db.Model):
    name: so.Mapped[str] = so.mapped_column(sa.String(120))


class Order(BaseModel, db.Model):
    customer_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Customer.id))
    pickup_location_id: so.Mapped[str] = so.mapped_column(
        sa.ForeignKey(PickupLocation.id)
    )
    status: so.Mapped[str] = so.mapped_column(
        sa.Enum(OrderStatus), default=OrderStatus.sent
    )
    customer: so.Mapped[Customer] = so.relationship(back_populates="orders")


class Book(BaseModel, db.Model):
    title: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(256))
    original_price: so.Mapped[float] = so.mapped_column(
        sa.DECIMAL(precision=12, scale=2)
    )
    selling_price: so.Mapped[float] = so.mapped_column(
        sa.DECIMAL(precision=12, scale=2)
    )
    images: so.WriteOnlyMapped["Image"] = so.relationship(back_populates="book")

    @property
    def slug(self):
        return inflection.parameterize(self.title)

    @property
    def main_image(self):
        return db.session.scalar(self.images.select().limit(1)).path

    @property
    def other_images(self):
        images = db.session.scalars(self.images.select())
        return [image.path for image in images]


class Image(BaseModel, db.Model):
    name: so.Mapped[str] = so.mapped_column(sa.String(256))
    book_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Book.id))
    book: so.Mapped[Book] = so.relationship(back_populates="images")

    @property
    def path(self):
        return url_for("uploads", file_name=self.name)


class BookOrder(BaseModel, db.Model):
    book_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Book.id))
    order_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Order.id))
    quantity: so.Mapped[int] = so.mapped_column(default=1)
    acquired: so.Mapped[bool] = so.mapped_column(default=False)
