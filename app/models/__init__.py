from typing import Optional
from uuid import uuid4
from datetime import datetime, timezone

from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db, login
from .order_status import OrderStatus


class BaseModel:
    id: so.Mapped[str] = so.mapped_column(
        sa.String(24), primary_key=True, index=True, default=lambda: str(uuid4())
    )
    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Customer(BaseModel, UserMixin, db.Model):
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(120))
    phone: so.Mapped[str] = so.mapped_column(sa.String(24))

    @login.user_loader
    def load_user(id):
        return db.session.get(Customer, id)


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


class Book(BaseModel, db.Model):
    title: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(256))
    original_price: so.Mapped[float] = so.mapped_column(
        sa.DECIMAL(precision=12, scale=2)
    )
    selling_price: so.Mapped[float] = so.mapped_column(
        sa.DECIMAL(precision=12, scale=2)
    )


class Image(db.Model):
    path: so.Mapped[str] = so.mapped_column(sa.String(256))
    book_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Book.id))


class BookOrder(BaseModel, db.Model):
    book_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Book.id))
    order_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Order.id))
    quantity: so.Mapped[int] = so.mapped_column(default=1)
    acquired: so.Mapped[bool] = so.mapped_column(default=False)
