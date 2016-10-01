$(document).ready(function(){

	/*** FUNCTION DEFINITIONS ***/
	
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
	
	/** Load related Poetry **/
	var loadRelatedPoetry = function(e) {
		console.log("loadRelatedPoetry: In");
		
		id = parseInt($("#id-related-poetry").data('id'));
		url = $("#id-related-poetry").data('url');
		
		requestUrl = window.location.origin + url;
		console.log(id, requestUrl);
		
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
				}
			}
		});
		
		$.ajax({
			cache: false,
			url: requestUrl,
			type: "GET",
			dataType: "json",
			contentType: false,
			processData: false,
			
			success: function(data) {
				console.log("loadRelatedPoetry: success!!");
				console.log(data.status);
				
				$("#id-related-poetry").children().remove();
				if (data.status == 200) {
					var html = $.parseHTML(data.contenthtml)
					$("#id-related-poetry").append(html);
					componentHandler.upgradeDom();
					
					// Bind actions on Poetry
					bindActionClickPoetry();
					
				} else {
					var html = $.parseHTML('<i class="material-icons mdl-color-text--green-600">highlight_off</i>')
					$("#id-related-poetry").append(html);
					componentHandler.upgradeDom();
				}
			},
			
			error: function( xhr, status, errorThrown ) {
				console.log( "Error: " + errorThrown );
				console.log( "Status: " + status );
				console.dir( xhr );
				$("#id-related-poetry").children().remove();
				var html = $.parseHTML('<i class="material-icons mdl-color-text--red-600">highlight_off</i>')
				$("#id-related-poetry").append(html);
				componentHandler.upgradeDom();
			},
			
		});
	};
	
	/** Action:click on Poetry list cards **/
	var actionClickPoetry = function(e) {
		e.stopPropagation();
		if($(e.target).is('a') || $(e.target.parentNode).is('a')){
			// clicked on `a` tag.
			return;
		}
		window.document.location = $(this).data("href");
	};
	
	/** Bind Actions to Poetry list **/
	var bindActionClickPoetry = function(e) {
		var nodes = $('.poetry-card.small');
		nodes.on('click', actionClickPoetry);
	};
	
	/*** END OF FUNCTION DEFINITIONS ***/
	
	/* Load related Poetry */
	loadRelatedPoetry();
	
});
