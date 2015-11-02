/**
 * To create Author in main DB from the crawled Author.
 */
$(document).ready(function(){

	var data_attributes = {};
	data_attributes.valid = false;

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
	 * Send GET request to set crawled author's validity
	 */
	var validateAuthor = function(val){	
		console.log("validateAuthor: In");		

	    $.ajaxSetup({
	        beforeSend: function(xhr, settings) {
	            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	            }
	        }
	    });

	    $.ajax({
	        cache: false,
	        url: window.location.href + '?valid='+val,	        
	        type: "GET",
	        dataType: "json",
	        contentType: false,
            processData: false,
	        
	        success: function(data){
                console.log("validateAuthor success!!");
                console.log(data);
				$("#id-flash-icon").children().remove();
				if (data.result == 'success') {
					data_attributes.valid = true;
					var html = $.parseHTML('<i class="material-icons mdl-color-text--green-600">check_circle</i>')
					$("#id-flash-icon").append(html);
					$("#id-flash-msg").text('Author created! Validation successful!');
					$("#id-validity").text('True');
					$("#id-add-btn").addClass("hidden");
				} else {
					var html = $.parseHTML('<i class="material-icons mdl-color-text--red-600">highlight_off</i>')
					$("#id-flash-icon").append(html);
					$("#id-flash-msg").text('Author created! Validation failed due to invalid request.');
				}
            },
            
		    // Code to run if the request fails; 
		    // The raw request and status codes are passed to the function
		    error: function( xhr, status, errorThrown ) {
		        //alert( "Sorry, there was a problem!" );
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		        console.dir( xhr );
				$("#id-flash-icon").children().remove();
				var html = $.parseHTML('<i class="material-icons mdl-color-text--red-700">highlight_off</i>')
				$("#id-flash-icon").append(html);
				$("#id-flash-msg").text('Author created! Validation failed due to unexpected error.');
		    },
		    
	    });	
	};	

	/**
	 * Parse the response of 'submitForm' and render
	 */
	var renderResponseSubmit = function(data){
		console.log("renderResponseSubmit: In, "+data.result+", "+data.url);
		if (data.result == 'success') {
			//dismissForm();
			// Display success result
			var body = $("#id-div-form-body");
			body.children().remove();
			var str = '<div id="id-flash-icon" class="tAc pT-48"><div class="mdl-spinner mdl-js-spinner is-active"></div></div>'
					+'<div id="id-flash-msg" class="flash-msg mdl-color-text--grey-600 tAc">'
						+'Author created! Please wait while we validate crawled author...'
					+'</div>'
					+'<div class="tAc"><a href="'+data.url+'" target="_blank" title="Visit author page">Visit Author</a></div>';
			var html = $.parseHTML(str);
			body.append(html);
			componentHandler.upgradeDom();
			// Validate crawled Author
			validateAuthor('True');
						
		} else if (data.result == 'failure') {
			renderForm(data.data);
		} else {
	
		}
	
	}
	
	
	/**
	 * POST Form data
	 */
	var submitForm = function(e){	
		e.defaultPrevented;
		e.stopPropagation();
		console.log("submitForm: In");		

		// Create a new FormData object.
		var formData = new FormData(document.getElementById('id-author-form'));

		/* POST it now!
		 * Form Validation goes here....
		 */
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
	        url: data_attributes.url,
	        
	        type: "POST",
	        dataType: "json",
	        contentType: false,
            processData: false,
	        data: formData,
	        //timeout: 3000,
	        
	        success: function(data){
                console.log("submitForm success!!");
                console.log(data);
                renderResponseSubmit(data);
            },
            
		    // Code to run if the request fails; 
		    // The raw request and status codes are passed to the function
		    error: function( xhr, status, errorThrown ) {
		        //alert( "Sorry, there was a problem!" );
		        console.log( "Error: " + errorThrown );
		        console.log( "Status: " + status );
		        console.dir( xhr );
				var body = $("#id-div-form-body");
				body.children().remove();
				var str = '<div id="id-flash-icon" class="tAc pT-48">'
							+'<i class="material-icons mdl-color-text--red-700">highlight_off</i>'
						+'</div>'
						+'<div id="id-flash-msg" class="flash-msg mdl-color-text--grey-600 tAc">'
							+'Failed to create Author! Unexpected error occured. <br/>Admin chutiye ko bolo dhang se code likhe.'
						+'</div>';
				var html = $.parseHTML(str);
				body.append(html);
		    },
		    
	    });	
	};	

	/**
	 * Dismiss the Form
	 */
	var dismissForm = function(){
		console.log("dismissForm: In");
		// Remove the html inside the div
		var body = $("#id-div-form-body");
		body.children().remove();
		$('#id-div-form').addClass('hidden');
		$('#id-author-card').addClass('wFull');

		if (data_attributes.valid == false) {
			$('#id-add-btn').removeClass('hidden');
		}
	};
	
	/**
	 * Got a successful response from the server. 
	 * Now, render the Form
	 */
	var renderForm = function(data){
		console.log("renderForm: In");
		var html = $.parseHTML(data);
		var body = $("#id-div-form-body");
		$("#id-div-form-body").off('submit', "#id-author-form");//Remove event listner
		body.children().remove();
		body.append(html);

		componentHandler.upgradeDom();// Register new mdl elements
		
		$('#id-form-submit').prop( "onclick", null );
		$("#id-div-form-body").on('submit', "#id-author-form", function(e){
			e.defaultPrevented;
			e.stopPropagation();   		
			submitForm(e);
			return false;
		});
		$('#id-form-cancel').prop( "onclick", null );
		$('#id-form-cancel').off('click');
		$('#id-form-cancel').on('click', dismissForm);
		$('#id-dismiss').off('click');
		$('#id-dismiss').on('click', dismissForm);

		$('#id-author-card').removeClass('wFull');
		$('#id-add-btn').addClass('hidden');
		$('#id-div-form').removeClass('hidden');
	};

	/**
	 * Load form
	 */
	var loadForm = function(){
		console.log("loadForm: In");	
		
		$.ajax({
				    
		    url: data_attributes.url,		 
		    // the data to send (will be converted to a query string)
		    data: {
		        format:'json'
		    },		 
		    // whether this is a POST or GET request
		    type: "GET",		 
		    // the type of data we expect back
		    dataType: "html",
		 
		    // code to run if the request succeeds;
		    // the response is passed to the function
		    success: renderForm,
		 
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
		data_attributes.url = window.location.origin + '/en/p/add/author/';
		loadForm();
	};
	
	$('#id-add-btn').on('click', pageClickAct);

});
