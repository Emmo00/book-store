from app import create_app

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db
from app.models import (
    Customer,
    Book,
    Order,
    OrderStatus,
    BookOrder,
    PickupLocation,
    Image,
)

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "sa": sa,
        "so": so,
        "db": db,
        "Customer": Customer,
        "Book": Book,
        "Order": Order,
        "BookOrder": BookOrder,
        "OrderStatus": OrderStatus,
        "PickupLocation": PickupLocation,
        "Image": Image,
    }
