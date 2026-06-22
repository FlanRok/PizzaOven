document.querySelectorAll('.quantity-button').forEach(button => {
    button.addEventListener('click', async function (e) {
        const action = this.classList.contains('increment') ? 'increase' : 'decrease';
        const url = this.dataset.url;
        const orderSection = this.closest('.order-section');
        const cartId = orderSection.dataset.cartId;
        const quantitySpan = orderSection.querySelector('.item-quantity');
        const priceSpan = orderSection.querySelector('.item-price');

        try {
            const formData = new FormData();
            formData.append('action', action);
            formData.append('csrfmiddlewaretoken', getCSRFToken());

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            });
            const data = await response.json();
            if (data.success) {
                if (data.deleted) {
                    orderSection.remove();
                } else {
                    quantitySpan.textContent = data.new_quantity;
                    priceSpan.textContent = `${data.new_item_price} ₽`;
                }

                document.getElementById('cart-total-quantity').textContent = data.total_quantity;
                document.getElementById('cart-total-price').textContent = `${data.total_price} ₽`;
                updateCartCounter(data.total_quantity);

                if (data.total_quantity === 0) {
                    document.querySelector('.cart').innerHTML = '<h2>Ваша корзина пустая</h2>';
                }
            } else {
                showNotification(data.message || 'Ошибка изменения количества', false);
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    });
});

document.querySelectorAll('.remove-button').forEach(button => {
    button.addEventListener('click', async function (e) {
        const url = this.dataset.url;
        try {
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const data = await response.json();
            if (data.success) {
                this.closest('.order-section').remove();
                document.getElementById('cart-total-quantity').textContent = data.total_quantity;
                document.getElementById('cart-total-price').textContent = `${data.total_price} ₽`;
                updateCartCounter(data.total_quantity);
                if (data.total_quantity === 0) {
                    document.querySelector('.cart').innerHTML = '<h2>Ваша корзина пустая</h2>';
                }
            } else {
                showNotification(data.message || 'Ошибка удаления', false);
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    });
});