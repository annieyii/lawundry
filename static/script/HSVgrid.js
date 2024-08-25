


/*
$(document).ready(function() {
    $('.image-box').on('click', function(event) {
        const boxWidth = $(this).width();
        const boxHeight = $(this).height();
        const offsetX = event.offsetX;
        const offsetY = event.offsetY;

        const column = Math.floor(offsetX / (boxWidth / 3));
        const row = Math.floor(offsetY / (boxHeight / 3));
        const index = row * 3 + column;

        $(this).find('.grid-box').removeClass('active');

        $('.image-box').each(function() {
            $(this).find('.grid-box').removeClass('active');
            $(this).find('.grid-box').each(function(i) {
                if (i !== index) {
                    $(this).addClass('active');
                }
            });
        });
    });
});
*/
