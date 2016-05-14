$(document).ready(function(){

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
	 * Parse the response & render
	 */
	var renderResponse = function(data){
		console.log("renderResponse: In, "+data.status);		
		if (data.status == '200') {
			//success
			if (data.id != 0) {
				$(this).addClass("true");
				$(this).attr('data-bid', data.id);
				$(this).prop('title', "Remove from my Bookmarks");				
			} else {
				$(this).removeClass("true");
				$(this).attr('data-bid', data.id);
				$(this).prop('title', "Send to my Bookmarks to read later");		
			}						
		} else {
			console.log("Error: "+data.status);
			$(this).prop('title', "Try again");
		}	
	}

	/**
	 * Validate and send bookmark to server
	 */
	var validateAndSend = function(e){
		e.defaultPrevented;
		e.stopPropagation();
		console.log("validateAndSend: In");
		
		id = parseInt($(this).data('id'));
		contentType = parseInt($(this).data('ct'));
		bookmarkId = parseInt($(this).attr('data-bid'));
		console.log(contentType, id, bookmarkId);
		
		if (bookmarkId != 0) {
			postUrl = window.location.origin + '/en/bookmark/remove/';
		} else {
			postUrl = window.location.origin + '/en/bookmark/add/';
		}
		
		var fd = new FormData()
		fd.append('content_type', contentType);
		fd.append('object_id', id);
		
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    
    //Send request to server
    $.ajax({
        cache: false,
        url : postUrl,
        type: "POST",
        dataType : "json",
        contentType: false,
        processData: false,
        data : fd,
        context : this,
        success : renderResponse,
        error : function (xhRequest, ErrorText, thrownError) {
            //alert("Failed to process annotation correctly, please try again");
            console.log('xhRequest:\n');
            console.log(xhRequest);
            console.log('ErrorText: ' + ErrorText + "\n");
            console.log('thrownError: ' + thrownError + "\n");
        }
    });		 
	};

	/*
	 * Bind methods to click on bookmark buttons and enable the buttons
	 */	
	$('.bookmark-btn').on('click', validateAndSend);

});
