function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000)

    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $('#form-name').submit(function(e){
        e.preventDefault();
        user_name = $('#user-name').val()
        $.ajax({
            url:'/user/user_name/',
            type:'PATCH',
            dataType:'json',
            data:{'user_name':user_name},
            success:function(data){
                console.log(data)
                if(data.code == '200'){
                    location.href = '/user/my/'
                }

            }
        })
    })
   $('#form-avatar').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/user/user_avatar/',
            dataType: 'json',
            type: 'PATCH',
            success: function(data){
                if(data.code == '200'){
                    $('#user-avatar').attr('src', '/static/media/' + data.avatar)
                    location.href = '/user/my/'
                }
            },
        })
   })

})
