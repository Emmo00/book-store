from app import db, create_app


app = create_app()

app.app_context().push()

from app.models import Customer, Book, Order, OrderStatus, BookOrder, PickupLocation

c = Customer(name="emma", email="email@email.com", phone="1234567890")
pl = PickupLocation(name="Jimbazz")
book = Book(
    title="GSP101", description="gsp 101", original_price=1500, selling_price=1700
)

db.session.add_all([c, pl, book])
db.session.commit()

print(c.to_json())
print(pl.to_json())
print(book.to_json())

order = Order(customer_id=c.id, pickup_location_id=pl.id)

db.session.add(order)
db.session.commit()

print(order.to_json())

bo = BookOrder(book_id=book.id, order_id=order.id, quantity=3)

db.session.add(bo)
db.session.commit()

print(bo.to_json())
