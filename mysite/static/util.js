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


$(document).ready(function() {
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
    }).done(function(data) {
    var s_cart =  data["users_shopping_cart"];
    var s_cart_length = Object.keys(s_cart).length;
    $("#cart_counter").html(s_cart_length);        
    });
};


function removeFromCart(user_id, product_id, positions_amount) {
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
    }).done(function(data) {
        var position_id = '#position_' + product_id.toString();
        $(position_id).remove();
        var s_cart =  data["users_shopping_cart"];
        var s_cart_length = Object.keys(s_cart).length;
        $("#cart_counter").html(s_cart_length);
        if (s_cart_length == 0) {
            $('.full_cart').remove();
            var s_cart_is_empty = 
            "<div class='empty_cart'>" +
                "<h3>Ваша корзина, к сожалению, пуста!</h3>" +
                "<a href='/'>" +
                    "<button>Вернуться к покупкам!</button>" +
                "</a>" +
            "</div>";
            $('.shopping-cart-content').append(s_cart_is_empty);
        };
    });
};








