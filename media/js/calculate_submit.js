/**
 * @author tianwei
 * the 
 */
$(document).ready(function(){
  $('#response_type_copy > p').hide();
});

//raw content copy
$("[rel='raw_content']").change(function(){
  var name = $(this).attr('id') + "_copy";
  $("#"+name).text($(this).val());
});

//raw choice copy
$("[rel='raw_choice']").change(function(){
  var name = $(this).attr("id") + "_selected";
  if($(this).attr("checked") == "checked")
    {
      $("#" + name).show();
    }
  else
    {
      $("#" + name).hide();
    }
});
