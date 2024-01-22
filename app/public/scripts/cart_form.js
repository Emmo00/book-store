document.querySelector('.cart-continue').addEventListener('click', async () => {
  // submit form to server
  const fname = document.querySelector('#name').value.trim();
  const phone = document.querySelector('#phone').value.trim();
  const email = document.querySelector('#email').value.trim();
  const location = document.querySelector('#location').value;

  if (!fname || !phone || !email || location === 'default') {
    showAlert('All input fields are required');
    return;
  }
  if (!validPhone(phone)) {
    showAlert('Invalid Phone number');
    return;
  }
  if (!validEmail(email)) {
    showAlert('Invalid Email address');
    return;
  }
  const payload = {
    name: fname,
    phone,
    email,
    location,
    books: orders.orders,
  };
  console.log(payload);
  const response = await fetch('/api/orders', {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    showAlert('Error Processing order. Please Try again later');
    return;
  }
  const data = (await response.json()).data;
  document.location = data.link;
});

function validPhone(phone) {
  const phonePattern = /^\+[0-9]{13}$/;
  return phonePattern.test(phone);
}

function validEmail(email) {
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailPattern.test(email);
}
