/* ========================================================================
 * name: repository.js
 * info: To load repository items eg. related poetry, recent poetry etc.
 * path: /repository/static/repository/js/repository.js
 * dependencies: /poetry/static/js/shared.js
 * ======================================================================== */

+function ($) {
	'use strict';

	// REPOSITORY PUBLIC CLASS DEFINITION
	// ==================================
	
	var selector_related_poetry = '#id-related-poetry';
	var selector_more_poetry = '#id-more-poetry';
	var selector_more_poetry_btn = '#id-more-poetry-btn';
	
	var Repository = function (element, options) {
		this.itemtype       = null
		this.id             = null
		this.continuation   = null
		this.requestUrl     = null
		this.element       = $(element)
	}
	
	Repository.DEFAULTS = {
		loadingText: 'loading...',
	};
	
	Repository.prototype.getDefaults = function () {
		return Repository.DEFAULTS;
	};
	
	Repository.prototype.getContinuation = function () {
		var continuation = $(selector_more_poetry).data("continuation");
		if (typeof continuation !== typeof undefined && continuation !== false) {
			return continuation;
		} else {
			return "";
		}
	};
	
	Repository.prototype.responseError = function (xhRequest, ErrorText, thrownError) {
		console.log("Repository: response_error:");
		console.log(xhRequest);
		console.log('Repository: ErrorText: ' + ErrorText + "\n");
		console.log('Repository: thrownError: ' + thrownError + "\n");
	};
	
	Repository.prototype.responseSuccess = function(data) {
		//console.log("Repository: response_success: " + data.status);
		
		if ( this.getContinuation() ) {
			var flagCt = true;
			var selector = $(selector_more_poetry);
		} else {
			var selector = $(selector_related_poetry);
		}
		selector.children().remove();
		
		if (data.status == '200') {
			var html = $.parseHTML(data.contenthtml);
			selector.append(html);
			$(selector_more_poetry).attr("data-continuation", data.continuation);
			if (flagCt == true) {
				$(selector_more_poetry_btn).addClass('hidden');
			} else if ( data.continuation ) {
				$(selector_more_poetry_btn).removeClass('hidden');
			}
		} else {
			var html = $.parseHTML('<i class="material-icons mdl-color-text--green-600">highlight_off</i>')
			selector.append(html);
		}
		componentHandler.upgradeDom();
	};
	
	/* Load related Poetry */
	Repository.prototype.loadRelatedPoetry = function() {
		//console.log("Repository: loadRelatedPoetry: In");
		
		var $this    = this.element;
		
		this.itemtype = parseInt($this.data('ct'));
		this.id = parseInt($this.data('id'));
		this.continuation = this.getContinuation();
		this.requestUrl = window.location.origin + $this.data('url') + "?id="+this.id + "&continuation="+this.continuation;
		
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
	
	/* click on Poetry list cards */
	Repository.prototype.clickPoetryCards = function(e) {
		e.stopPropagation();
		if( $(e.target).is('a') || $(e.target.parentNode).is('a')
			|| $(e.target).is('button') ){
			// clicked on `a` or `button` tag.
			return;
		}
		window.document.location = $(this).data("href");
	};

	// REPOSITORY PLUGIN DEFINITION
	// ==========================
	
	function Plugin(option) {
		return this.each(function () {
			var $this = $(this);
			var data  = $this.data('bs.repository');
			
			if (!data) $this.data('bs.repository', (data = new Repository(this)));
			//if (typeof option == 'string') data[option].call($this)//It will pass this.element, which we dont need
			if (typeof option == 'string') data[option]();
		})
	}
	
	var old = $.fn.repository;
	
	$.fn.repository             = Plugin;
	$.fn.repository.Constructor = Repository;
	
	
	// REPOSITORY NO CONFLICT
	// ======================
	$.fn.repository.noConflict = function () {
		$.fn.repository = old;
		return this;
	}
	
	
	// APPLY TO REPOSITORY ELEMENTS
	// ============================
	/** Bind Action: to load related poetry list **/
	var bindActionLoadRelatedPoetry = function() {
		// Call action if element $(selector_related_poetry) present with correct attributes
		if( $(selector_related_poetry).length ) {
			// Check data attributes of the element
			var id = $(selector_related_poetry).attr("data-id");
			var url = $(selector_related_poetry).attr("data-url");
			if ( (typeof id !== typeof undefined && id !== false) &&
				(typeof url !== typeof undefined && url !== false) ) {
				// Call action method
				Plugin.call($(selector_related_poetry), 'loadRelatedPoetry');
			}
		}
	};
	
	var loadMorePoetry = function() {
		// Call action method
		Plugin.call($(selector_related_poetry), 'loadRelatedPoetry');
	};

	$(document).ready(bindActionLoadRelatedPoetry);
	$(document).on('click.bs.repository.data-api', '.poetry-card.small', Repository.prototype.clickPoetryCards);
	$(document).on('click.bs.repository.data-api', selector_more_poetry_btn, loadMorePoetry);
	
}(jQuery);