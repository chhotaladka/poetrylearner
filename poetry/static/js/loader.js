$(document).ready(function(){

	/*###### COMMON FUNCTIONS ######*/
	
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
	
	
	/*###### REPOSITORY/POETRY RELATED FUNCTIONS ######*/
	
	/** Action: Load related Poetry **/
	var actionLoadRelatedPoetry = function(id, url) {
		console.log("actionLoadRelatedPoetry: In");
		
		item_id = parseInt(id);
		requestUrl = window.location.origin + url + "?id=" + item_id;
		console.log(requestUrl);
		
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
				console.log("actionLoadRelatedPoetry: success!!");
				console.log(data.status);
				
				$("#id-related-poetry").children().remove();
				if (data.status == 200) {
					var html = $.parseHTML(data.contenthtml)
					$("#id-related-poetry").append(html);
					componentHandler.upgradeDom();
					
					// Bind actions on Poetry
					//bindActionClickPoetry();
					
				} else {
					var html = $.parseHTML('<i class="material-icons mdl-color-text--green-600">highlight_off</i>')
					$("#id-related-poetry").append(html);
					componentHandler.upgradeDom();
				}
			},
			
			error: function( xhr, status, errorThrown ) {
				console.log("actionLoadRelatedPoetry: error!!");
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
	
	
	/** Action: click on Poetry list cards **/
	var actionClickPoetry = function(e) {
		e.stopPropagation();
		if($(e.target).is('a') || $(e.target.parentNode).is('a')){
			// clicked on `a` tag.
			return;
		}
		window.document.location = $(this).data("href");
	};
	
	
	/** Bind Action: to load related poetry list **/
	var bindActionLoadRelatedPoetry = function() {
		// Call action if element #id-related-poetry present with correct attributes
		if( $("#id-related-poetry").length ) {
			// Check data attributes of the element
			var id = $("#id-related-poetry").attr("data-id");
			var url = $("#id-related-poetry").attr("data-url");
			if ( (typeof id !== typeof undefined && id !== false) &&
				(typeof url !== typeof undefined && url !== false) ) {
				// Call action method
				actionLoadRelatedPoetry(id, url);
			}
		}
	};
	
	
	/** Bind Action: to click on Poetry list cards **/
	var bindActionClickPoetry = function() {
		var nodes = $('.poetry-card.small');
		nodes.on('click', actionClickPoetry);
	};
	
	
	/*###### CALLING  ######*/
	
	/* Load related Poetry */
	bindActionLoadRelatedPoetry();
	
});
