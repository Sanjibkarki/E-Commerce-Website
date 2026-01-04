// Page script: load category products and provide UI helpers

const categories = {
    'E': 'electronics-container',
    'F': 'fashion-container',
    'A': 'accessories-container',
    'W': 'wearables-container',
    'C': 'computers-container'
};

function renderProducts(products, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return; // nothing to render here

    if (!products || products.length === 0) {
        container.innerHTML = '<div class="col-12 text-center text-muted">No products available</div>';
        return;
    }

    let html = '';
    products.forEach(product => {
        let imgSrc = product.Image || '';
        if (imgSrc && !/^https?:\/\//i.test(imgSrc)) {
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

function safeSetContainerError(containerId, message) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = `<div class="col-12 text-center text-danger">${message}</div>`;
}

async function fetchCategory(code) {
    const url = `/api/products/?category=${code}`;
    try {
        const resp = await fetch(url, { credentials: 'same-origin' });
        if (!resp.ok) {
            throw new Error(`HTTP ${resp.status}`);
        }
        const data = await resp.json();
        const products = data.results || data || [];
        return products;
    } catch (err) {
        console.error('Failed to fetch', url, err);
        return { error: err };
    }
}

async function loadProductsByCategory() {
    console.log('Loading products by category...');
    for (const [code, containerId] of Object.entries(categories)) {
        const result = await fetchCategory(code);
        if (!result) {
            safeSetContainerError(containerId, 'Failed to load products');
            continue;
        }
        if (result.error) {
            safeSetContainerError(containerId, 'Failed to load products');
            continue;
        }
        renderProducts(result, containerId);
    }
}

// Expose helpers for other scripts
window.showProductDetail = window.showProductDetail || function(uuid) {
    console.warn('showProductDetail called before definition:', uuid);
};

document.addEventListener('DOMContentLoaded', loadProductsByCategory);
