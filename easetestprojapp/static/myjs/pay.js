$(document).ready( function() { 

        $('header').css({'border-bottom':'1px solid #000'})
       
        $(window).scroll(function() {
                var scrlDist = $(window).scrollTop();
                
                if(scrlDist > 400) {
                        $('.dashboard-banner').slideUp()
                }
                
        })
});