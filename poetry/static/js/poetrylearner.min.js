/*!
 * Checking jQuery and its version
 */

if (typeof jQuery === 'undefined') {
  throw new Error('This JavaScript requires jQuery')
}

+function ($) {
  'use strict';
  var version = $.fn.jquery.split(' ')[0].split('.')
  if ((version[0] < 2 && version[1] < 9) || (version[0] == 1 && version[1] == 9 && version[2] < 1)) {
    throw new Error('This JavaScript requires jQuery version 1.9.1 or higher')
  }
}(jQuery);

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
 * Bootstrap: modal.js v3.3.4
 * http://getbootstrap.com/javascript/#modals
 * ========================================================================
 * Copyright 2011-2015 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // MODAL CLASS DEFINITION
  // ======================

  var Modal = function (element, options) {
    this.options             = options
    this.$body               = $(document.body)
    this.$element            = $(element)
    this.$dialog             = this.$element.find('.modal-dialog')
    this.$backdrop           = null
    this.isShown             = null
    this.originalBodyPad     = null
    this.scrollbarWidth      = 0
    this.ignoreBackdropClick = false

    if (this.options.remote) {
      this.$element
        .find('.modal-content')
        .load(this.options.remote, $.proxy(function () {
          this.$element.trigger('loaded.bs.modal')
        }, this))
    }
  }

  Modal.VERSION  = '3.3.4'

  Modal.TRANSITION_DURATION = 300
  Modal.BACKDROP_TRANSITION_DURATION = 150

  Modal.DEFAULTS = {
    backdrop: true,
    keyboard: true,
    show: true
  }

  Modal.prototype.toggle = function (_relatedTarget) {
    return this.isShown ? this.hide() : this.show(_relatedTarget)
  }

  Modal.prototype.show = function (_relatedTarget) {
    var that = this
    var e    = $.Event('show.bs.modal', { relatedTarget: _relatedTarget })

    this.$element.trigger(e)

    if (this.isShown || e.isDefaultPrevented()) return

    this.isShown = true

    this.checkScrollbar()
    this.setScrollbar()
    this.$body.addClass('modal-open')

    this.escape()
    this.resize()

    this.$element.on('click.dismiss.bs.modal', '[data-dismiss="modal"]', $.proxy(this.hide, this))

    this.$dialog.on('mousedown.dismiss.bs.modal', function () {
      that.$element.one('mouseup.dismiss.bs.modal', function (e) {
        if ($(e.target).is(that.$element)) that.ignoreBackdropClick = true
      })
    })

    this.backdrop(function () {
      var transition = $.support.transition && that.$element.hasClass('fade')

      if (!that.$element.parent().length) {
        that.$element.appendTo(that.$body) // don't move modals dom position
      }

      that.$element
        .show()
        .scrollTop(0)

      that.adjustDialog()

      if (transition) {
        that.$element[0].offsetWidth // force reflow
      }

      that.$element
        .addClass('in')
        .attr('aria-hidden', false)

      that.enforceFocus()

      var e = $.Event('shown.bs.modal', { relatedTarget: _relatedTarget })

      transition ?
        that.$dialog // wait for modal to slide in
          .one('bsTransitionEnd', function () {
            that.$element.trigger('focus').trigger(e)
          })
          .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
        that.$element.trigger('focus').trigger(e)
    })
  }

  Modal.prototype.hide = function (e) {
    if (e) e.preventDefault()

    e = $.Event('hide.bs.modal')

    this.$element.trigger(e)

    if (!this.isShown || e.isDefaultPrevented()) return

    this.isShown = false

    this.escape()
    this.resize()

    $(document).off('focusin.bs.modal')

    this.$element
      .removeClass('in')
      .attr('aria-hidden', true)
      .off('click.dismiss.bs.modal')
      .off('mouseup.dismiss.bs.modal')

    this.$dialog.off('mousedown.dismiss.bs.modal')

    $.support.transition && this.$element.hasClass('fade') ?
      this.$element
        .one('bsTransitionEnd', $.proxy(this.hideModal, this))
        .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
      this.hideModal()
  }

  Modal.prototype.enforceFocus = function () {
    $(document)
      .off('focusin.bs.modal') // guard against infinite focus loop
      .on('focusin.bs.modal', $.proxy(function (e) {
        if (this.$element[0] !== e.target && !this.$element.has(e.target).length) {
          this.$element.trigger('focus')
        }
      }, this))
  }

  Modal.prototype.escape = function () {
    if (this.isShown && this.options.keyboard) {
      this.$element.on('keydown.dismiss.bs.modal', $.proxy(function (e) {
        e.which == 27 && this.hide()
      }, this))
    } else if (!this.isShown) {
      this.$element.off('keydown.dismiss.bs.modal')
    }
  }

  Modal.prototype.resize = function () {
    if (this.isShown) {
      $(window).on('resize.bs.modal', $.proxy(this.handleUpdate, this))
    } else {
      $(window).off('resize.bs.modal')
    }
  }

  Modal.prototype.hideModal = function () {
    var that = this
    this.$element.hide()
    this.backdrop(function () {
      that.$body.removeClass('modal-open')
      that.resetAdjustments()
      that.resetScrollbar()
      that.$element.trigger('hidden.bs.modal')
    })
  }

  Modal.prototype.removeBackdrop = function () {
    this.$backdrop && this.$backdrop.remove()
    this.$backdrop = null
  }

  Modal.prototype.backdrop = function (callback) {
    var that = this
    var animate = this.$element.hasClass('fade') ? 'fade' : ''

    if (this.isShown && this.options.backdrop) {
      var doAnimate = $.support.transition && animate

      this.$backdrop = $('<div class="modal-backdrop ' + animate + '" />')
        .appendTo(this.$body)

      this.$element.on('click.dismiss.bs.modal', $.proxy(function (e) {
        if (this.ignoreBackdropClick) {
          this.ignoreBackdropClick = false
          return
        }
        if (e.target !== e.currentTarget) return
        this.options.backdrop == 'static'
          ? this.$element[0].focus()
          : this.hide()
      }, this))

      if (doAnimate) this.$backdrop[0].offsetWidth // force reflow

      this.$backdrop.addClass('in')

      if (!callback) return

      doAnimate ?
        this.$backdrop
          .one('bsTransitionEnd', callback)
          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
        callback()

    } else if (!this.isShown && this.$backdrop) {
      this.$backdrop.removeClass('in')

      var callbackRemove = function () {
        that.removeBackdrop()
        callback && callback()
      }
      $.support.transition && this.$element.hasClass('fade') ?
        this.$backdrop
          .one('bsTransitionEnd', callbackRemove)
          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
        callbackRemove()

    } else if (callback) {
      callback()
    }
  }

  // these following methods are used to handle overflowing modals

  Modal.prototype.handleUpdate = function () {
    this.adjustDialog()
  }

  Modal.prototype.adjustDialog = function () {
    var modalIsOverflowing = this.$element[0].scrollHeight > document.documentElement.clientHeight

    this.$element.css({
      paddingLeft:  !this.bodyIsOverflowing && modalIsOverflowing ? this.scrollbarWidth : '',
      paddingRight: this.bodyIsOverflowing && !modalIsOverflowing ? this.scrollbarWidth : ''
    })
  }

  Modal.prototype.resetAdjustments = function () {
    this.$element.css({
      paddingLeft: '',
      paddingRight: ''
    })
  }

  Modal.prototype.checkScrollbar = function () {
    var fullWindowWidth = window.innerWidth
    if (!fullWindowWidth) { // workaround for missing window.innerWidth in IE8
      var documentElementRect = document.documentElement.getBoundingClientRect()
      fullWindowWidth = documentElementRect.right - Math.abs(documentElementRect.left)
    }
    this.bodyIsOverflowing = document.body.clientWidth < fullWindowWidth
    this.scrollbarWidth = this.measureScrollbar()
  }

  Modal.prototype.setScrollbar = function () {
    var bodyPad = parseInt((this.$body.css('padding-right') || 0), 10)
    this.originalBodyPad = document.body.style.paddingRight || ''
    if (this.bodyIsOverflowing) this.$body.css('padding-right', bodyPad + this.scrollbarWidth)
  }

  Modal.prototype.resetScrollbar = function () {
    this.$body.css('padding-right', this.originalBodyPad)
  }

  Modal.prototype.measureScrollbar = function () { // thx walsh
    var scrollDiv = document.createElement('div')
    scrollDiv.className = 'modal-scrollbar-measure'
    this.$body.append(scrollDiv)
    var scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth
    this.$body[0].removeChild(scrollDiv)
    return scrollbarWidth
  }


  // MODAL PLUGIN DEFINITION
  // =======================

  function Plugin(option, _relatedTarget) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.modal')
      var options = $.extend({}, Modal.DEFAULTS, $this.data(), typeof option == 'object' && option)

      if (!data) $this.data('bs.modal', (data = new Modal(this, options)))
      if (typeof option == 'string') data[option](_relatedTarget)
      else if (options.show) data.show(_relatedTarget)
    })
  }

  var old = $.fn.modal

  $.fn.modal             = Plugin
  $.fn.modal.Constructor = Modal


  // MODAL NO CONFLICT
  // =================

  $.fn.modal.noConflict = function () {
    $.fn.modal = old
    return this
  }


  // MODAL DATA-API
  // ==============

  $(document).on('click.bs.modal.data-api', '[data-toggle="modal"]', function (e) {
    var $this   = $(this)
    var href    = $this.attr('href')
    var $target = $($this.attr('data-target') || (href && href.replace(/.*(?=#[^\s]+$)/, ''))) // strip for ie7
    var option  = $target.data('bs.modal') ? 'toggle' : $.extend({ remote: !/#/.test(href) && href }, $target.data(), $this.data())

    if ($this.is('a')) e.preventDefault()

    $target.one('show.bs.modal', function (showEvent) {
      if (showEvent.isDefaultPrevented()) return // only register focus restorer if modal will actually get shown
      $target.one('hidden.bs.modal', function () {
        $this.is(':visible') && $this.trigger('focus')
      })
    })
    Plugin.call($target, option, this)
  })

}(jQuery);

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
	
	
}(jQuery);/* ========================================================================
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
			if (data.bid != 0) {
				$(this).addClass("true");
				$(this).attr('data-bid', data.bid);
				$(this).prop('title', 'Remove from my Bookmarks');
			} else {
				$(this).removeClass("true");
				$(this).attr('data-bid', data.bid);
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
		this.itemtype = parseInt($this.data('type'));
		this.bookmarkId = parseInt($this.attr('data-bid'));
		//console.log(this.itemtype, this.id, this.bookmarkId);
		
		// Return if the data items are not valid
		if (isNaN(this.id) || isNaN(this.itemtype) || isNaN(this.bookmarkId)) {
			console.log("Bookmark: invalid params");
			return;
		}
		
		if (this.bookmarkId != 0) {
			this.requestUrl = window.location.origin + '/bookmark/remove/';
		} else {
			this.requestUrl = window.location.origin + '/bookmark/add/';
		}
		
		var fd = new FormData()
		fd.append('type', this.itemtype);
		fd.append('id', this.id);
		
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
	
	//$(document).on('click.bs.bookmark.data-api', ".bookmark-js-button", Bookmark.prototype.update);
	$(document).on('click.bs.bookmark.data-api', ".bookmark-js-button", clickHandler);
	
	
}(jQuery);

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
	var selector_more_poetry_loading = '#id-more-poetry-loading';
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
		$(selector_more_poetry_loading).text('error loading suggestions :(');
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
			$(selector_more_poetry_loading).addClass('hidden');
			var html = $.parseHTML(data.contenthtml);
			selector.append(html);
			$(selector_more_poetry).attr("data-continuation", data.continuation);
			if ( (!flagCt) && (data.continuation) ) {
				$(selector_more_poetry_btn).removeClass('hidden');
			}
		} else {
			$(selector_more_poetry_loading).text('error loading suggestions!');
		}
		componentHandler.upgradeDom();
	};
	
	/* Load related Poetry */
	Repository.prototype.loadRelatedPoetry = function() {
		//console.log("Repository: loadRelatedPoetry: In");
		
		$(selector_more_poetry_btn).addClass('hidden');
		$(selector_more_poetry_loading).removeClass('hidden');
		
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



