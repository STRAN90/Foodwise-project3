$(document).ready(function(){
    $('.sidenav').sidenav();
    $('#category_color_input').on('input', function() {
            // Get the new color value from the input field
            var newColor = $(this).val();
            
            // Update the class of the card content div dynamically
            $('.category-color-{{ category._id }}').removeClass().addClass('card-content black-text category-color-{{ category._id }} ' + newColor);
        });
  });