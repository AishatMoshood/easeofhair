$(document).ready(function() {

	//$('.carousel').carousel({interval: 7000});

	$('.slogan a').addClass('animate__animated animate__bounceInDown')

	$('.dropdown-menu-a').css({'color':'#000'});

	$('.navbar-collapse a:active').css({'color':'#fff'}) 
	$('.navbar-collapse a').css({'paddingLeft':'17px','fontSize':'18px', 'fontWeight':'800'});
	  
	//   .navbar-collapse a:visited {
	// 	color: #fff;
	//   }


	
	$(window).scroll( function() {
		var scrlDist = $(window).scrollTop();
		//alert(scrlDist)
		if (scrlDist > 200 && scrlDist < 630) {
			$('.navbar').hide();
			$('.navbar-collapse a').hover({'border': '3px solid #00'});
		} else {
			$('.navbar').slideDown();
		}

		if (scrlDist < 630) {
			$('.navbar').css({'backgroundColor':'transparent','boxShadow':'none', 'z-index':'10','top': '15px','padding-top':'10px'});
			$('.navbar-collapse a').css({'color':'#fff'});
			$('.navbar-collapse a').hover({'color':'#fff','border': '3px solid #fff'});
			$('.navbar-nav').css({'border': 'none'});
			$('.srhbtn').removeClass('btn-danger');
			$('.dropdown-menu-a').css({'color':'#000'});
			

		} else {
			$('.navbar').css({'backgroundColor':'#fff', 'position':'fixed', 'top':'0', 'left':'0', 'right':'0', 'z-index':'1',
				'boxShadow':'3px 3px 2px #eee', 'padding-top':'30px'});
			$('.navbar-nav').css({'border': '1px solid #000'});
			$('.navbar-collapse a').css({'color':'#000','fontStyle':'italic',' margin-right': '.5em'});
			$('.srhbtn').addClass('btn-danger');
		}
	}); 



	// function updateBackground(){
	// 	let window_width = window.innerWidth;
	// 	if (window_width > 0) document.querySelector(".navbar").classList.remove("").add("background2");
	// 	else document.getElementById("to-modify").classList.remove("background2").add("background1");
	// }

	// window.onresize.apply(updateBackground);


  	// $('.fa-search').click(function() {
	// 	$('.srch').slideDown();
  	// })


	$('.small-img1,.small-img2,.small-img3,.small-img4,.small-img5,.small-img6').mouseover( function() {
		$('.small-p1,.small-p2,.small-p3,.small-p4,.small-p5,.small-p6').slideDown();
	})

});