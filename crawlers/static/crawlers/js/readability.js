/* ========================================================================
 * name: readability.js
 * info: To load readability item for a given url.
 * path: /crawlers/static/crawlers/js/readability.js
 * dependencies: /poetry/static/js/shared.js
 * ======================================================================== */

+function ($) {
	'use strict';

	// PUBLIC CLASS DEFINITION
	// ==================================
	var selector_fetch_url = '#id-fetch-url';
	
	var Readability = function (element, options) {
		this.url             = null
		this.requestUrl     = null
		this.element       = $(element)
	}
	
	Readability.DEFAULTS = {
		loadingText: 'loading...',
	};
	
	Readability.prototype.getDefaults = function () {
		return Readability.DEFAULTS;
	};
	
	Readability.prototype.responseError = function (xhRequest, ErrorText, thrownError) {
		console.log("Readability: response_error:");
		console.log(xhRequest);
		console.log('Readability: ErrorText: ' + ErrorText + "\n");
		console.log('Readability: thrownError: ' + thrownError + "\n");
		
		$('dialog div.dialog-loading').removeClass('is-active');
		var dialog_content = $('dialog div.mdl-dialog__content');
		dialog_content.empty();
		dialog_content.text('Unexpected error occurred!');
		$(selector_fetch_url).removeClass('hidden');
	};
	
	Readability.prototype.responseSuccess = function(data) {
		//console.log("Readability: response_success: " + data.status);
		$('dialog div.dialog-loading').removeClass('is-active');
		var dialog_content = $('dialog div.mdl-dialog__content');
		dialog_content.empty();
		
		if (data.status == '200') {
			var html = $.parseHTML(data.contenthtml);
			dialog_content.append(html);

		} else {
			dialog_content.text('Something went wrong! < error '+data.status+'>');
		}
		$(selector_fetch_url).removeClass('hidden');
		componentHandler.upgradeDom();
	};
	
	/* Load readable view of an url */
	Readability.prototype.loadReadable = function() {
		//console.log("Readability: loadReadable: In");
		
		$(selector_fetch_url).addClass('hidden');
		
		var dialog = document.querySelector('dialog');
		if (!dialog.showModal) {
			dialogPolyfill.registerDialog(dialog);
		}
		dialog.querySelector('.close').addEventListener('click', function() {
			dialog.close();
		});
		$('dialog div.mdl-dialog__content').empty();
		$('dialog div.dialog-loading').addClass('is-active');
		dialog.showModal();
		
		var $this    = this.element;
		this.url = $this.data('url');
		this.fetch = $this.data('fetch');
		this.requestUrl = window.location.origin + $this.data('url') + "?url="+this.fetch;
		
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

	// PLUGIN DEFINITION
	// ==========================
	
	function Plugin(option) {
		return this.each(function () {
			var $this = $(this);
			var data  = $this.data('bs.readability');
			
			if (!data) $this.data('bs.readability', (data = new Readability(this)));
			//if (typeof option == 'string') data[option].call($this)//It will pass this.element, which we dont need
			if (typeof option == 'string') data[option]();
		})
	}
	
	var old = $.fn.readability;
	
	$.fn.readability             = Plugin;
	$.fn.readability.Constructor = Readability;
	
	
	// NO CONFLICT
	// ======================
	$.fn.readability.noConflict = function () {
		$.fn.readability = old;
		return this;
	}
	
	
	// APPLY TO READABILITY ELEMENTS
	// =============================
	var fetchUrl = function() {
		// Call action method
		Plugin.call($(selector_fetch_url), 'loadReadable');
	};

	$(document).on('click.bs.readability.data-api', selector_fetch_url, fetchUrl);
	
}(jQuery);

