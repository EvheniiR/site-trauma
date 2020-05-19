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


function addToCart(user_id, product_id, count) {
    data = {
        user_id : user_id,
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


function removeFromCart(user_id, product_id, count) {
    data = {
        user_id : user_id,
        product_id : product_id,
        count : count
    };
    $.ajax({
        type : 'POST',
        url : '/remove_from_cart',
        data : JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json'
    });
};







