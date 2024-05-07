$(document).ready(function(){
    $('.sidenav').sidenav();
    $('#textarea1').val('New Text');
    $('.modal').modal();
    M.textareaAutoResize($('#textarea1'));
    $('#category_color_input').on('input', function() {
            // Get the new color value from the input field
            var newColor = $(this).val();
            
            // Update the class of the card content div dynamically
            $('.category-color-{{ category._id }}').removeClass().addClass('card-content black-text category-color-{{ category._id }} ' + newColor);
        });
    $('select').formSelect();
  });