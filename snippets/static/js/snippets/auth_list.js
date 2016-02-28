/**
 * To display snippets by an Author.
 */
$(document).ready(function(){
	var data_attr = {};
	data_attr.done = false;
	data_attr.lock = false;

	/**
	 * Iska hum kuchh nahi kar sakte !!
	 */ 	
	var getCookie = function(name){
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	};
	
	var csrfSafeMethod = function(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};

	/**
	 * Send GET request to get snippets
	 */
	var listSnippet = function(val){	
		console.log("listSnippet: In"+window.location.origin + $('#id-recent-poems').data('url'));		
	    $.ajaxSetup({
	        beforeSend: function(xhr, settings) {
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	            }
	        }
	    });

	    $.ajax({
	        cache: false,
	        url: data_attr.url,	        
	        type: "GET",
	        dataType: "json",
	        contentType: false,
            processData: false,
	        
	        success: function(data){
                console.log("response success!!");
				$.each(data, function(i, item) {			
					var str = 
'<div>'
+ '<a href="' + item.url + '" title="View full article | ' + item.title + '" class="mdl-card poetry-card--sm wFull">'
+ '<div class="title">'
+ item.title
+ '</div>'
+ '<div class="text">'
+ item.body
+ '</div>'
+ '</a>'	          
+ '</div>'
					var html = $.parseHTML(str)
					$("#id-recent-poems").append(html);
					data_attr.done = true;
					data_attr.lock = false;
				});
            },

		    error: function( xhr, status, errorThrown ) {
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		    },
		    
	    });	
	};	

	function isScrolledIntoView(elem) {
		console.log("function called");
		var $elem = $(elem);
		var $window = $(window);

		var docViewTop = $window.scrollTop();
		var docViewBottom = docViewTop + $window.height();

		var elemTop = $elem.offset().top;
		var elemBottom = elemTop + $elem.height();

		return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
	};

	$('.mdl-layout__content').on('scroll', function () {
		if (data_attr.done == true ) {
			console.log("turning off the event");
			$('.mdl-layout__content').off('scroll');
			return false;
		}
		if (isScrolledIntoView('#id-recent-poems') == true) {
			console.log('scrolled');
			if (data_attr.done == false && data_attr.lock == false ) {
				data_attr.lock = true;
				data_attr.url = window.location.origin + $('#id-recent-poems').data('url');
			    listSnippet();
			}
		}
		return false; 
	});

});
