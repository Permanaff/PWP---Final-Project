let slideIndex = 1;
let user_id = $('#user_id').val()
let product_id = $('#productId').val()

$(document).ready(function () {
    showProduct();
    updateViews(product_id)
    
});


function showProduct() {
    let productId = document.getElementById('productId').value;
    $.ajax({
        url: 'http://127.0.0.1:3000/getDetail/'+productId, 
        method: 'GET',
        success: function (response) {
            let containerProduct = $('#detail-product-body');
            let product = response.products[0]; 
            let formattedPrice = new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 });

            // Menambahakan Image Produk
            const contentImg = `
                <div class="mySlides">
                    <div class="numbertext">1 / 4</div>
                    <img src="/static/images/product/${product.image1}" style="width:100%">
                </div>
                <div class="mySlides">
                    <div class="numbertext">2 / 4</div>
                    <img src="/static/images/product/${product.image2}" style="width:100%">
                </div>
                <div class="mySlides">
                    <div class="numbertext">3 / 4</div>
                    <img src="/static/images/product/${product.image3}" style="width:100%">
                </div>
                <div class="mySlides">
                    <div class="numbertext">4 / 4</div>
                    <img src="/static/images/product/${product.image4}" style="width:100%">
                </div>

                <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
                <a class="next" onclick="plusSlides(1)">&#10095;</a>
                <div class="caption-container"></div>

                <div class="container">
                    <div class="row">
                        <div class="column-img">
                            <img class="demo cursor" src="/static/images/product/${product.image1}" style="width:100%" onclick="currentSlide(1)" alt="The Woods">
                        </div>
                        <div class="column-img">
                            <img class="demo cursor" src="/static/images/product/${product.image2}" style="width:100%" onclick="currentSlide(2)" alt="Cinque Terre">
                        </div>
                        <div class="column-img">
                            <img class="demo cursor" src="/static/images/product/${product.image3}" style="width:100%" onclick="currentSlide(3)" alt="Mountains and fjords">
                        </div>
                        <div class="column-img">
                            <img class="demo cursor" src="/static/images/product/${product.image4}" style="width:100%" onclick="currentSlide(4)" alt="Northern Lights">
                        </div>
                    </div>
                </div>
            `;
            $('#container-img').append(contentImg);

            // Menambahkan Detail Product
            const contentDetail = `
                <h2 class="fs-3 fw-bold">${product.name}</h2>
                <p class="fw-light" style="font-size: 14px">Terjual <span class="text-secondary">${product.terjual}</span></p>
                <p class="fs-3 fw-bold">${formattedPrice.format(product.price)}</p>
                <hr class="my-3">
                <h6 class="m-1" id="detail">Detail</h6>
                <hr class="my-3">
                <div id="displayText">
                    <pre id="desc_product" class="text-justify wrapped-text" style="font-family: monserrat , sans-serif; white-space: pre-wrap;">${product.description}</pre>
                </div>

                <a class="mt-2 mb-3" id="readMoreBtn" href="#detail" style="color: #B31312;">Tampilkan Lebih Banyak</a>
                <a class="mt-2 mb-3" id="readLessBtn" href="#" style="display: none; color: #B31312;">Tampilkan Lebih Sedikit</a>
                <hr class="my-4">
            `
            $('#detail-product').append(contentDetail)


            const contentSeller = `
                <div class="col-auto">
                    <img src="/static/images/profile_image/${product.seller_image}" class="rounded-circle border border-secondary" alt="Deskripsi gambar" style="width: 55px">
                </div>
                <div class="col">
                    <p class="text fw-bold">${product.seller_name}</p>
                </div>
            `;
            $('#nama-toko').append(contentSeller)


            // Menmabahkan content card samping 
            const contentInfo = `
                <div class="card-body">
                    <h5 class="card-title">Jumlah Stok</h5>
                    <p class="card-text stok-barang" data-stok="${product.stok}">${product.stok}</p>
                </div>
                
                <ul class="list-group list-group-flush">
                    <div class="container mt-3 mb-3">
                        <div class="wrapper">
                            <span class="minus">-</span>
                            <span class="num">1</span>
                            <span class="plus">+</span>
                        </div>
                    </div>
                    <div class="container">
                        <div class="row">
                        <div class="col">
                            <p class="fs-6 text-body-secondary mt-1">Subtotal</p>
                        </div>
                        <div class="col">
                            <p class="subtotal-display fs-5 fw-semibold text-end" data-product-price="${formattedPrice.format(product.price)}">${formattedPrice.format(product.price)}</p>

                        </div>
                    </div>
                </ul>

                <div class="card-footer" style="background-color: white;">
                    <div class="row">
                        <button class="btn btn-success" id="btn-beli" onclick="addToCart(${product.id})">Beli</button>
                    </div>
                </div>
            `
            $('#content-info').append(contentInfo)


            // Untuk Menampilkan image
            showSlides(slideIndex);

            // Untuk memperpendek detail product
            var displayText = document.getElementById('displayText');
            textExpand(displayText)
            JumlahBeli(product.stok, product.price)
        },
        error: function (xhr, status, error) {
            console.error('Gagal mengambil data :', error);
        }
    });  
}



// image galery product
function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("demo");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
}
// image galery product END


// Meringkas Deskripsi Barang
function textExpand(displayText) { 
    // var displayText = document.getElementById('displayText');
    var fullText = displayText.innerText;
    var shortTextLength = 250;
    var readMoreBtn = document.getElementById('readMoreBtn');


    if (fullText.length > shortTextLength) {
        displayText.innerText = fullText.substring(0, shortTextLength);

        readMoreBtn.style.display = 'block';

        readMoreBtn.addEventListener('click', function() {
            displayText.innerText = fullText;

            readMoreBtn.style.display = 'none';
            document.getElementById('readLessBtn').style.display = 'block';
        });

        document.getElementById('readLessBtn').addEventListener('click', function() {
            displayText.innerText = fullText.substring(0, shortTextLength);

            this.style.display = 'none';
            readMoreBtn.style.display = 'block';
        });
    } else {
        $('#readMoreBtn').addClass("visually-hidden");

    };

}
// Ringkas Deskripsi PRoduk ENd


// Input Jumlah Beli
function JumlahBeli(stokBarang, productPrice) {
    const plus = document.querySelector(".plus");
    const minus = document.querySelector(".minus");
    const num = document.querySelector(".num");
    const beliButton  = document.querySelector("#btn-beli");
    const subtotalDisplay = document.querySelector(".subtotal-display");
    const stokBarangElement = document.querySelector(".stok-barang");
    
    let beli = 1;
    
    if (stokBarang < 1) {
        $(document).ready(function () {
            beliButton.prop("disabled", true);
        });
    };
    
    plus.addEventListener("click", () => {
      if (beli < stokBarang) {
        beli++;
        num.innerText = beli;
        updateSubtotal();
        updateButtonState();
      }
    });
    
    minus.addEventListener("click", () => {
      if (beli > 1) {
        beli--;
        num.innerText = beli;
        updateSubtotal();
        updateButtonState();
      }
    });
    
    function updateSubtotal() {
      if (!isNaN(productPrice)) {
        const totalPrice = beli * productPrice;
    
        const formatter = new Intl.NumberFormat('id-ID', {
          style: 'currency',
          currency: 'IDR',
          minimumFractionDigits: 0
        });
    
        subtotalDisplay.innerText = formatter.format(totalPrice);
      } else {
        subtotalDisplay.innerText = "Invalid Price";
      }
    }
    
    function updateButtonState() {
        if (beli === 1) {
          minus.setAttribute("disabled", true);
        } else {
          minus.removeAttribute("disabled");
        }
      
        if (beli === stokBarang) {
          plus.setAttribute("disabled", true);
        } else {
          plus.removeAttribute("disabled");
        }
      }
    
}
// Input Jumlah Beli END

// Menambahkan Produk Ke Cart 
function addToCart(productId) { 
    var quantity = parseInt($('.num').text());
    $.ajax({
        url: 'http://127.0.0.1:3000/add-cart/'+user_id, 
        method: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ productId:productId, quantity:quantity }),
        success: function (response) {
            
        }
    });
   
}

function updateViews(product_id) {
    $.ajax({
        url: 'http://127.0.0.1:3000/update-views/'+product_id,
        method: 'POST',  
        success: function (response) {
        }
    }) 
}