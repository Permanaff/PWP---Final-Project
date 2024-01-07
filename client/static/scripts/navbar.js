let id_user = $('#user_id').val()
$(document).ready(function() {
    $.ajax({
        url: 'http://127.0.0.1:3000/get-data-cart/'+ id_user, 
        method: 'GET',
        dataType: 'json',
        success: function (response) {
            if (response && response.length > 0) {
                var cartData = response[0].cart;
                var quantityTotal = response[2].quantityTotal;
                $("#jml-cart").text(quantityTotal);

            } 
        }

    })


    
});


