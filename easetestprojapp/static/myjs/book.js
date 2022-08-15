$(document).ready(function() {

        $(window).scroll( function() {
            var scrlDist = $(window).scrollTop();
          
            if (scrlDist < 200) {
                $('.navbar').css({'backgroundColor':'transparent','boxShadow':'none'});
                $('.navbar-nav').css({'border': '0'});
                $('.navbar-collapse a').css({'color':'#000','fontStyle':'italic','borderBottom': '3px solid #D90429','font-weight':'600','font-size':'18px','margin-top':'0', 'margin-left':'1em'});
                $('.search-btn').removeClass('btn-outline-dark');
            } else {
                $('.navbar').css({'backgroundColor':'#fff', 'position':'fixed', 'top':'0', 'left':'0', 'right':'0', 'z-index':'99',
                    'boxShadow':'3px 3px 2px #eee'});
                $('.search-btn').addClass('btn-outline-dark');
                $('.navbar-nav').css({'border': '1px solid #000', 'paddingBottom':'10px'});
                $('.navbar-collapse a').css({'color':'#000','fontStyle':'normal','border':'none','font-weight':'500','font-size':'20px','margin-top':'10px', 'margin-left':'0'});
                $('.navbar-collapse a').hover({'border': '3px solid #000'});
            }
        });

        
    });