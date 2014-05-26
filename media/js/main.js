$(function () {
    $('.tree li:has(ul)').addClass('parent_li').find(' > span');
    $('.tree li.parent_li > span').on('click', function (e) {
        var children = $(this).parent('li.parent_li').find(' > ul > li');
        if (children.is(":visible")) {
            children.hide();
            $(this).find(' > i').addClass('glyphicon-plus-sign').removeClass('glyphicon-minus-sign');
        } else {
            children.show();
            $(this).find(' > i').addClass('glyphicon-minus-sign').removeClass('glyphicon-plus-sign');
        }
        e.stopPropagation();
    });
});


$(function () {
    $('.model-args').hide(); 

    $('.checkbox').click(function(){
      var model_args = $('#' + $(this).attr('model') + '_args'); 
      if($(this).find('input[type=checkbox]').is(':checked')){
        model_args.hide();
      }else{
        model_args.show();
      }
    });
});
