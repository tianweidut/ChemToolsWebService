/**
 * @author tianwei
 * the 
 */

// test code
$('#task_name_id1').change(function(){
  $('#task_name_commit').text($(this).val());
});


//raw content copy
$("[rel='raw_content']").change(function(){
  var name = $(this).attr('id') + "_copy";
  $("#"+name).text($(this).val());
});
