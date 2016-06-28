$(document).ready(function(){

	var feedback_attributes = {};
	feedback_attributes.url = '';
	feedback_attributes.sending_started = false;

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
	 * Parse the response of 'submitFeedbackForm' and render
	 */
	var renderResponseSubmit = function(data){
		console.log("renderResponseSubmit: IN, ", data.result, data.status);
		var body = $("#id-feedback-form-body");
		body.children().remove();		
		// Display success result
		if (data.result == 'success') {			
			body.append(data.html);

		} else if (data.result == 'failure') {
			var str = '<div class="tAc p-32 err">Error! (' + data.status + ')</div>';
			var html = $.parseHTML(str);
			body.append(html);			
		} else {
	
		}
		feedback_attributes.sending_started = false; //So that next message can be sent	
	}
		
	/**
	 * POST Feedback form data
	 */
	var submitFeedbackForm = function(e){
		feedback_attributes.sending_started = true;
		e.defaultPrevented;
		e.stopPropagation();
		console.log( "submitFeedbackForm: IN");

		// Create a new FormData object.
		var feedback_form = new FormData(document.getElementById('id-feedback-form'));

		feedback_form.append('page_num', 111);

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
	    
    // Save Form Data
    $.ajax({
        cache: false,
        url: feedback_attributes.url,
        
        type: "POST",
        dataType: "json",
        contentType: false,
        processData: false,
        data: feedback_form,
        timeout: 3000,
        
        success: function(data){
              renderResponseSubmit(data);
        },
          
		    // Code to run if the request fails; 
		    // The raw request and status codes are passed to the function
		    error: function( xhr, status, errorThrown ) {
		        //alert( "Sorry, there was a problem!" );
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		        console.dir( xhr );
		    },
	    
    });
	};	
	
	/**
	 * Got a successful response from the server. 
	 * Now, render the Feedback Form
	 */
	var renderFeedbackFrom = function(data) {
		console.log("renderFeedbackFrom: IN");
		
		// Update the html inside #id-feedback-form-body
		var body = $("#id-feedback-form-body");		
		body.html(data);
		componentHandler.upgradeDom();// Register new mdl elements
		
		$('#id-feedback-form-submit').prop( "onclick", null);
		$("#id-feedback-form-body").on('submit', "#id-feedback-form", function(e){
			e.defaultPrevented;
			e.stopPropagation(); 
			if (feedback_attributes.sending_started == false) {  		
				submitFeedbackForm(e);
			}
			return false;
		});
		//$('[id="id-feedback-form-submit"]').on('click', submitFeedbackForm);
		
		// Modal setup
		//$('#modal-flashMsg .message').text("");
		//$('#modal-flashMsg .material-icons').text("");
		//$('#modal-flashMsg').removeClass('alert-success');
		//$('#modal-flashMsg').removeClass('alert-danger');	
		//$('#modal-flashMsg').addClass('hidden');
		
		// Modal Display
		$("#id-feedback-modal").modal({keyboard: true, backdrop: true});
		
	};

	/**
	 * Load Feedback form
	 */
	var loadFeedbackForm = function() {
		console.log("loadFeedbackForm: IN");
		
		$.ajax({
				    
		    url: feedback_attributes.url,
		 
		    // the data to send (will be converted to a query string)
		    data: {
		        format:'json'
		    },		 

		    type: "GET",		 

		    // the type of data we expect back
		    dataType: "html",

		    success: renderFeedbackFrom,
		 
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
	var pageClickAct = function() {
		console.log( "pageClickAct: IN");
		feedback_attributes.url = window.location.origin + $(this).data('url');
		loadFeedbackForm();
	}
	//var nodes = document.querySelectorAll('*[id^="feedbackBtn"]');//for new browsers
	var nodes = $('*[id^="feedbackBtn"]'); //old browser
	nodes.on('click', pageClickAct);//old browser	

});