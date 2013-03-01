/**
 * @author tianwei
 * the whole features js
 */

// tooltips
$(document).ready(function(){
  $("[rel=tooltip]").tooltip();
});

// carousel
$(document).ready(function(){
  $('#myCarousel').carousel();
});

// carousel
$(document).ready(function(){
  //$('#carousel-bootcamp').carousel();
});

//step-contents

$(document).ready(function () {
	// WIZARD
	$('#MyWizard').on('change', function(e, data) {
		console.log('change');
		if(data.step===3 && data.direction==='next') {
			// return e.preventDefault();
		}
  });

  $('#MyWizard').on('changed', function(e, data) {
		console.log('changed');
	});
	$('#MyWizard').on('finished', function(e, data) {
		console.log('finished');
	});
	$('#btnWizardPrev').on('click', function() {
		$('#MyWizard').wizard('previous');
	});
	$('#btnWizardNext').on('click', function() {
		$('#MyWizard').wizard('next','foo');
	});
	$('#btnWizardStep').on('click', function() {
		var item = $('#MyWizard').wizard('selectedItem');
		console.log(item.step);
	});
});


$(document).ready(function(){ 
  //button toggle for model choices
  $('[rel=button-switch]').btn_toggle();
  
  //choice label 
  $('[rel=label-choice]').hide();
  
  //date picker
  $('.datepicker').datepicker({
		format: 'yyyy-mm-dd'
	});
	
  //search options
  var search_panel = "#search-options-panel";
  $(search_panel).hide();
  $('#option-search').click(
    function(){
    if($(search_panel).attr('visible')==='false')
      {
        $(search_panel).show();
        $(search_panel).attr('visible','true');
      }
      else
      {
        $(search_panel).hide();
        $(search_panel).attr('visible','false');
      }
  });
  
  //task details filter label
  $('ul li a.filter').click(
    function(){
      $("ul li a.filter").parent().removeClass('active');
      $(this).parent().attr('class','active');
      
      var success_queue = 'ul.tasklist > li.queue-success';
      var failed_queue = 'ul.tasklist > li.queue-failed';
      var inprogress_queue = 'ul.tasklist > li.queue-inprogress';
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

/*
$(document).ready(function(){
	$('ul li a.setting-bar').click(
		function(){
			$("ul li a.setting-bar").parent().removeClass('active');
			$(this).parent().attr('class','active');
		});
});
*/