jQuery(document).ready(function(){
    var items = jQuery("#review-ticker .review-item");
    var currentIndex = 0;

    if (items.length > 1) {
        // Initially hide all items and show the first one
        items.hide();
        items.eq(0).show();

        // Function to cycle reviews
        function cycleReviews(){
            // Fade out the current review over 1000ms
            items.eq(currentIndex).fadeOut(1000, function(){
                // Once faded out, hide it and reset its opacity
                jQuery(this).hide().css("opacity", 1);
                // Update current index cyclically
                currentIndex = (currentIndex + 1) % items.length;
                // Fade in the next review over 1000ms
                items.eq(currentIndex).css("opacity", 0).show().fadeTo(1000, 1, function(){
                    // After fading in, wait 5000ms before cycling again
                    setTimeout(cycleReviews, 5000);
                });
            });
        }
        // Start the cycle after an initial delay of 5000ms
        setTimeout(cycleReviews, 5000);
    } else if (items.length === 1) {
        items.show();
    }
});
