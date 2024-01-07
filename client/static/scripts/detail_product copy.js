let slideIndex = 1;

$(document).ready(function () {
    showProduct();
    
});


function showProduct() {
    let productId = document.getElementById('productId').value;
    $.ajax({
        url: '/getDetail/'+productId, 
        method: 'GET',
        success: function (response) {
            let containerProduct = $('#detail-product-body');
            let product = response.products[0]; 
            let formattedPrice = new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 });
            let content = `
                <div class="col-md-4" id="image-detail">
                    <div class="container-img">
                        <div class="mySlides">
                            <div class="numbertext">1 / 4</div>
                            <img src="/static/images/product/${product.image}" style="width:100%">
                        </div>
                        <div class="mySlides">
                            <div class="numbertext">2 / 4</div>
                            <img src="/static/images/product/${product.image}" style="width:100%">
                        </div>
                        <div class="mySlides">
                            <div class="numbertext">3 / 4</div>
                            <img src="/static/images/product/${product.image}" style="width:100%">
                        </div>
                        <div class="mySlides">
                            <div class="numbertext">4 / 4</div>
                            <img src="/static/images/product/${product.image}" style="width:100%">
                        </div>

                        <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
                        <a class="next" onclick="plusSlides(1)">&#10095;</a>

                        <div class="caption-container"></div>


                        <div class="container">
                            <div class="row">
                                <div class="column-img">
                                    <img class="demo cursor" src="/static/images/product/${product.image}" style="width:100%" onclick="currentSlide(1)" alt="The Woods">
                                </div>
                                <div class="column-img">
                                    <img class="demo cursor" src="/static/images/product/${product.image}" style="width:100%" onclick="currentSlide(2)" alt="Cinque Terre">
                                </div>
                                <div class="column-img">
                                    <img class="demo cursor" src="/static/images/product/${product.image}" style="width:100%" onclick="currentSlide(3)" alt="Mountains and fjords">
                                </div>
                                <div class="column-img">
                                    <img class="demo cursor" src="/static/images/product/${product.image}" style="width:100%" onclick="currentSlide(4)" alt="Northern Lights">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="col-md-5">
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
                    
                    <!-- Nama Toko  -->
                    <div class="row">
                        <div class="col-auto">
                            <img src="/static/images/placeholder/placeholder-image.png" class="rounded-circle border border-secondary" alt="Deskripsi gambar" style="width: 55px">
                        </div>
                        <div class="col">
                            <p class="text fw-bold">${product.seller_name}</p>
                        </div>
                    </div>
                    <hr class="my-4">  
                </div>

                <div class="col-md-3">
                    <div class="card shadow-sm">
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

                        <div class="card-body">
                            <button class="btn btn-success" id="btn-beli">Beli</button>
                        </div>
                    </div>
                </div>
            `;
        
            containerProduct.append(content);

            showSlides(slideIndex);

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


// Input Junlah Beli
function JumlahBeli(stokBarang, productPrice) {
    const plus = document.querySelector(".plus");
    const minus = document.querySelector(".minus");
    const num = document.querySelector(".num");
    const beliButton  = document.getElementById("#btn-beli");
    const subtotalDisplay = document.querySelector(".subtotal-display");
    const stokBarangElement = document.querySelector(".stok-barang");
    
    let a = 1;
    
    if (stokBarang < 1) {
        $(document).ready(function () {
            beliButton.setAttribute("disabled", true);
        });
    };
    
    plus.addEventListener("click", () => {
      if (a < stokBarang) {
        a++;
        num.innerText = a;
        updateSubtotal();
        updateButtonState();
      }
    });
    
    minus.addEventListener("click", () => {
      if (a > 1) {
        a--;
        num.innerText = a;
        updateSubtotal();
        updateButtonState();
      }
    });
    
    function updateSubtotal() {
        console.log(a)
      if (!isNaN(productPrice)) {
        const totalPrice = a * productPrice;
    
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
        if (a === 1) {
          minus.setAttribute("disabled", true);
        } else {
          minus.removeAttribute("disabled");
        }
      
        if (a === stokBarang) {
          plus.setAttribute("disabled", true);
        } else {
          plus.removeAttribute("disabled");
        }
    
        if (stokBarang === 0) {
            beliButton.setAttribute("disabled", true);
        } else {
            beliButton.removeAttribute("disabled");
        }
      }
    
}
// Input Jumlah Beli END