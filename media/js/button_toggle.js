/*
 * Button Toggle 
 *
 * From Tianwei
 *
 * 
 */

$.fn.btn_toggle = function(){

  $(this).click(
    function(){
      $(this).text($(this).attr("switch_text"));
      alert($(this).attr("switch_text"));
  });

};
