/**
 * @author tianwei
 * the 
 */

// inital hide
$(document).ready(function(){
  $('#response_type_copy > p').hide();
  $('[rel="modified_choice"]').hide();
  $('[rel=label-choice]').hide();
  $("#mol_file_string_copy").hide();
});

//raw content copy
$("[rel='raw_content']").change(function(){
  var name = $(this).attr('id') + "_copy";
  //TODO: should check whether the element exists;
  $("#"+name).text($(this).val());
});

//raw choice copy
$("[rel='raw_choice']").change(function(){
  var name = $(this).attr("id") + "_selected";
  if($(this).attr("checked") === "checked")
    {
      $("#" + name).show();
    }
  else
    {
      $("#" + name).hide();
    }
});

// modified choice copy, it means KOA, KOF ,... model choice
$("[rel='button-switch']").click(function(){
  var show_element = "#"+ $(this).attr("id") + "_copy";
  var model = $(this).attr("model");
  var checked_element ="#label_id_" + model;
  var temperature_element = "#temperature__" + model; 
  var humidity_element = "#humidity_" + model; 
  var other_element = "#other_" + model; 
 
  if($(checked_element).attr("visible") === "false")
    {
      $(this).text("undo this choice");
      $(this).toggleClass("btn-danger");
      $(checked_element).attr("visible", "true");
      $(checked_element).show();
      $(show_element).attr("visible", "true");
      $(show_element).show();
    }
  else
    {
      $(this).text("Please choice");
      $(this).toggleClass("btn-danger");
      $(checked_element).attr("visible", "false");
      $(checked_element).hide();
      $(show_element).attr("visible", "false");
      $(show_element).hide(); 
    }
});

$('#basic_search_add').click(function(){
  var smile_element = $('#last_smile');
  var pic_element = $('#last_picture');
  var smile_copy = "#" + smile_element.attr("id") + "_copy";
  var pic_copy = "#" + pic_element.attr("id") + "_copy";

  $(smile_copy).text(smile_element.text());
  $(pic_copy).attr("src", pic_element.attr("src"));
  
  $(this).text("Added!");
  $(this).toggleClass("btn-primary");
  $(this).toggleClass("btn-danger");
});

$(document).ready(function(){
    var editor = chemwriter.loadEditor('editor', {
			    enableClipboard: true,
			    appletPath:      "{{ STATIC_URL }}chemwriter/chemwriter-util.jar"
		});
    
    $('#draw_btn').click(function(){
      var mol_string = editor.getMolfile();
      
      $("#mol_string_flag").text("The mol string has already been added!");
      $("#mol_file_string_copy").attr("loaded","true");
      $("#mol_file_string_copy").text(mol_string);

      $(this).text("Added!");
      $(this).addClass("btn-danger");
    });
});


