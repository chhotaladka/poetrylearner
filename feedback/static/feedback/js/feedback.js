/* ========================================================================
 * name: feedback.js
 * info: To send feedbacks
 * path: /feedback/static/feedback/js/feedback.js
 * dependencies: /poetry/static/js/shared.js
 * ======================================================================== */

+function ($) {
	'use strict';
	
	
	// FEEDBACK PUBLIC CLASS DEFINITION
	// ================================
	
	var feedback_attr = {};
	feedback_attr.url = '';
	feedback_attr.sending = false;
	
	var Feedback = function (element, options) {
		this.itemtype       = null
		this.requestUrl     = null
		this.element        = $(element)
		
	}
	
	Feedback.DEFAULTS = {
		loadingText: 'loading...',
	};
	
	Feedback.prototype.getDefaults = function () {
		return Feedback.DEFAULTS
	};
	
	Feedback.prototype.responseError = function (xhRequest, ErrorText, thrownError) {
		console.log("Feedback: response_error:");
		console.log(xhRequest);
		console.log('Feedback: ErrorText: ' + ErrorText + "\n");
		console.log('Feedback: thrownError: ' + thrownError + "\n");
	};

	/* Parse the response of 'submitForm' and render */
	Feedback.prototype.renderResponseSubmit = function(data) {
		//console.log("Feedback: renderResponseSubmit: IN, ", data.status);
		
		var $this = this.element
		
		var body = $("#id-feedback-form-body");
		body.children().remove();

		if (data.status == '200') {
			body.append(data.contenthtml);

		} else {
			console.log("Feedback: error ", data.status);
			body.append(data.contenthtml);
			
		}
		feedback_attr.sending = false; //So that next message can be sent	
	}
	
	/* POST Feedback form data */
	Feedback.prototype.submitForm = function() {
		//console.log("Feedback: submitForm: IN");
		
		feedback_attr.sending = true;
		this.requestUrl = feedback_attr.url;
		
		var $this = this.element[0]

		// Create a new FormData object.
		var feedback_form = new FormData($this);
		feedback_form.append('page_num', 111);

		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!$.csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", $.getCookie('csrftoken'));
				}
			}
		});
		
		$.ajax({
			cache: false,
			url : this.requestUrl,
			type: "POST",
			data : feedback_form,
			dataType : "json",
			contentType: false,
			processData: false,
			timeout: 3000,
			context : this,
			
			success : this.renderResponseSubmit,
			error : this.responseError,
			
		});
	};
	
	/* Got a successful response from the server. Render the Feedback Form */
	Feedback.prototype.renderForm = function(data) {
		//console.log("Feedback: renderFrom: IN");
		
		var $this = this.element
		
		// Update the html inside #id-feedback-form-body
		var body = $("#id-feedback-form-body");
		body.html(data);
		componentHandler.upgradeDom();// Register new mdl elements
		
		$('#id-feedback-form-submit').prop( "onclick", null);
		// Modal Display
		$("#id-feedback-modal").modal({keyboard: true, backdrop: true});
		
	};
	
	/* Load feedback form */
	Feedback.prototype.loadForm = function() {
		//console.log("Feedback: loadForm: IN");
		
		var $this = this.element
		this.requestUrl = feedback_attr.url;
		
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!$.csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", $.getCookie('csrftoken'));
				}
			}
		});
		
		$.ajax({
			cache: false,
			url : this.requestUrl,
			type: "GET",
			data : {
				format:'json'
			},
			dataType : "html",
			contentType: false,
			processData: false,
			context : this,
			
			success : this.renderForm,
			error : this.responseError,
		});
	};
	
	
	// FEEDBACK PLUGIN DEFINITION
	// ==========================
	
	function Plugin(option) {
		return this.each(function () {
			var $this = $(this)
			var data  = $this.data('bs.feedback')
			
			if (!data) $this.data('bs.feedback', (data = new Feedback(this)))
			if (typeof option == 'string') data[option]()
		})
	}
	
	var old = $.fn.feedback
	
	$.fn.feedback             = Plugin
	$.fn.feedback.Constructor = Feedback
	
	
	// FEEDBACK NO CONFLICT
	// ====================
	
	$.fn.feedback.noConflict = function () {
		$.fn.feedback = old
		return this
	}
	
	
	// APPLY TO STANDARD FEEDBACK ELEMENTS
	// ===================================

	var clickFeedbackBtn = function (e) {
		//console.log("feedback: clickFeedbackBtn: In");
		var url = $(this).data('url');

		if ( typeof url !== typeof undefined && url !== false ) {
			// Update feedback_attr.url
			feedback_attr.url = window.location.origin + url;
			// Call action method
			Plugin.call($(this), 'loadForm');
		}
	};
	
	var clickFeedbackSend = function (e) {
		//console.log("Feedback: submit clicked");
		e.defaultPrevented;
		e.stopPropagation();
		
		if (feedback_attr.sending == false) {
			// Call action method
			Plugin.call($(this), 'submitForm');
		}
		return false;
	};
	
	$(document).on('click.bs.feedback.data-api', '*[id^="feedbackBtn"]', clickFeedbackBtn);
	$(document).on('submit.bs.feedback.data-api', '#id-feedback-form', clickFeedbackSend);
	
	
}(jQuery);