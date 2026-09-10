function filterGoods() {
    const category = document.getElementById('categoryFilter').value;
    const rarity = document.getElementById('rarityFilter').value;
    const stock = document.getElementById('stockFilter').value;
    const sort = document.getElementById('sortFilter').value;
    
    const items = document.querySelectorAll('.goods-item');
    let visibleItems = [];
    
    // Фильтрация
    items.forEach(item => {
        let show = true;
        
        if (category !== 'all' && item.dataset.category !== category) {
            show = false;
        }
        if (rarity !== 'all' && item.dataset.rarity !== rarity) {
            show = false;
        }
        if (stock !== 'all' && item.dataset.stock !== stock) {
            show = false;
        }
        
        item.style.display = show ? 'block' : 'none';
        if (show) visibleItems.push(item);
    });
    
    // Сортировка
    const container = document.getElementById('goodsContainer');
    const itemsArray = Array.from(visibleItems);
    
    itemsArray.sort((a, b) => {
        switch(sort) {
            case 'price_asc':
                return parseInt(a.dataset.price) - parseInt(b.dataset.price);
            case 'price_desc':
                return parseInt(b.dataset.price) - parseInt(a.dataset.price);
            case 'rarity_asc':
                return parseInt(a.dataset.rarityValue) - parseInt(b.dataset.rarityValue);
            case 'rarity_desc':
                return parseInt(b.dataset.rarityValue) - parseInt(a.dataset.rarityValue);
            case 'name_asc':
                return a.querySelector('.good-title').textContent.localeCompare(b.querySelector('.good-title').textContent);
            default:
                return 0;
        }
    });
    
    // Пересортировка DOM
    itemsArray.forEach(item => {
        container.appendChild(item);
    });
    
    // Обновление счетчика
    document.getElementById('itemCount').textContent = `Найдено товаров: ${visibleItems.length}`;
}

function resetFilters() {
    document.getElementById('categoryFilter').value = 'all';
    document.getElementById('rarityFilter').value = 'all';
    document.getElementById('stockFilter').value = 'all';
    document.getElementById('sortFilter').value = 'price_asc';
    filterGoods();
}

// Инициализация
document.addEventListener('DOMContentLoaded', function() {
    filterGoods();
});