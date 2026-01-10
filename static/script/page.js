

const categories = {
    'E': 'electronics-container',
    'F': 'fashion-container',
    'A': 'accessories-container',
    'W': 'wearables-container',
    'C': 'computers-container'
};

function renderProducts(products, containerId) {
    const container = document.getElementById(containerId);

    if (!products || products.length === 0) {
        container.innerHTML = '<div class="col-12 text-center text-muted">No products available</div>';
        return;
    }

    let html = '';
    products.forEach(product => {
        // Determine image source: already absolute URL or relative path
        let imgSrc = product.Image || '';
        if (imgSrc && !/^https?:\/\//i.test(imgSrc)) {
            // remove leading slashes if any
            imgSrc = imgSrc.replace(/^\//, '');
            imgSrc = '/media/' + imgSrc;
        } else if (!imgSrc) {
            imgSrc = 'https://via.placeholder.com/260';
        }

        html += `
                <div class="col-md-4 col-lg-3 mb-4">
                    <a class="card-link" onclick="showProductDetail('${product.uuid}')" data-uuid="${product.uuid}">
                        <div class="product-card">
                            <img src="${imgSrc}" class="img-fluid" onerror="this.src='https://via.placeholder.com/260'">
                            <div class="p-3">
                                <h6>${product.Name}</h6>
                                <span class="price-tag">Rs. ${parseFloat(product.Price).toFixed(2)}</span>
                                <p class="small text-muted mt-2">Qty: ${product.Quantity}</p>
                            </div>
                        </div>
                    </a>
                </div>
            `;
    });

    container.innerHTML = html;
}

// Modal for product details (with quantity input)
function createProductModal() {
    if (document.getElementById('product-modal')) return;
    const modal = document.createElement('div');
    modal.id = 'product-modal';
    modal.innerHTML = `
                <div class="modal" tabindex="-1" role="dialog" style="display:none; position:fixed; z-index:1050; left:0; top:0; width:100%; height:100%; background:rgba(0,0,0,0.5);">
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="product-modal-title"></h5>
                                <button type="button" class="close" onclick="closeProductModal()">&times;</button>
                            </div>
                            <div class="modal-body" id="product-modal-body"></div>
                            <div class="modal-footer">
                                <div class="mr-auto">
                                    <label for="product-qty" class="sr-only">Quantity</label>
                                    <input id="product-qty" type="number" min="1" value="1" style="width:90px; color:black;" class="form-control">
                                </div>
                                <button class="btn btn-primary" id="add-to-cart-btn">Add to Cart</button>
                                <button class="btn btn-secondary" onclick="closeProductModal()">Close</button>
                            </div>
                        </div>
                    </div>
                </div>`;
    document.body.appendChild(modal);
}

function showProductModal(product) {
    createProductModal();
    document.getElementById('product-modal-title').innerText = product.Name;
    let imgSrc = product.Image || '';
    if (imgSrc && !/^https?:\/\//i.test(imgSrc)) {
        imgSrc = imgSrc.replace(/^\//, '');
        imgSrc = '/media/' + imgSrc;
    } else if (!imgSrc) {
        imgSrc = 'https://via.placeholder.com/260';
    }
    document.getElementById('product-modal-body').innerHTML = `
            <div class="text-center"><img src="${imgSrc}" style="max-width:100%; height:260px; object-fit:cover;"></div>
            <p class="mt-3">Price: Rs. ${parseFloat(product.Price).toFixed(2)}</p>
            <p class="small text-muted">Available: ${product.Quantity}</p>
            <p>${product.Name}</p>
        `;

    const modal = document.querySelector('#product-modal .modal');
    modal.style.display = 'block';

    // initialize quantity input and hook add button
    const qtyInput = document.getElementById('product-qty');
    if (qtyInput) { qtyInput.value = 1; qtyInput.min = 1; try { qtyInput.max = parseInt(product.Quantity) || 1; } catch (e) { qtyInput.max = 1; } }

    const addBtn = document.getElementById('add-to-cart-btn');
    addBtn.onclick = function () {
        const qty = parseInt((document.getElementById('product-qty') || { value: 1 }).value) || 1;
        addToCart(product, qty);
    };
}

function closeProductModal() {
    const modal = document.querySelector('#product-modal .modal');
    if (modal) modal.style.display = 'none';
}

async function showProductDetail(uuid) {
    try {
        const resp = await fetch(`/api/products/${uuid}/`);
        if (!resp.ok) throw new Error('Failed to fetch');
        const product = await resp.json();
        showProductModal(product);
    } catch (e) {
        console.error(e);
        alert('Failed to load product details');
    }
}

async function addToCart(product, quantity = 1) {
    // Check if CSRF token exists; if not, auto-logout
    const csrfToken = getCookie('csrftoken');
    if (!csrfToken) {
        alert('Session expired. Please login again.');
        window.location.href = '/accounts/logout';
        return;
    }
    // Try backend cart first (include CSRF token and credentials)
    try {
        const resp = await fetch('/api/cart/items/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: JSON.stringify({ product_uuid: product.uuid, quantity: quantity })
        });
        if (resp.status === 201) {
            alert('Added to cart');
            closeProductModal();
            return;
        }
        if (resp.status === 401) {
            // fallback to localStorage
            addToLocalCart(product, quantity);
            alert('Added to local cart (login to persist)');
            closeProductModal();
            return;
        }
        const data = await resp.json();
        console.log(data);
    } catch (e) {
        console.error(e);
        addToLocalCart(product, quantity);
        alert('Added to local cart');
        closeProductModal();
    }
}

function addToLocalCart(product, quantity = 1) {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const idx = cart.findIndex(it => it.product_uuid === product.uuid);
    if (idx > -1) {
        cart[idx].quantity = (cart[idx].quantity || 0) + quantity;
    } else {
        cart.push({ product_uuid: product.uuid, Name: product.Name, Price: product.Price, Image: product.Image, quantity: quantity });
    }
    localStorage.setItem('cart', JSON.stringify(cart));
}

// CSRF helper to read cookie value
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function loadProductsByCategory() {
    for (const [code, containerId] of Object.entries(categories)) {
        try {
            const response = await fetch(`/api/products/?category=${code}`);
            const data = await response.json();
            const products = data.results || data || [];
            renderProducts(products, containerId);
        } catch (error) {
            console.error(`Error loading category ${code}:`, error);
            document.getElementById(containerId).innerHTML =
                '<div class="col-12 text-center text-danger">Failed to load products</div>';
        }
    }
}

document.addEventListener('DOMContentLoaded', loadProductsByCategory);
