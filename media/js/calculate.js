/**
 * @author tianwei
 */

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
  $("#calculate-submit-info").hide();
});


$(function(){
  $("#commit_email").change(function(){
    Calculate.email = $(this).val();
  });
  $("#commit_name").change(function(){
    Calculate.task_name = $(this).val();
  });
  $("#commit_notes").change(function(){
    Calculate.notes = $(this).val();
  });
});

//model choice
$(function(){


  $("[rel='button-switch']").click(function(){
    var checked="#label_id_" + $(this).attr("model");
 
    if($(checked).attr("visible") === "false"){
        $(this).text("undo this choice").toggleClass("btn-danger");
        $(checked).attr("visible", "true").show();
    }else{
        $(this).text("Choice This Model!").toggleClass("btn-danger");
        $(checked).attr("visible", "false").hide();
    }
  });

  $("#model-choice-all").click(function(){
    $("[rel=button-switch]").each(function(){
      var checked="#label_id_" + $(this).attr("model");
      $(this).text("undo this choice").addClass("btn-danger");
      $(checked).attr("visible", "true").show();
    });
  });

  $("#model-cancel-all").click(function(){
    $("[rel=button-switch]").each(function(){
      var checked="#label_id_" + $(this).attr("model");
      $(this).text("Choice This Model!").removeClass("btn-danger");
      $(checked).attr("visible", "false").hide();
    });
  });
});

//chem structure draw
$(function(){
    var editor = chemwriter.loadEditor('editor', {
			    enableClipboard: true,
			    appletPath:      "{{ STATIC_URL }}chemwriter/chemwriter-util.jar"
		});
    
    $('#draw_btn').click(function(){
      Calculate.draw_mol = editor.getMolfile();
      $(this).text("Added!").addClass("btn-danger");
    });
});


$("#upload_update").click(function(){
  Calculate.files = [];

  $("#files_table tr").each(function(trindex, tritem){
    $(tritem).find("td").each(function(tdindex, tditem){
      if($(tditem).attr("class") === "name")
        {
          Calculate.files[trindex] = $(tditem).children().attr("fid"); 
        }
    });
  }); 
  
  $(this).text("Files Added!")
         .toggleClass("btn-danger").toggleClass("btn-info");

});

function update_model(){
  Calculate.models = {};
  $("[rel=button-switch]").each(function(){
    var model = $(this).attr("model");
    var checked="#label_id_" + model; 
    var temp = "#temperature_" + model;
    if($(checked).attr("visible") === "true"){
      Calculate.models[model] = {};
      Calculate.models[model]["temperature"]= $(temp).val();
    }
  });
  console.log(Calculate.models);
}

$('#commit-saved-btn').click(function(){
  update_model();
  data = {
          "smile":Calculate.smile,
          "draw_mol":Calculate.draw_mol,
          "notes":Calculate.notes,
          "task_name":Calculate.task_name,
          "email":Calculate.email,
          "files":Calculate.files,
          "models":Calculate.models,
         };

  Dajaxice.gui.calculate_submit(calculate_callback ,data);
  
  function calculate_callback(data){
    if(data.is_submitted){
      window.location.href="/history/";
    }else{
      $("#calculate-submit-info").show().text(data.message);
    }
  }
});

$('#search_varify_btn').click(function(){
  data = {
          "query":$("#query_input").val(),
  };
  
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

    if(data.is_searched && data.results.length !== 0){
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
        var td = this.parentNode.parentNode;
        var smile = $(td).children(".smile").text();

        Calculate.smile = smile;

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
      $(this).text("Show")
             .toggleClass("btn-primary")
             .toggleClass("btn-info")
             .attr("visible","true"); 
    }
  else
    {
      update_model();
      update_pre();
      $("div#commit_content").show();
      $(this).text("Hide")
             .toggleClass("btn-primary")
             .toggleClass("btn-info")
             .attr("visible","false"); 
    }
});

function update_info(){
  Calculate.query = $("#query_input").val();
}

function update_pre(){
  var row = "<tr><td colspan='2'><p class='alert'>Inputs</p></td></tr>";

  if(Calculate.query){
    row += "<tr><td>Query</td><td>"+
           Calculate.query+"</td></tr>";
    row += "<tr><td>Smiles</td><td>"+
           Calculate.smiles+"</td></tr>";
  }

  if(Calculate.draw_mol){
    row += "<tr><td>Chem Structure</td>"+
           "<td>Draw Structure has been added!</td></tr>";
  }

  if(Calculate.files){
    row += "<tr><td>Upload Files</td>"+
           "<td>Upload "+ Calculate.files.length +" mol files</td></tr>";
  }

  row += "<tr><td colspan='2'><p class='alert'>Models</p></td></tr>"; 
  if(Calculate.models){
    $.each(Calculate.models, function(k,v){
      row += "<tr><td>"+k+"</td><td>"+v.temperature+"(temperature)</td></tr>";  
    });
  }

  row += "<tr><td colspan='2'><p class='alert'>Meta</p></td></tr>"; 
  row += "<tr><td>Task Name</td><td>" +Calculate.task_name+"</td></tr>";
  row += "<tr><td>Notify Email</td><td>"+Calculate.email+"</td></tr>";
  row += "<tr><td>Notes</td><td>"+Calculate.notes+"</td></tr>";

  $("#calculate-pre").append(row);
}
