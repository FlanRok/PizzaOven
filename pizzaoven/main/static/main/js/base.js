const MAX_NOTIFICATIONS = 3;
const NOTIFICATION_DELAY = 4000;

function showNotification(message, isSuccess = true) {
    const container = document.getElementById('notification-container');
    if (!container) return;

    while (container.children.length >= MAX_NOTIFICATIONS) {
        container.removeChild(container.firstChild);
    }

    const notification = document.createElement('div');
    notification.style.cssText = `
        background: ${isSuccess ? '#28a745' : '#dc3545'};
        color: #fff;
        padding: 12px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.3s, transform 0.3s;
        margin-bottom: 8px;
    `;
    notification.textContent = message;
    container.appendChild(notification);

    requestAnimationFrame(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateY(0)';
    });

    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateY(-20px)';
        setTimeout(() => notification.remove(), 300);
    }, NOTIFICATION_DELAY);
}

function updateCartCounter(total) {
    const counterSpan = document.getElementById('cart-quantity');
    if (counterSpan) {
        counterSpan.textContent = total;
        counterSpan.style.display = total > 0 ? 'inline-block' : 'none';
    }
}

function getCSRFToken() {
    const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (tokenInput) return tokenInput.value;
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));
    return cookieValue ? cookieValue.split('=')[1] : '';
}

document.addEventListener('submit', async function (e) {
    const form = e.target.closest('.add-to-cart-form');
    if (!form) return;
    e.preventDefault();

    const formData = new FormData(form);
    const url = form.action;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        });
        const data = await response.json();
        if (data.success) {
            updateCartCounter(data.total_quantity);
            showNotification(data.message || 'Товар добавлен в корзину!', true);
        } else {
            showNotification(data.message || 'Ошибка при добавлении', false);
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Произошла ошибка. Попробуйте позже.', false);
    }
});

function initSizeButtons(container = document) {
    container.querySelectorAll('.card').forEach(card => {
        const sizeButtons = card.querySelectorAll('.size-button');
        const hiddenSizeInput = card.querySelector('.selected-size-input');
        const priceElement = card.querySelector('.card-price');

        sizeButtons.forEach(btn => {
            btn.removeEventListener('click', handleSizeClick);
        });

        function handleSizeClick(e) {
            const btn = e.currentTarget;
            const btns = btn.closest('.card').querySelectorAll('.size-button');
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const selectedSize = btn.dataset.size;
            const selectedPrice = btn.dataset.price;
            if (hiddenSizeInput) hiddenSizeInput.value = selectedSize;
            if (priceElement && selectedPrice) {
                priceElement.textContent = `${selectedPrice} ₽`;
            }
        }

        sizeButtons.forEach(btn => {
            btn.addEventListener('click', handleSizeClick);
        });

        if (sizeButtons.length && !card.querySelector('.size-button.active')) {
            sizeButtons[0].click();
        }
    });
}