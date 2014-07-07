$(function(){
  $('#search-result').hide();
  $('#search-no-result').hide();
  $('#search-loading').hide();
  $("#calculate-submit-info").hide();
});

//model choice
$(function () {
    $('.model-args').hide(); 
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

    $('.checkbox').click(function(){
      var model_args = $('#' + $(this).attr('model') + '_args'); 
      if($(this).find('input[type=checkbox]').is(':checked')){
        model_args.hide();
      }else{
        model_args.show();
      }
    });
});

function update_model(){
  Calculate.models = [];
  $(".checkbox").each(function(){
    var model = $(this).attr("model");
    var temperature = "#temperature_" + model;

    if($(this).find('input[type=checkbox]').is(':checked')){
      var data = {'model':model,
                 'temperature':$(temperature).val()}; 
      Calculate.models.push(data);
    }    
  });
}

//chem structure draw
$(function(){
  $('#draw_btn').click(function(){
    var chem_iframe = $("#chemwriter_iframe");
    chemwriter_iframe.window.get_chem_draw_content();
    Calculate.draw_mol_data = chem_iframe.contents().find('#data').html();
    console.log(Calculate.draw_mol);
    $(this).text("已添加").addClass("btn-danger");
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
  
    console.log(Calculate.files);
    $(this).text("文件添加完毕!")
           .toggleClass("btn-danger").toggleClass("btn-info");

  });
});


$('#calculate-submit-btn').click(function(){
  Calculate.task_name = $("#task_name").val();
  Calculate.task_notes = $("#task_notes").val();
  update_model();

  if (!(Calculate.smile || Calculate.draw_mol_data || Calculate.files)){
      $("#calculate-submit-info").show().text("至少选择一种输入方式!");
      return;
  }

  if (Calculate.task_name.length == 0){
      $("#calculate-submit-info").show().text("请输入计算任务名称!");
      return;
  }

  if (Calculate.task_notes == 0){
      $("#calculate-submit-info").show().text("请输入计算任务描述!");
      return;
  }

  if (Calculate.models.length == 0){
      $("#calculate-submit-info").show().text("请至少选择一种计算模型!");
      return;
  }

  var data = {
          "smile":Calculate.smile,
          "local_search_id":Calculate.local_search_id,
          "draw_mol_data":Calculate.draw_mol_data,
          "task_notes":Calculate.task_notes,
          "task_name":Calculate.task_name,
          "files_id_list":JSON.stringify(Calculate.files),
          "models":JSON.stringify(Calculate.models),
         };

  console.log(data);

  var url = '/api/task-submit/';

  $.post(url, data).done(function(content){
    if(content.status){
      window.location.href="/history/";
    }else{
      $("#calculate-submit-info").show().text(content.info);
    }
  });
});

$('#search-btn').click(function(){
  var data = {"cas":$("#query_input_cas").val(),
              "smile":$("#query_input_smile").val(),
              "common_name_en":$("#query_input_common_name_en").val(),
              "common_name_ch":$("#query_input_common_name_ch").val()}

  var url = "/api/smile-search/";
  
  $('#search-loading').show();
  
  $.post(url, data).done(function(content){
    var element = "#search-smile-content";
    $("#search-loading").hide();

    if(content.length !== 0){
      $("#search-result").show();
      $("#search-no-result").hide();
      $(element).find("tbody").html("");
      $.each(content, function(k,v){
        var row = "<tr class='search-content'><td>"+ v.cas +"</td><td>"+
                  v.formula + "</td><td>" +
                  v.commonname + "</td><td class='smile' local_search_id='"+ v.id +"'>" +
                  v.smiles + "</td><td>" +
                  v.alogp + "</td>"+
                  "<td><a class='btn btn-primary search-select'>选择</a></td></tr>";
        $(element).find("tbody").append(row);
      });
      
      $(".search-select").click(function(){
        var td = this.parentNode.parentNode;
        var smile = $(td).children(".smile").text();
        var local_search_id = $(td).children(".smile").attr('local_search_id'); 

        Calculate.smile = smile;
        Calculate.local_search_id = local_search_id;
        console.log(smile);
        console.log(local_search_id);

        $(".search-content").removeClass("danger");
        $(".search-select").text('选择');
        $(td).addClass("danger");
        $(this).text('已选择');

      });
    }else{
      $("#search-result").hide();
      $("#search-no-result").show();
    }
  });
});
