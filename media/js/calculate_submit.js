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

  //search results
  $('#search_result_panel').hide();
  $('#valid_results').hide();
  $('#unvalid_results').hide();

  $('#search-loading').hide();
  $("div#commit_content").hide();
});

//raw content copy
$("[rel='raw_content']").change(function(){
  var name = $(this).attr('id') + "_copy";
  //TODO: should check whether the element exists;
  console.log($(this).val());
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
      //alert("visible=false")
      $(this).text("undo this choice");
      $(this).toggleClass("btn-danger");
      $(checked_element).attr("visible", "true");
      $(checked_element).show();
      $(show_element).attr("visible", "true");
      //alert($(show_element).attr("visible"))
      //alert($(checked_element).attr("visible"))
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
   callback(d, "search-api"); 
  },data);

  Dajaxice.gui.search_local(function(d){
   callback(d, "search-local"); 
  },data);


  function callback(data, element){
    element = "#" + element;
    console.log(data);
    $("#search-loading").hide();
    $("#search_result_panel").show();

    if(data.is_searched && data.results.length != 0){
      $(element).find("tbody").html("");
      $.each(data.results, function(k,v){
        var row = "<tr class='search-content'><td>"+ v.cas +"</td><td>"+
                  v.formula + "</td><td>" +
                  v.commonname + "</td><td class='smile'>" +
                  v.smiles + "</td><td>" +
                  v.alogp + "</td>"+
                  "<td><a class='btn btn-primary search-select'>Select</a></td></tr>";
        $(element).find("tbody").append(row);
      });
      
      $(".search-select").click(function(){
        var smile_copy = "#basic_search_add_copy";
        var td = this.parentNode.parentNode;
        var smile = $(td).children(".smile").text();

        $(smile_copy).text(smile);
        $(".search-content").removeClass("alert alert-error");
        $(td).addClass("alert alert-error");
      });
    }else{
      $(element).text("No matching results!");
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



