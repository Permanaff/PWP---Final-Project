
$(document).ready(function () {
    
    showProduct(); 
});

function showProduct() {
    $.ajax({
        url: 'http://127.0.0.1:3000/get_Product', 
        method: 'GET',
        success: function (response) {
            let containerProduct = $('#daftar-produk');
            let containerProductPopuler = $('#produk-populer');
            let product_populer = '';
            let content = '';
            let formattedPrice = new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 });

            $.each(response.populer, function (index, populer) {
                product_populer +=`
                    <a href="/detail-product/${populer.id}" style="text-decoration: none">
                        <div class="card h-100 shadow-sm" style="width: 12rem; height: 18rem;">
                            <img src="/static/images/product/${populer.image}" class="card-img-top img-fluid" alt="product-image" placeholder="/static/images/placeholder/placeholder-image.png">
                            <div class="card-body">
                                <h5 class="card-text fs-6 text-truncate">${populer.name}</h5>
                                <p class="card-text fs-5 fw-bold">${formattedPrice.format(populer.price)}</p>
                                <p class="card-text fw-light" style="font-size: 14px;">${populer.terjual} terjual</p>
                            </div>
                        </div>  
                    </a>
                `;
            });
            
            containerProductPopuler.append(product_populer);

            $.each(response.products, function (index, product) {
                content +=`
                    <a href="/detail-product/${product.id}" style="text-decoration: none">
                        <div class="card h-100 shadow-sm" style="width: 12rem; height: 18rem;">
                            <img src="/static/images/product/${product.image}" class="card-img-top img-fluid" alt="product-image" placeholder="/static/images/placeholder/placeholder-image.png">
                            <div class="card-body">
                                <h5 class="card-text fs-6 text-truncate">${product.name}</h5>
                                <p class="card-text fs-5 fw-bold">${formattedPrice.format(product.price)}</p>
                                <p class="card-text fw-light" style="font-size: 14px;">${product.terjual} terjual</p>
                            </div>
                        </div>  
                    </a>
                `;
            });
            
            containerProduct.append(content);
        },

        error: function (xhr, status, error) {
            console.error('Gagal mengambil data :', error);
        }
    });  
}
