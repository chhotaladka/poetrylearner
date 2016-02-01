/**
 * To create Poetries from articles of an author
 */
$(document).ready(function(){

	var data_attributes = {};

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
	 * Parse the response
	 */
	var renderResponse = function(data){
		console.log("renderResponses: In, "+data.result);
		$('#id-div-status').addClass('hidden');
		$('#id-div-loading').toggleClass('hidden');

		if (data.result == 'success') {
			$('#id-status-text').text(data.count+' articles added to snippet successfully!!');
			$('#id-status-icon').text('done');
			$('#id-div-status').removeClass('status-failure');
			$('#id-div-status').addClass('status-success');
			$('#id-div-status').removeClass('hidden');			
						
		} else if (data.result == 'failure') {
			console.log("failed");
			$('#id-status-text').text('Failed to add articles to snippet! Current Author was not found in main db. Please add.');
			$('#id-status-icon').text('error_outline');
			$('#id-div-status').removeClass('status-success');
			$('#id-div-status').addClass('status-failure');
			$('#id-div-status').removeClass('hidden');
			$('#id-article-btn').toggleClass('hidden');
		} else {
			console.log("unexpected error!");
			$('#id-status-text').text('Unexpected error occurred!');
			$('#id-status-icon').text('error_outline');
			$('#id-div-status').removeClass('status-success');
			$('#id-div-status').addClass('status-failure');
			$('#id-div-status').removeClass('hidden');
			$('#id-article-btn').toggleClass('hidden');
		}
	
	}

	/**
	 * Send request
	 */
	var sendRequest = function(){
		console.log("sendRequest: In");	
		
		$.ajax({
				    
		    url: data_attributes.url,
		    data: {
		        format:'json'
		    },
		    type: "GET",		 
		    // the type of data we expect back
		    dataType: "json",
		 
		    // code to run if the request succeeds;
		    // the response is passed to the function
		    success: renderResponse,
		 
		    // code to run if the request fails; the raw request and
		    // status codes are passed to the function
		    error: function( xhr, status, errorThrown ) {
		        //alert( "Sorry, there was a problem!" );
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		        console.dir( xhr );
		    },
		 
		    // code to run regardless of success or failure
		    complete: function( xhr, status ) {
		        //alert( "The request is complete!" );
		    }
		});
	};

	/**
	 * Page Click Actions
	 */
	var pageClickAct = function(){			
		console.log("pageClickAct: In");	
					
		data_attributes.url = window.location.origin + $('#id-add-article-btn').data('url');
		console.log(data_attributes.url);
		var arg1 = 'articles='
		var count = 0;
		$('#id-tbody').find('tr.is-selected').each(function() {
  		arg1 += $(this).data('id') + ','
  		count++;
		});
		console.log(arg1, count);
		
		if (count == 0) {
			$('#id-status-text').text('Select at least one article.');
			$('#id-div-status').removeClass('hidden');
			return false;			
		}

		var arg2 = 'creator=';
		var cId = '';
		$('#id_creator option').each(function() {
  		cId = $(this).val();
  		console.log(cId);
		});
				
		arg2 += cId;
		console.log(arg2);		
		
		
		$('#id-div-action').addClass('hidden');
		$('#id-status-text').text('Waiting for the server response. Please wait...');
		$('#id-div-status').removeClass('hidden');
		$('#id-div-loading').removeClass('hidden');
		$('#id-cancel-btn').addClass('hidden');
				
		//sendRequest();
	};	
	
	var displayAction = function(){
		$('#id-add-btn').addClass('hidden');			
		$('#id-div-action').removeClass('hidden');
		$('#id-cancel-btn').removeClass('hidden');
	};
	var hideAction = function(){			
		$('#id-cancel-btn').addClass('hidden');	
		$('#id-div-action').addClass('hidden');
		$('#id-add-btn').removeClass('hidden');	
		$('#id-div-status').addClass('hidden');	
	};
		
	$('#id-add-btn').on('click', displayAction);
	$('#id-cancel-btn').on('click', hideAction);
	$('#id-add-article-btn').on('click', pageClickAct);

});
