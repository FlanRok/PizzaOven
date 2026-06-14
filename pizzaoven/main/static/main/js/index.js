 document.querySelectorAll('.card').forEach(card => {
        const sizeButtons = card.querySelectorAll('.size-button');
        const hiddenSizeInput = card.querySelector('.selected-size-input');

        sizeButtons.forEach(button => {
            button.addEventListener('click', function () {
                sizeButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');

                const selectedSize = this.dataset.size;
                const selectedPrice = this.dataset.price;

                hiddenSizeInput.value = selectedSize;

                const priceElement = this.closest('.card').querySelector('.card-price')
                if (priceElement && selectedPrice) {
                    priceElement.textContent = `${selectedPrice} ₽`
                }
            });
        });

        if (sizeButtons.length > 0) {
            sizeButtons[0].click();
        }
    });

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function updateCartCounter(total) {
        const counterSpan = document.getElementById('cart-quantity');
        if (counterSpan) {
            counterSpan.textContent = total;
            counterSpan.style.display = total > 0 ? 'inline-block' : 'none';
        }
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
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            });
            const data = await response.json();
            if (data.success) {
                updateCartCounter(data.total_quantity);
            } else {
                alert(data.message || 'Ошибка');
            }
        } catch (error) {
            console.error('Ошибка:', error);
        }
    });