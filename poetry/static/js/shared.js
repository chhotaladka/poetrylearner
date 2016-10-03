/* ========================================================================
 * name: shared.js
 * info: shared resources and functions
 * path: /poetry/static/js/shared.js
 * dependencies: jquery-2.1.4
 * ======================================================================== */

+function ($) {
	'use strict';
	
	// GLOBAL PUBLIC DEFINITIONS
	// =========================
	
	$.getCookie = function(name){
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
	
	$.csrfSafeMethod = function(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};
	
}(jQuery);