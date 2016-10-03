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

/* ========================================================================
 * name: bookmark.js
 * info: To create and remove the bookmarks
 * path: /bookmarks/static/bookmarks/js/bookmarks.js
 * dependencies: /poetry/static/js/shared.js
 * ======================================================================== */

+function ($) {
	'use strict';
	
	
	// BOOKMARK PUBLIC CLASS DEFINITION
	// ================================
	
	//var dismiss = '[data-dismiss="alert"]'
	var selector = '.bookmark-btn'
	
	var Bookmark = function (element, options) {
		this.itemtype       = null
		this.id             = null
		this.bookmarkId     = null
		this.requestUrl     = null
		this.element       = $(element)
		
	}
	
	Bookmark.DEFAULTS = {
		loadingText: 'loading...',
	};
	
	Bookmark.prototype.getDefaults = function () {
		return Bookmark.DEFAULTS
	};
	
	Bookmark.prototype.responseSuccess = function(data) {
		//console.log("Bookmark: response_success: " + data.status);
		
		if (data.status == '200') {
			if (data.id != 0) {
				$(this).addClass("true");
				$(this).attr('data-bid', data.id);
				$(this).prop('title', 'Remove from my Bookmarks');
			} else {
				$(this).removeClass("true");
				$(this).attr('data-bid', data.id);
				$(this).prop('title', 'Send to my Bookmarks to read later');
			}
		} else {
			$(this).prop('title', 'Try again');
		}
	};
	
	Bookmark.prototype.responseError = function (xhRequest, ErrorText, thrownError) {
		console.log("Bookmark: response_error:");
		console.log(xhRequest);
		console.log('Bookmark: ErrorText: ' + ErrorText + "\n");
		console.log('Bookmark: thrownError: ' + thrownError + "\n");
	};
	
	/* Create or remove the bookmark of an item */
	Bookmark.prototype.update = function() {
		//console.log("Bookmark: update: In");
		//console.log(this)
		var $this    = this.element
		//console.log($this)
		this.id = parseInt($this.data('id'));
		this.itemtype = parseInt($this.data('ct'));
		this.bookmarkId = parseInt($this.attr('data-bid'));
		//console.log(this.itemtype, this.id, this.bookmarkId);
		
		if (this.bookmarkId != 0) {
			this.requestUrl = window.location.origin + '/bookmark/remove/';
		} else {
			this.requestUrl = window.location.origin + '/bookmark/add/';
		}
		
		var fd = new FormData()
		fd.append('content_type', this.itemtype);
		fd.append('object_id', this.id);
		
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
			data : fd,
			dataType : "json",
			contentType: false,
			processData: false,
			context : $this,
			
			success : this.responseSuccess,
			error : this.responseError,
		});
	};
	
	
	// BOOKMARK PLUGIN DEFINITION
	// ==========================
	
	function Plugin(option) {
		return this.each(function () {
			var $this = $(this)
			var data  = $this.data('bs.bookmark')
			
			if (!data) $this.data('bs.bookmark', (data = new Bookmark(this)))
			//if (typeof option == 'string') data[option].call($this)//It will pass this.element, which we dont need
			if (typeof option == 'string') data[option]()
		})
	}
	
	var old = $.fn.bookmark
	
	$.fn.bookmark             = Plugin
	$.fn.bookmark.Constructor = Bookmark
	
	
	// BOOKMARK NO CONFLICT
	// ====================
	
	$.fn.bookmark.noConflict = function () {
		$.fn.bookmark = old
		return this
	}
	
	
	// APPLY TO STANDARD BOOKMARK ELEMENTS
	// ===================================
	var clickHandler = function (e) {
		//console.log("bookmark: clickHandler: In");
		e.preventDefault();
		Plugin.call($(this), 'update');
	};
	
	//$(document).on('click.bs.bookmark.data-api', ".bookmark-btn", Bookmark.prototype.update);
	$(document).on('click.bs.bookmark.data-api', ".bookmark-btn", clickHandler);
	
	
}(jQuery);