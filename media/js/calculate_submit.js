/**
 * @author tianwei
 * the 
 */

// inital hide

var table_data;

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
      $("#" + name).attr("visible", "true");
    }
  else
    {
      $("#" + name).hide();
      $("#" + name).attr("visible", "false");
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

$("#upload_update").click(function(){
  table_data =new Array();
  var row = "";
  $("#files_table tr").each(function(trindex, tritem){
    $(tritem).find("td").each(function(tdindex, tditem){
      if($(tditem).attr("class") === "name")
        {
          var str = $(tditem).children().text();
          table_data[trindex] = $(tditem).children().text();
          //commit 
          $("#fileupload_copy").empty();
          row += '<tr><td>'+str+'</td></tr>';
        }
    });
  }); 
  
  console.log(row);
  $("#fileupload_copy").append(row);

});

//Get Elements
function GetModels(){
  var dct = "";

  return dct;
}

function GetUniqueNames(){
  var str = "";
  var i =0 ;

  for(i=0;i<table_data.length;i++)
  {
    str += table_data[i] + ";";
  }

  return str;
}

function GetResponseTypes(){
  var str = "";
  
  $("#response_type_copy").find("p").each(function(index, item){
    if($(item).attr("visible") === "true")
      {
        str += $(item).text() + ";";
      }
  });

  return str;
}

// Ajax for calcualte submit
$('#commit-saved-btn').click(function(){
  // Get calculated submit infomation
  // Arguments Defination:
  //   * smile: smile name
  //   * mol: it is mol string which is from ChemWrite
  //   * notes: calculated task note
  //   * name: calculated task name, which will be uniqued in backend
  //   * unique_names: an array, which are the unique filenames from fileupload
  //   * types: response file type: pdf, csv, txt
  //   * models: a JSON dict, which is the model and it arguments 
  
  types = GetResponseTypes();
  unique_names = GetUniqueNames();
  models = GetModels();

  data = {
          "smile":$("#last_smile_copy").text(),
          "mol":$("#mol_file_string_copy").text(),
          "notes":$("#commit_notes_copy").text(),
          "name":$("#commit_name_copy").text(),
          "types":types,
          "unique_names":unique_names,
          "models":models,
  };

  console.log(data);

  Dajaxice.gui.calculate_submit(function(d){
    alert(d.message);
  },data);
});


