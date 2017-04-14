/* ========================================================================
 * name: activity.js
 * info: To access various activity list
 * path: /activity/static/activity/js/activity.js
 * dependencies: /poetry/static/js/shared.js
 * ======================================================================== */

+function ($) {
	'use strict';

	// ACTIVITY PUBLIC CLASS DEFINITION
	// ==================================
	
	var selector_contributors = '#id-contributors';
	var selector_contributors_loading = '#id-contributors-loading';
	
	var Activity = function (element, options) {
		this.requestUrl     = null
		this.element       = $(element)
	}
	
	Activity.prototype.responseError = function (xhRequest, ErrorText, thrownError) {
		console.log("Activity: response_error:");
		console.log(xhRequest);
		console.log('Activity: ErrorText: ' + ErrorText + "\n");
		console.log('Activity: thrownError: ' + thrownError + "\n");
		$(selector_contributors_loading).text('error loading contributors :(');
	};
	
	Activity.prototype.responseSuccess = function(data) {
		//console.log("Activity: response_success: " + data.status);
		var selector = $(selector_contributors);
		selector.children().remove();
		
		if (data.status == '200') {
			$(selector_contributors_loading).addClass('hidden');
			var html = $.parseHTML(data.contenthtml);
			selector.append(html);
		} else {
			$(selector_contributors_loading).text('error loading contributors!');
		}
		componentHandler.upgradeDom();
	};
	
	/* Load related Poetry */
	Activity.prototype.loadContributors = function() {
		//console.log("Activity: loadContributors: In");
		$(selector_contributors_loading).removeClass('hidden');
		
		var $this    = this.element;
		this.requestUrl = window.location.origin + $this.data('url');
		
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!$.csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", $.getCookie('csrftoken'));
				}
			}
		});
		
		$.ajax({
			cache: false,
			url: this.requestUrl,
			type: "GET",
			dataType: "json",
			contentType: false,
			processData: false,
			context : this,
			
			success : this.responseSuccess,
			error : this.responseError,
			
		});
	};

	// ACTIVITY PLUGIN DEFINITION
	// ==========================	
	function Plugin(option) {
		return this.each(function () {
			var $this = $(this);
			var data  = $this.data('bs.activity');
			
			if (!data) $this.data('bs.activity', (data = new Activity(this)));
			//if (typeof option == 'string') data[option].call($this)//It will pass this.element, which we dont need
			if (typeof option == 'string') data[option]();
		})
	}
	
	var old = $.fn.activity;
	
	$.fn.activity             = Plugin;
	$.fn.activity.Constructor = Activity;
	
	
	// ACTIVITY NO CONFLICT
	// ======================
	$.fn.activity.noConflict = function () {
		$.fn.activity = old;
		return this;
	}
	
	// APPLY TO ACTIVITY ELEMENTS
	// ============================
	var bindActionLoadContributors = function() {
		// Call action if element $(selector_contributors) present with correct attributes
		if( $(selector_contributors).length ) {
			// Check data attributes of the element
			var url = $(selector_contributors).attr("data-url");
			if ( typeof url !== typeof undefined && url !== false ) {
				Plugin.call($(selector_contributors), 'loadContributors');
			}
		}
	};

	$(document).ready(bindActionLoadContributors);
	
}(jQuery);



