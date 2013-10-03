/**
 * @author tianwei
 * the 
 */

var table_data;

$(document).ready(function(){
  $('#response_type_copy > p').hide();
  $('[rel="modified_choice"]').hide();
  $('[rel=label-choice]').hide();
  $("#mol_file_string_copy").hide();

  //search results
  $('#search_result_panel').hide();
  $('#valid_results').hide();
  $('#unvalid_results').hide();

  $('#search-loading').hide();
  $("div#commit_content").hide();
});

$("[rel='raw_content']").change(function(){
  var name = $(this).attr('id') + "_copy";
  //TODO: should check whether the element exists;
  console.log($(this).val());
  $("#"+name).text($(this).val());
});

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

$("[rel='button-switch']").click(function(){
  var show= "#"+ $(this).attr("id") + "_copy";
  var checked="#label_id_" + $(this).attr("model");
 
  if($(checked).attr("visible") === "false")
    {
      $(this).text("undo this choice").toggleClass("btn-danger");
      $(checked).attr("visible", "true").show();
      $(show).attr("visible", "true").show();
    }
  else
    {
      $(this).text("Choice This Model!").toggleClass("btn-danger");
      $(checked).attr("visible", "false").hide();
      $(show).attr("visible", "false").hide(); 
    }
});

$("#model-choice-all").click(function(){
  $("[rel=button-switch]").each(function(){
    var show= "#"+ $(this).attr("id") + "_copy";
    var checked="#label_id_" + $(this).attr("model");
    $(this).text("undo this choice").addClass("btn-danger");
    $(checked).attr("visible", "true").show();
    $(show).attr("visible", "true").show();
  });
});

$("#model-cancel-all").click(function(){
  $("[rel=button-switch]").each(function(){
    var show= "#"+ $(this).attr("id") + "_copy";
    var checked="#label_id_" + $(this).attr("model");
    $(this).text("Choice This Model!").removeClass("btn-danger");
    $(checked).attr("visible", "false").hide();
    $(show).attr("visible", "false").hide(); 
  });
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
          var fid = $(tditem).children().attr("fid");
          table_data[trindex] = fid; 
          console.log(table_data[trindex]);
          //commit 
          $("#fileupload_copy").empty();
          row += '<tr><td fid="'+fid +'">'+str+'</td></tr>';
        }
    });
  }); 
  
  console.log(row);
  $("#fileupload_copy").append(row);
  
  $(this).text("Files Added!");
  $(this).toggleClass("btn-danger");
  $(this).toggleClass("btn-info");

});

//Get Elements
function GetModels(){
  var dct = new Array();
  var index = 0;
  
  $("#models_choice_copy >tbody >tr").each(function(trindex, tritem){
    //alert($(tritem).attr("visible"))
    if($(tritem).attr("visible") === "true")
      {
        var model = $(tritem).attr("model");
        var temperature = $("#temperature_" + model + "_copy").text(); 
        var humidity = $("#humidity_" + model + "_copy").text(); 
        var other = $("#other_" + model + "_copy").text(); 

        var args = temperature + ";" + humidity + ";" + other;
        dct[index] = model + ";" + args;

        index ++;

      }
  });
  
  console.log(dct);

  return dct;
}

function GetUniqueNames(){
  var str = "";
  var i =0 ;

  if(table_data === undefined)
    {
      return str;
    }

  for(i=0;i<table_data.length;i++)
  {
    str += table_data[i] + ";";
  }

  console.log(str);

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

function calculate_callback(data){
  console.log(data.message);
  if(data.is_submitted === true)
    {
      window.location.href="/history/";
    }
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
          "email":$("#commit_email_copy").text(),
          "types":types,
          "unique_names":unique_names,
          "models":models,
  };

  console.log(data);

  Dajaxice.gui.calculate_submit(calculate_callback ,data);


});

$('#search_varify_btn').click(function(){
  data = {
          "query":$("#query_input").val(),
  };
  
  console.log(data);
  
  $('#search-loading').show();

  Dajaxice.gui.search_varify_info(function(d){
   callback(d); 
  },data);

  function callback(d){
    console.log(d);
    //show the results
    console.log(d.is_searched);
    if(d.is_searched === true)
      {
        $("#search_result_panel").show();
        $('#search-loading').hide();
        if(d.search_result.is_valid === true)
          {
            $('#valid_results').show();
            $('#unvalid_results').hide();
            $('#last_picture').attr('src', d.search_result.content.imagepath);
            $('#xlogp').text(d.search_result.content.xlogp); 
            $('#alogp').text(d.search_result.content.alogp); 
            $('#molecular_weight').text(d.search_result.content.molecularweight); 
            $('#mf').html(d.search_result.content.mf); 
            $('#std_inchikey').text(d.search_result.content.inchikey); 
            $('#std_inchi').text(d.search_result.content.inchi); 
            $('#last_smile').text(d.search_result.content.smiles); 
            $('#common_name').text(d.search_result.content.commonname); 
            $('#mono_mass').text(d.search_result.content.monoisotopicmass); 
            $('#average_mass').text(d.search_result.content.averagemass); 
          }
        else
          {
            $('#valid_results').hide();
            $('#unvalid_results').show();
          }
      }
  }
});

$("#commit-show-btn").click(function(){
  if($(this).attr("visible")==="false")
    {
      $("div#commit_content").hide();
      $(this).text("Show");
      $(this).toggleClass("btn-primary");
      $(this).toggleClass("btn-info");
      $(this).attr("visible","true"); 
    }
  else
    {
      $("div#commit_content").show();
      $(this).text("Hide");
      $(this).toggleClass("btn-primary");
      $(this).toggleClass("btn-info");
      $(this).attr("visible","false"); 
    }
});
