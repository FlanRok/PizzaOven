let allCards = [];
function cacheCards() {
    allCards = Array.from(document.querySelectorAll('.card'));
}

function applyFiltersAndSort() {
    const category = document.getElementById('filterCategory').value;
    const spicy = document.getElementById('filterSpicy').checked;
    const vegetarian = document.getElementById('filterVegetarian').checked;
    const popular = document.getElementById('filterPopular').checked;
    const newPizza = document.getElementById('filterNew').checked;
    const sortBy = document.getElementById('sortSelect').value;

    let filtered = allCards.filter(card => {
        if (category !== 'all' && card.dataset.category !== category) return false;
        if (spicy && card.dataset.spicy !== 'true') return false;
        if (vegetarian && card.dataset.vegetarian !== 'true') return false;
        if (popular && card.dataset.popular !== 'true') return false;
        if (newPizza && card.dataset.new !== 'true') return false;
        return true;
    });

    if (sortBy === 'price_asc') {
        filtered.sort((a, b) => parseFloat(a.dataset.price30) - parseFloat(b.dataset.price30));
    } else if (sortBy === 'price_desc') {
        filtered.sort((a, b) => parseFloat(b.dataset.price30) - parseFloat(a.dataset.price30));
    } else if (sortBy === 'name_asc') {
        filtered.sort((a, b) => a.dataset.name.localeCompare(b.dataset.name));
    } else if (sortBy === 'name_desc') {
        filtered.sort((a, b) => b.dataset.name.localeCompare(a.dataset.name));
    } else {
        filtered.sort((a, b) => allCards.indexOf(a) - allCards.indexOf(b));
    }

    const wrapper = document.querySelector('.cards-wrapper');
    wrapper.innerHTML = '';
    filtered.forEach(card => wrapper.appendChild(card.cloneNode(true)));

    initSizeButtons();
}

function resetFilters() {
    document.getElementById('filterCategory').value = 'all';
    document.getElementById('filterSpicy').checked = false;
    document.getElementById('filterVegetarian').checked = false;
    document.getElementById('filterPopular').checked = false;
    document.getElementById('filterNew').checked = false;
    document.getElementById('sortSelect').value = 'default';
    applyFiltersAndSort();
}

document.addEventListener('DOMContentLoaded', () => {
    cacheCards();
    initSizeButtons();

    const controls = ['filterCategory', 'filterSpicy', 'filterVegetarian', 'filterPopular', 'filterNew', 'sortSelect'];
    controls.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', applyFiltersAndSort);
    });

    const resetBtn = document.getElementById('resetFilters');
    if (resetBtn) resetBtn.addEventListener('click', resetFilters);
});


const modalElement = document.querySelector('.modal');
document.querySelector('.cards-wrapper').addEventListener('click', (event) => {
    const cardElement = event.target.closest('.card');
    if (!cardElement || event.target.tagName !== 'IMG') return;

    const slug = cardElement.dataset.slug;
    const name = cardElement.querySelector('.card-name').textContent;
    const description = cardElement.querySelector('.card-info').textContent;
    const price30 = cardElement.dataset.price30;
    const price35 = cardElement.dataset.price35;
    const price40 = cardElement.dataset.price40;
    const imgSrc = cardElement.querySelector('.card-wrapper-img img').src;
    const originalForm = cardElement.querySelector('.add-to-cart-form');
    const actionUrl = originalForm.getAttribute('action');

    modalElement.innerHTML = `
        <button class="close-modal-button">x</button>
        <div class="card-content">
            <div class="card-wrapper-img">
                <img src="${imgSrc}" alt="${name}">
            </div>
            <div class="card-name-wrapper">
                <div class="card-name">${name}</div>
                <div class="card-price">${price30} ₽</div>
            </div>
            <div class="card-info">${description}</div>
        </div>
        <div class="card-sizes-wrapper">
            <div class="card-sizes">
                <button class="size-button" data-size="30" data-price="${price30}">30см</button>
                <button class="size-button" data-size="35" data-price="${price35}">35см</button>
                <button class="size-button" data-size="40" data-price="${price40}">40см</button>
            </div>
            <div class="card-cart">
                <form class="add-to-cart-form" action="${actionUrl}" method="post">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRFToken()}">
                    <input type="hidden" name="size" class="selected-size-input" value="30">
                    <button type="submit" class="to-cart-button">В корзину</button>
                </form>
            </div>
        </div>
    `;

    modalElement.classList.add('modal-open');

    const modalSizeButtons = modalElement.querySelectorAll('.size-button');
    const modalHiddenSize = modalElement.querySelector('.selected-size-input');
    const modalPriceElement = modalElement.querySelector('.card-price');

    modalSizeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            modalSizeButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            modalHiddenSize.value = btn.dataset.size;
            if (modalPriceElement) {
                modalPriceElement.textContent = `${btn.dataset.price} ₽`;
            }
        });
    });
    if (modalSizeButtons.length) modalSizeButtons[0].click();

    modalElement.querySelector('.close-modal-button').addEventListener('click', () => {
        modalElement.classList.remove('modal-open');
    });
});