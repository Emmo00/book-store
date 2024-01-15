async function getBookInfoFromServer(bookId) {
  const response = await fetch(`/api/books/${bookId}`);
  return (await response.json()).data;
}

async function getCartBooksInfo() {
  const books = [];
  for (const [bookId, quantity] of Object.entries(orders.orders)) {
    books.push({ ...(await getBookInfoFromServer(bookId)), quantity });
  }
  return books;
}

function createCartItem(bookId, bookTitle, bookPrice, bookQuantity) {
  return `<article class="cart-item">
    <div>
      <p><b class="book-title">${bookTitle}</b></p>
      <p class="book-price">N${bookPrice}</p>
    </div>
    <div class="book-btns">
      <button class="book-btn btn-sub" data-book-id="${bookId}">-</button><span class="bq-${bookId}">${bookQuantity}</span>
      <button class="book-btn btn-add" data-book-id="${bookId}">+</button>
    </div>
  </article>`;
}

async function populateCartItems() {
  const cartItems = document.querySelector('.cart-items');
  if (cartItems) cartItems.innerHTML = '';
  const cartBooks = [];
  (await getCartBooksInfo()).forEach((book) => {
    cartBooks.push(
      createCartItem(book.id, book.title, book.price, book.quantity)
    );
  });
  if (cartItems) cartItems.innerHTML = cartBooks.join(' ');
  // add buttons
  document.querySelectorAll('.btn-add').forEach((button) => {
    button.addEventListener('click', () => {
      addBookToCart(button.dataset.bookId);
      updateCartTotal();
    });
  });
  // subtract buttons
  document.querySelectorAll('.btn-sub').forEach((button) => {
    button.addEventListener('click', () => {
      removeBookFromCart(button.dataset.bookId);
      updateCartTotal();
    });
  });
}

async function updateCartTotal() {
  const books = await getCartBooksInfo();
  const total = books.reduce((a, b) => +a + +b.price * b.quantity, 0);
  document.querySelector('.cart-total').innerHTML = total + '.00';
}

populateCartItems();
updateCartTotal();
