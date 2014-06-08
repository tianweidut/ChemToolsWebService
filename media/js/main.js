$(function(){ 
  $('a.filter').click(
    function(){
      $("a.filter").removeClass('btn-danger');
      $(this).addClass('btn-danger');
      
      var success_queue = 'ul.tasklist > li.success';
      var failed_queue = 'ul.tasklist > li.failed';
      var inprogress_queue = 'ul.tasklist > li.calculating';
      switch($(this).attr('rel'))
      {
        case 'all':
          $(success_queue).show();
          $(failed_queue).show();
          $(inprogress_queue).show();
          break;
        case 'success':
          $(success_queue).show();
          $(failed_queue).hide();
          $(inprogress_queue).hide();
          break;
        case 'failed':
          $(success_queue).hide();
          $(failed_queue).show();
          $(inprogress_queue).hide();
          break;
        case 'inprogress':
          $(success_queue).hide();
          $(failed_queue).hide();
          $(inprogress_queue).show();
          break;
        default:
          break;
      }
  });
});
