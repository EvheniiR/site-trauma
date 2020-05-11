$(function() {
    $(window).scroll(function() {
        if ($(this).scrollTop() != 0) {
            $('#toTop').fadeIn();
        } else {
            $('#toTop').fadeOut();
        }
    });

    $('#toTop').click(function() {
        $('body,html').animate({
            scrollTop: 0
        }, 800);
    });
});


/*$('#send_data_{{ item.product_id }}').click(function(event) {
    event.preventDefault();
    data = {
        product_id : $('#product_id_{{ item.product_id }}').val(),
        count : 1 
    };
    $.ajax({
        type : 'POST',
        url : '/add_to_cart',
        data : JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json'
    });  
});*/

function addToCart(product_id, count) {
    data = {
        product_id : product_id,
        count : count 
    };
    $.ajax({
        type : 'POST',
        url : '/add_to_cart',
        data : JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json'
    });        
};