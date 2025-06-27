let token = '';
let artisanName = '';
let cart = [];

function register() {
  const data = {
    name: document.getElementById('name').value,
    bio: document.getElementById('bio').value,
    email: document.getElementById('email').value,
    password: document.getElementById('password').value
  };
  fetch('http://localhost:5000/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json()).then(alerta => alert(alerta.message));
}

function login() {
  const data = {
    email: document.getElementById('loginEmail').value,
    password: document.getElementById('loginPassword').value
  };
  fetch('http://localhost:5000/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json()).then(result => {
    if (result.token) {
      token = result.token;
      artisanName = document.getElementById('loginEmail').value;
      alert('Login realizado com sucesso');
    } else {
      alert(result.error);
    }
  });
}

function addProduct() {
  if (!token) return alert('Faça login primeiro');
  const data = {
    name: document.getElementById('prodName').value,
    description: document.getElementById('prodDesc').value,
    price: document.getElementById('prodPrice').value,
    artisan: artisanName
  };
  fetch('http://localhost:5000/api/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(res => res.json()).then(result => {
    alert(result.message);
    loadProducts();
  });
}

function addToCart(productId) {
  cart.push({ id: productId });
  localStorage.setItem("cart", JSON.stringify(cart));
  alert("Produto adicionado ao carrinho");
}

function checkout() {
  const storedCart = JSON.parse(localStorage.getItem("cart") || "[]");
  fetch("http://localhost:5000/api/checkout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ cart: storedCart })
  }).then(r => r.json()).then(d => {
    alert(d.message);
    localStorage.removeItem("cart");
    cart = [];
  });
}

function submitComment(event, productId) {
  event.preventDefault();
  const author = event.target.querySelector(".comment-author").value;
  const content = event.target.querySelector(".comment-content").value;
  const rating = event.target.querySelector(".comment-rating").value;

  fetch("http://localhost:5000/api/comments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, author, content, rating })
  }).then(res => res.json()).then(res => {
    alert(res.message);
    loadProducts();
  });
}

function loadComments(productId) {
  fetch(`http://localhost:5000/api/comments/${productId}`)
    .then(r => r.json())
    .then(comments => {
      const div = document.getElementById(`comments-${productId}`);
      div.innerHTML = "<h4>Avaliações:</h4>";
      comments.forEach(c => {
        div.innerHTML += `<div class="comment"><b>${c.author}</b>: ${c.content} ⭐${c.rating}</div>`;
      });
    });
}

function loadProducts() {
  fetch('http://localhost:5000/api/products')
    .then(response => response.json())
    .then(products => {
      displayProducts(products);
    })
    .catch(error => {
      console.error('Erro ao carregar produtos:', error);
      alert('Erro ao carregar produtos');
    });
}

function filterProducts() {
  const searchTerm = document.getElementById('search').value.toLowerCase();
  const priceFilter = document.getElementById('price-filter').value;
  
  fetch('http://localhost:5000/api/products')
    .then(response => response.json())
    .then(products => {
      let filtered = products.filter(p => 
        p.name.toLowerCase().includes(searchTerm) || 
        p.description.toLowerCase().includes(searchTerm)
      );
      
      if (priceFilter) {
        const [min, max] = priceFilter === '500+' ? [500, Infinity] : priceFilter.split('-').map(Number);
        filtered = filtered.filter(p => p.price >= min && p.price <= max);
      }
      
      displayProducts(filtered);
    });
}

function displayProducts(products) {
  const container = document.getElementById('products');
  container.innerHTML = '';
  
  if (products.length === 0) {
    container.innerHTML = '<p>Nenhum produto encontrado.</p>';
    return;
  }
  
  products.forEach(p => {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
      <h3>${p.name}</h3>
      <p>${p.description}</p>
      <p>R$ ${p.price.toFixed(2)}</p>
      <p><i>${p.artisan}</i></p>
      <form onsubmit="submitComment(event, ${p.id})">
        <input type="text" class="comment-author" placeholder="Seu nome" required>
        <input type="text" class="comment-content" placeholder="Comentário" required>
        <input type="number" class="comment-rating" min="1" max="5" placeholder="Nota" required>
        <button type="submit">Enviar Avaliação</button>
      </form>
      <div id="comments-${p.id}"></div>
    `;
    container.appendChild(card);
    loadComments(p.id);
  });
}

// Carrega os produtos quando a página é carregada
window.onload = function() {
  loadProducts();
};
