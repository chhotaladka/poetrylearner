$(document).ready(function(){

	var project_attributes = {};
	project_attributes.pid = 0;
	project_attributes.page = 0;

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
	 * Parse the response of 'submitImgUploadForm' and render
	 */
	var renderResponseSubmit = function(data){
		if (data.result == 'success') {
			$('#modal-flashMsg .message').text("Scanned image for page "+project_attributes.page+"\
				has been added successfully!");
			$('#modal-flashMsg .material-icons').text("done");
			$('#modal-flashMsg').removeClass('alert-danger');
			$('#modal-flashMsg').addClass('alert-success');
			$('#modal-flashMsg').removeClass('hidden');
			$('#imgModalBody').html('');
			
			//TODO change the color of page-block; change the data-add value to '0' 
			var pageNumId = "pageNum" + project_attributes.page;
			//var page = document.getElementById(pageNumid);
			//console.dir(page);
			//page.removeClass('miss');
			$('#'+pageNumId+' .link-block').removeClass('mdl-button--accent');
			$('#'+pageNumId+' .link-block').data('add', '0');
			
						
		} else if (data.result == 'failure') {
			$('#modal-flashMsg .message').text("Upload a valid image. \
				The file you uploaded was either not an image or a corrupted image.");
			$('#modal-flashMsg .material-icons').text("error_outline");
			$('#modal-flashMsg').addClass('alert-danger');
			$('#modal-flashMsg').removeClass('hidden');			
		
		} else {
			$('#modal-flashMsg .message').text("Oops!! something went wrong!");
			$('#modal-flashMsg .material-icons').text("error_outline");
			$('#modal-flashMsg').addClass('alert-danger');
			$('#modal-flashMsg').removeClass('hidden');
			$('#imgModalBody').html('');
			
		}
	
	}
	
	
	/**
	 * POST Image upload form data
	 */
	var submitImgUploadForm = function(e){	
		e.defaultPrevented;
		e.stopPropagation();
		console.log( "submitImgUpload: IN");
		
		var fileSelect = document.getElementById('id_image');	
		
		// Get the selected files from the input.	
		var file = fileSelect.files[0];
		
		// Check the file type.
		if (file) {
			if (!file.type.match('image.*')) {
				console.log( "Error: file is not an image");
				$('#modal-flashMsg .message').text("Upload a valid image. \
				The file you uploaded was either not an image or a corrupted image.");
				$('#modal-flashMsg .material-icons').text("warning");
				$('#modal-flashMsg').addClass('alert-danger');
				$('#modal-flashMsg').removeClass('hidden');
				return false;
			}
		} else {
			console.log( "Error: No file is selected");
			$('#modal-flashMsg .message').text("You forgot to select an image.");
			$('#modal-flashMsg .material-icons').text("warning");
			$('#modal-flashMsg').addClass('alert-danger');
			$('#modal-flashMsg').removeClass('hidden');			
			return false;
		}		

		// Create a new FormData object.
		var formData = new FormData();

		formData.append('image', file, file.name);
		formData.append('project', project_attributes.pid);
		formData.append('page_num', project_attributes.page);

		console.log("hello");
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
	        url: project_attributes.url,
	        
	        type: "POST",
	        dataType: "json",
	        contentType: false,
            processData: false,
	        data: formData,
	        timeout: 3000,
	        
	        success: function(data){
                console.log("image upload success!!");
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
		    },
		    
	    });	
	};	
	
	/**
	 * Got a successful response from the server. 
	 * Now, render the Image upload Form
	 */
	var renderImgUploadFrom = function(data){
		console.log("renderImgUploadForm: IN");
		// Update the html inside #imgModalBody
		var body = $("#imgModalBody");		
		body.html(data);
		$("#imgModal .mdl-card__subtitle-text").html("Upload scanned image for page "+project_attributes.page);
		
		$('[id="imgUploadBtn"]').on('click', submitImgUploadForm);
		
		// Modal setup
		$('#modal-flashMsg .message').text("");
		$('#modal-flashMsg .material-icons').text("");
		$('#modal-flashMsg').removeClass('alert-success');
		$('#modal-flashMsg').removeClass('alert-danger');	
		$('#modal-flashMsg').addClass('hidden');
		
		// Modal Display
		$("#imgModal").modal({backdrop: false});
		
	};

	/**
	 * Load Image upload form
	 */
	var loadImgUploadForm = function(){

		console.log( "ImgUpload: pid "+project_attributes.pid+", page "+project_attributes.page);	
		
		/*
		 * At some point of time, this method will be making Ajax queries. 
		 */
		$.ajax({
				    
		    url: project_attributes.url,
		 
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
		    success: renderImgUploadFrom,
		 
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
	 * Got a successful response from the server. 
	 * Now, render the Image View
	 */
	var renderImgView = function(data){
		
		// Update the html inside #imgModalBody
		var body = $("#imgModalBody");		
		body.html(data);
		$("#imgModal .mdl-card__title-text").html("View scanned images");
			
		$('[id="imgUploadBtn"]').on('click', submitImgUploadForm);
		
		// Modal setup
		$('#modal-flashMsg .material-icons').text("");
		$('#modal-flashMsg .message').text("");
		$('#modal-flashMsg').removeClass('alert-danger');	
		$('#modal-flashMsg').addClass('hidden');
		
		// Modal Display
		$("#imgModal").modal({backdrop: true});
		
	};

	/**
	 * Load Image View
	 */
	var loadImgView = function(){

		console.log( "loadImgView: pid "+project_attributes.pid+", page "+project_attributes.page);	
		
		/*
		 * At some point of time, this method will be making Ajax queries. 
		 */
		$.ajax({
				    
		    url: project_attributes.url,
		 
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
		    success: renderImgView,
		 
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
			
		project_attributes.pid = parseInt($(this).data('pid'));
		project_attributes.page = parseInt($(this).data('page'));
		project_attributes.add = parseInt($(this).data('add'));
		console.log( "pageClickAct: pid "+project_attributes.pid+
			", page "+project_attributes.page+
			", add "+project_attributes.add);
		
		if (project_attributes.add == 1) {
			project_attributes.url = window.location.origin + 
				'/en/p/data/image/' + project_attributes.pid + 
				'/?page=' + project_attributes.page + 
				'&action=add';
			loadImgUploadForm();
		} else {
			project_attributes.url = window.location.origin + 
				'/en/p/data/image/' + project_attributes.pid + 
				'/?page=' + project_attributes.page + 
				'&action=view';
			loadImgView();
		}
	
	}

	$('.pageListBlock a').on('click', pageClickAct);



});