function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $('#form-auth').submit(function(e){
        e.preventDefault();
        real_name = $('#real-name').val()
        id_card = $('#id-card').val()
        $.ajax({
            url:'/user/auth/',
            data:{'real_name':real_name, 'id_card': id_card},
            dataType: 'json',
            type: 'post',
            success: function(data){
                if(data.code == '200'){
                    $('.btn-success').hide()
                    $('.form-control').css('disabled', 'disabled')
                }
            },
            error: function(data){
                alert('failed')
            },
        })

    })
})