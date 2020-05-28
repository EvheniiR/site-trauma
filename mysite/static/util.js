(function() {
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


function addToCart(user_id, product_id) {
    var counter_id = '#item_counter_' + product_id.toString();
    var count = $(counter_id).val();   
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


function removeFromCart(user_id, product_id) {
    data = {
        user_id : user_id,
        product_id : product_id
    };
    $.ajax({
        type : 'POST',
        url : '/remove_from_cart',
        data : JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json'
    });
};


function refreshCartCounter(users_shopping_cart) {
    var count = shoppingCart.length;
    $('#cart_counter').val(count);
};


$(document).ready(function() {
    $('.minus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function () {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });
});







