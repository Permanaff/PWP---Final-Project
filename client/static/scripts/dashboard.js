
// function toggleDashboard(activeDashboard) {
//     var listItems = document.querySelectorAll('li');
//     listItems.forEach(function(item) {
//         item.classList.remove('active');
//     });
//     console.log(activeDashboard - 1)
//     listItems[activeDashboard - 1].classList.add('active');
    
// }
const seller_id = $('#seller_id').val()

function TokoAnda(){
    let contentCard = $('.main-content')
    contentCard.empty()

    let content = `
    <div class="d-flex">
        <div class="container mt-5">
            <div class="card shadow-sm border-1 rounded-0" id="profil-seller">
                <div class="card-body" id="">

                    <h3 class="fs-5 fw-bold" id="teks-profil">Toko Saya</h3>
                    <hr class="mb-1">
                    <button class="btn btn-custom" id="btnDetail">Detail</button>
                    <button class="btn btn-custom" id="btnWaktu">Waktu Buka</button>
                    <hr class="mt-1">
                    
                    <div class="container ms-3">
                        <div class="row" id="contentProfil"></div>
                    <div>
                </div>
            </div>
        </div>
    </div>
    `
    contentCard.append(content);
    profile_seller()

    $(document).ready(function () {
        $('#btnDetail').addClass('border-0').attr("disabled", true)
    
        $('#btnDetail').click(function (event) {
            event.preventDefault();
            $('#contentProfil').empty();
            $('#btnDetail').addClass('border-0').attr("disabled", true)
            $('#btnWaktu').removeClass('border-0').removeAttr("disabled")   
            profile_seller()
        });
        $('#btnWaktu').click(function (event) {
            event.preventDefault();
            $('#contentProfil').empty();
            $('#btnWaktu').addClass('border-0').attr("disabled", true)
            $('#btnDetail').removeClass('border-0').removeAttr("disabled")
            contentWaktuBuka()
    
        });
    });
    
}


// function profile_seller() {
//     $.ajax({
//         url: 'http://127.0.0.1:3000/getSeller',
//         type: 'GET',
//         dataType: 'json',
//         success: function(data) {
//             var contentCard = $('#contentProfil')
//             var seller = data.sellerProfil[0]

//             var content = `
//             <div class="col-8" >
//                 <form class="ms-2" id="formWaktuBuka" method="POST" enctype="multipart/form-data">
//                     <div class="form-group mt-3" id="nama">
//                         <div class="row">
//                             <div class="col-2">
//                                 <label class="fs-6" for="name" style="color: #777795;">Nama Toko</label>
//                             </div>
//                             <div class="col-md-10">
//                                 <input  class="form-control rounded-0" type="text" name="name" id="name" value="${seller.name}" >
//                             </div>
//                         </div>
//                     </div>

//                     <div class="form-group mt-4">
//                         <div class="row">
//                             <div class="col-2">
//                                 <label for="name" style="color: #777795;">Nomor Telpon</label>
//                             </div>
//                             <div class="col-5">
//                                 <p class="">nomor telpon</p>
//                             </div>
//                         </div>
//                     </div>

//                     <div class="form-group mt-4">
//                         <div class="row">
//                             <div class="col-2">
//                                 <label for="name" style="color: #777795;">Alamat</label>
//                             </div>
//                             <div class="col-10">
//                                 <p class="">${seller.alamat_lengkap}, ${seller.provinsi}, ${seller.kota}, ${seller.kecamatan}</p>
//                             </div>
//                         </div>
//                     </div>
                    
//                     <div class="form-group mt-4">
//                         <div class="row">
//                             <div class="col-2">
//                                 <label for="name" style="color: #777795;">Hari Buka</label>
//                             </div>
//                             <div class="col-10" id="daftrWaktuBuka"> 
//                                 <p class="text-secondary fs-6" id="hariBukaList"></p>
//                             </div>
//                         </div>
//                     </div>

//                     <div class="form-group mt-3 mb-4" >
//                         <div class="row">
//                             <div class="col"></div>
//                             <div class="col-sm-10">
//                                 <button type="submit" class="btn btn-primary">Simpan</button>
//                             </div>
//                         </div>
//                     </div>

//                 </form>
//             </div>
//             <div class="col-1">
//                 <div class="vertical-line-2 "></div>
//             </div>
//             <div class="col-auto text-center">
//                 <img src="/static/images/placeholder/placeholder-image.png" class="rounded-circle border border-secondary" alt="Deskripsi gambar" style="width: 120px">

//                 <div class="mt-5">
//                     <input type="file" class="form-control visually-hidden" id="imageUpload" name="image">
//                     <button type="button" class="btn btn-sm btn-primary" onclick="document.getElementById('imageUpload').click()">Pilih Gambar</button>
//                 </div>
//             </div>
//             `
//             contentCard.append(content)

//             var hariBukaList = document.getElementById('hariBukaList');

//             var hariBukaArray = JSON.parse(seller.waktu_buka);
    
//             var hariBukaHTML = '';
//             var hariBukaHTML = '<ul class="list-unstyled">';
//             hariBukaArray.forEach(function(hari) {
//                 hariBukaHTML += '<li class="mb-2">' + hari + ' ' + seller.jamBuka + '-' + seller.jamTutup + '</li>';
//             });
//             hariBukaHTML += '</ul>';
//             hariBukaList.innerHTML = hariBukaHTML;


//         },
//         error: function(error) {
//             console.error('Error fetching data:', error);
//         }
//         });
// }


// function contentWaktuBuka() {
//     $.ajax({
//         url: 'http://127.0.0.1:3000/getSeller',
//         type: 'GET',
//         dataType: 'json',
//         success: function(data) {
//             var contentCard = $('#contentProfil')
//             var seller = data.sellerProfil[0]

//             var content = `
//             <div class="col-8" >
//                 <form class="ms-2" action="simpanWaktuBuka" method="POST" enctype="multipart/form-data">
//                     <div class="form-group mt-4">
//                         <div class="row">
//                             <div class="col-2">
//                                 <label for="name" style="color: #777795;">Jam Buka</label>
//                             </div>
//                             <div class="col-md-6 d-flex">
//                                 <select class="form-select rounded-0" id="time-open" name="time-open" style="width: 500px;"></select>
//                                 <select class="form-select rounded-0 ms-2" id="time-close" name="time-close" style="width: 500px;"></select>
//                             </div>
//                         </div>
//                     </div>
                    
//                     <div class="form-group mt-4">
//                         <div class="row">
//                             <div class="col-2">
//                                 <label for="name" style="color: #777795;">Hari Buka</label>
//                             </div>
//                             <div class="col-md-4 d-flex" id="select-hari-buka">
//                                 <!-- Select Hari Buka -->
//                             </div>
//                         </div>
//                     </div>

//                     <div class="form-group mt-3 mb-4" >
//                         <div class="row">
//                             <div class="col"></div>
//                             <div class="col-sm-10">
//                                 <button type="submit" class="btn btn-primary">Simpan</button>
//                             </div>
//                         </div>
//                     </div>

//                 </form>
//             </div>
//             `
//             contentCard.append(content)
            

//             var jamBuka = $("#time-open");
//             var jamTutup = $("#time-close");
        
//             for (var i = 0; i <= 23; i++) {
//                 var hour = (i < 10) ? '0' + i : i;
//                 jamBuka.append($('<option>',{
//                     value: hour + ":00",
//                     text : hour + ":00" 
//                 }));
//             }
            
//             for (var i = 0; i <= 23; i++) {
//                 var hour = (i < 10) ? '0' + i : i;
//                 jamTutup.append($('<option>',{
//                     value: hour + ":00",
//                     text : hour + ":00"
//                 }));
//             }
   


//             var hariBuka = $('#select-hari-buka');
//             var hari = ['Senin', 'Selasa', 'Rabu', "Kamis", 'Jumat', 'Sabtu', 'Minggu'];
        
//             var content = '';
        
//             $.each(hari, function(index, value) {
//                 content += `
//                     <input type="checkbox" name="day_open" class="btn-check" value="${value}" id="btn-check-${value}" autocomplete="off">
//                     <label class="btn ms-1 "Sabtu""  for="btn-check-${value}">${value}</label>
//                 `
//             });
        
//             hariBuka.append(content)
//         },
//         error: function(error) {
//             console.error('Error fetching data:', error);
  
//         }
//         });
// }