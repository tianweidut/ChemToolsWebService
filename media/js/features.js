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

//button toggle for model choices
$(document).ready(function(){ 
  $('[rel=button-switch]').btn_toggle();
});

//choice label 
$(document).ready(function(){
  $('[rel=label-choice]').hide();
});

//date picker
$(document).ready(function(){
	$('.datepicker').datepicker({
		format: 'yyyy-mm-dd'
	});
});
