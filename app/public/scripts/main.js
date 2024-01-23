class Orders {
  constructor() {
    this.load();
    this.save();
  }
  save() {
    window.localStorage.setItem('orders', JSON.stringify(this.orders));
  }
  load() {
    this.orders = JSON.parse(window.localStorage.getItem('orders'));
    if (!this.orders) {
      this.orders = {};
    }
  }
  addOrder(bookId) {
    this.load();
    if (!this.orders[bookId]) this.orders[bookId] = 1;
    this.save();
    return this.orders[bookId];
  }
  removeOrder(bookId) {
    this.load();
    delete this.orders[bookId];
    this.save();
    return 0;
  }
  clearOrders() {
    this.load();
    this.orders = {};
    this.save();
  }
  increaseBookOrder(bookId) {
    this.load();
    if (!this.orders[bookId]) this.orders[bookId] = 0;
    this.orders[bookId] += 1;
    this.save();
    return this.orders[bookId];
  }
  decreaseBookOrder(bookId) {
    this.load();
    if (!this.orders[bookId]) return 0;
    if (this.orders[bookId] === 1) return this.removeOrder(bookId);
    this.orders[bookId] -= 1;
    this.save();
    return this.orders[bookId];
  }
  getBookOrderCount(bookId) {
    this.load();
    if (!this.orders[bookId]) return 0;
    return this.orders[bookId];
  }
  getTotalOrderCount() {
    this.load();
    let count = 0;
    this.orders;
    for (const book of Object.keys(this.orders)) {
      count += this.orders[book];
    }
    return count;
  }
}

function showAlert(message) {
  const card = document.createElement('div');
  card.innerHTML = message;
  card.className = 'alert';
  document.body.querySelector('main').prepend(card);
}

function updateCartBadge() {
  const cartBade = document.querySelector('.cart .badge');
  if (!cartBade) return;
  const orderCount = orders.getTotalOrderCount();
  if (orderCount === 0) {
    cartBade.className = 'badge display-none';
  } else {
    cartBade.innerHTML = orderCount;
    cartBade.className = 'badge';
  }
}

// declare global and initialize stuff
const orders = new Orders();
updateCartBadge();
updateAllBookQuantity();

function updateAllBookQuantity() {
  document.querySelectorAll('[class^=bq]').forEach((bookQuantity) => {
    const bookId = bookQuantity.className.replace('bq-', '');
    bookQuantity.innerHTML = orders.getBookOrderCount(bookId);
  });
}

// cart action buttons
function addBookToCart(bookId) {
  orders.increaseBookOrder(bookId);
  document.querySelector(`.bq-${bookId}`).innerHTML =
    orders.getBookOrderCount(bookId);
  showAlert('Item added');
  updateCartBadge();
}
function removeBookFromCart(bookId) {
  orders.decreaseBookOrder(bookId);
  document.querySelector(`.bq-${bookId}`).innerHTML =
    orders.getBookOrderCount(bookId);
  showAlert('Item removed');
  updateCartBadge();
}
// add buttons
document.querySelectorAll('.btn-add').forEach((button) => {
  button.addEventListener('click', () => {
    addBookToCart(button.dataset.bookId);
  });
});
// subtract buttons
document.querySelectorAll('.btn-sub').forEach((button) => {
  button.addEventListener('click', () => {
    removeBookFromCart(button.dataset.bookId);
  });
});
// add to cart button
document
  .querySelector('button.add-to-cart')
  ?.addEventListener('click', function () {
    bookId = this.dataset.bookId;
    orders.addOrder(bookId);
    document.querySelector(`.bq-${bookId}`).innerHTML =
      orders.getBookOrderCount(bookId);
    showAlert('Item added');
    updateCartBadge();
  });
