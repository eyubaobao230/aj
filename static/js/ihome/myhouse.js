$(document).ready(function(){
    $(".auth-warn").show();
    $(document).ready(function(){
        $.ajax({
            url:'/house/m_house/',
            type:'GET',
            success:function(data){
                if(data.code == 200){
                     $('.auth-warn').hide();
                     $('#house-list').show();
                }
                if(data.code == 2001){
                     $('.auth-warn').show();
                     $('#house-list').hide();
                }
            }
        })

    })
    $.get('/house/house_info/', function(data){
    if(data.code == '200'){
        $('.auth-warn').hide()
        $('#houses-list').show()
        for(var i=0; i<data.houses.length; i++){
            var house = '<li>'
            house += '<a href="/house/detail/?house_id=' + data.houses[i].id + '">'
            house += '<div class="house-title">'
            house += '<h3>房屋ID:' + data.houses[i].id + '——' + data.houses[i].title + '</h3>'
            house += '</div><div class="house-content">'
            house += '<img src="/static/media/' + data.houses[i].image + '">'
            house += '<div class="house-text"><ul>'
            house += '<li>位于：' + data.houses[i].area + '</li><li>价格：￥' + data.houses[i].price + '/晚</li><li>发布时间：' + data.houses[i].create_time + '</li>'
            house += '</ul></div></div></a></li>'
            $('#houses-list').append(house)
        }
    }
    })
})


