// Main dit.js file
// Expected to hold global variables, messages, and provide base to namespaces

var dit = {
  // Namespace to be populated by external files
  classes: {},
  components: {}
}
// Utility Functions.
// ---------------------

// REQUIRES
// jQuery
// dit.js

dit.utils = (new function () {

  /* Attempt to generate a unique string
  * e.g. For HTML ID attribute.
  * @str = (String) Allow prefix string.
  **/
  this.generateUniqueStr = function (str) {
    return (str ? str : "") + ((new Date().getTime()) + "_" + Math.random().toString()).replace(/[^\w]*/mig, "");
  }

});

/* Class: Expander
* ----------------
* Expand and collapse a target element by another specified, controlling element,
* or through an automatically added default controller.
*
* Note: The COLLAPSED class is added when the Expander element is closed, so
* you can control CSS the open/close state, or other desired styling.
*
* REQUIRES:
* jquery
* dit.js
* dit.utils.js
*
**/
(function($, utils, classes) {
  var TYPE = "Expander";
  var COLLAPSED = "collapsed";
  var ACTIVE = "active";
  var OPEN = "open";
  var CLOSE = "close";
  var CLICK = "click." + TYPE;
  var BLUR = "blur." + TYPE;
  var FOCUS = "focus." + TYPE;
  var KEY = "keydown." + TYPE;
  var ONMOUSEOUT = "mouseout." + TYPE;
  var ONMOUSEOVER = "mouseover." + TYPE;

  /* Main Class
  * @$target (jQuery node) Target element that should open/close
  * @options (Object) Configuration switches.
  **/
  classes.Expander = Expander;
  function Expander($target, options) {
    var EXPANDER = this;
    var id = utils.generateUniqueStr(TYPE + "_");
    var $wrapper, $control;

    this.config = $.extend({
      blur: true, // If enabled closes on blur.
      cleanup: function() {
        // Additional tasks that may be performed on destroy.
      },
      closed: true, // Whether the item has initial closed state.
      cls: "", // config.wrap ? put on wrapper : put on target.
      complete: function() {
        // You can pass a function to run on open+close
      },
      focus: false, // If enabled puts focus back on activating element target is closed.
      hover: false, // If enabled opens/closes on hover as well.
      text: "Expand", // Control button text.
      wrap: false,
      $control: null // Pass a node if you want to specify something.
    }, options);

    if (arguments.length && $target.length) {

      $control = this.config.$control || $(document.createElement("a"));
      if ($control.get(0).tagName.toLowerCase() === "a") {
        $control.attr("href", "#" + id);
      }

      // Figure out and setup the expanding element
      if(this.config.wrap) {
        $wrapper = $(document.createElement("div"));
        $control.after($wrapper);
        $wrapper.append($target);
        this.$node = $wrapper;
      }
      else {
        id = $target.attr("id") || id; // In case the existing element has its own
        this.$node = $target;
      }

      this.links = {
        $found: $("a", this.$node) || $(),
        counter: -1
      }

      // If we detected any links, enable arrow movement through them.
      this.links.$found.on(KEY, function(e) {
        if (e.which !== 9 && e.which !== 13) {
          e.preventDefault();
        }
        Expander.move.call(EXPANDER, e);
      }).on(BLUR, function(){
        Expander.blur.call(EXPANDER);
      }).on(FOCUS, function() {
        Expander.focus.call(EXPANDER);
      });

      this.$node.before($control);
      this.$node.addClass(TYPE);
      this.$node.addClass(this.config.cls);
      this.$node.attr("id", id);

      // Finish setting up control
      this.$control = $control;
      $control.addClass(TYPE + "Control");
      $control.attr("aria-controls", id);
      $control.attr("aria-expanded", "false");
      $control.attr("aria-haspopup", "true");
      $control.attr("tabindex", 0);
      if($control.text() === "") {
        $control.html(this.config.text)
      }

      // Set initial state
      if (this.config.closed) {
        this.state = OPEN;
        this.close();
      }
      else {
        this.state = CLOSE;
        this.open();
      }

      // Bind events for user interaction
      Expander.bindEvents.call(this);
    }
  }

  /* Class utility function to bind required
  * events upon instantiation. Needs to be run
  * with context of the instantiated object.
  **/
  Expander.bindEvents = function() {
    var EXPANDER = this;

    Expander.AddKeyboardSupport.call(EXPANDER);

    if (EXPANDER.config.hover) {
      Expander.AddHoverSupport.call(EXPANDER);
    }
    else {
      Expander.AddClickSupport.call(EXPANDER);
    }
  }

  /* Add ability to control by keyboard
  **/
  Expander.AddKeyboardSupport = function() {
    var EXPANDER = this;

    EXPANDER.$control.on(KEY, function(e) {
      // keypress charCode=0, keyCode=13 = enter
      if (e.which !== 9 && e.which === 13) {
        e.preventDefault();
      }
      Expander.focus.call(EXPANDER);

      switch(e.which) {
        case 27:
        EXPANDER.close();
        break;
        case 13: // enter
        if (EXPANDER.state === OPEN) {
          EXPANDER.close();
        } else EXPANDER.open();
        break;
        default: ; // Nothing yet.
      }
    });
  }

  /* Add Hover events (for desktop only)
  **/
  Expander.AddHoverSupport = function() {
    var EXPANDER = this;
    var $node = EXPANDER.$node;

    EXPANDER.$control.add($node).on(ONMOUSEOVER, function(event) {
      event.preventDefault();
      Expander.on.call(EXPANDER);
      EXPANDER.open();
    });

    EXPANDER.$control.add($node).on(ONMOUSEOUT, function() {
      Expander.off.call(EXPANDER);
    });

    EXPANDER.$control.on(CLICK, function(event) {
      event.preventDefault();
    });
  }

  /* Using click for desktop and mobile.
  **/
  Expander.AddClickSupport = function() {
    var EXPANDER = this;

    EXPANDER.$control.on(CLICK, function(event) {
      event.preventDefault();
      Expander.on.call(EXPANDER);
      EXPANDER.toggle();
    });

    // And now what happens on blur.
    if(EXPANDER.config.blur) {
      EXPANDER.$control.on(BLUR, function() {
        Expander.blur.call(EXPANDER);
      });
    }
  }

  Expander.on = function() {
    clearTimeout(this.closerequest);
  }

  Expander.off = function() {
    var self = this;
    this.closerequest = setTimeout(function() {
      self.close(true);
    }, 0.5);
  }

  Expander.focus = function() {
    Expander.on.call(this);
  }

  Expander.blur = function() {
    if(this.config.blur && this.state != CLOSE) {
      Expander.off.call(this);
    }
  }

  Expander.move = function(e) {
    var counter = this.links.counter;
    var $links = this.links.$found;
    if($links) {
      switch(e.which) {
        case 37: // Fallthrough
        case 27: this.close();
        break;
        case 40:
        // Down.
        if(counter < ($links.length - 1)) {
          $links.eq(++counter).focus();
        }
        break;
        case 39:
        $links.eq(0).focus();
        break;
        case 38:
        // Up.
        if(counter > 0) {
          $links.eq(--counter).focus();
        }
        else {
          counter--;
          this.close();
        }
        break;
        default: ; // Nothing yet.
      }
    }
    this.links.counter = counter;
  }

  Expander.prototype = new Object;
  Expander.prototype.toggle = function() {
    if(this.state != OPEN) {
      this.open();
    }
    else {
      this.close();
    }
  }

  Expander.prototype.open = function() {
    if(!this._locked && this.state != OPEN) {
      this._locked = true;
      this.state = OPEN;
      this.$control.addClass(ACTIVE);
      this.$node["removeClass"](COLLAPSED);
      this.$control.attr("aria-expanded", "true");
      this.links.$found.attr("tabindex", 0);
      this.config.complete.call(this);
      this._locked = false;
    }
  }

  Expander.prototype.close = function() {
    var focus = this.config.focus;
    if(!this._locked && this.state != CLOSE) {
      this._locked = true;
      this.state = CLOSE;
      this.$control.removeClass(ACTIVE);
      this.$node["addClass"](COLLAPSED);
      this.config.complete.call(this);
      this.$control.attr("aria-expanded", "false");
      this.links.$found.attr("tabindex", -1);
      if(focus) {
        this.$control.focus();
      }
      this.links.counter = -1; // Reset.
      this._locked = false;
    }
  }

  Expander.prototype.destroy = function() {
    var events = CLICK + " " + BLUR + " " + FOCUS + " " + KEY + " " + ONMOUSEOUT + " " + ONMOUSEOVER;
    if(this.config.wrap) {
      this.$node.replaceWith(this.$node.contents());
    }
    else {
      this.$node.removeClass(this.config.cls);
      this.$node.removeClass(COLLAPSED);
      this.$node.removeClass(TYPE);
    }

    if(this.config.$control) {
      this.$control.off(events);
      this.$control.removeClass(this.config.cls + "Control");
      this.$control.removeAttr("tabindex");
      this.$control.removeAttr("aria-controls");
      this.$control.removeAttr("aria-expanded");
      this.$control.removeAttr("aria-haspopup");
    }
    else {
      this.$control.remove();
    }

    this.links.$found.off(events);
    this.links.$found.removeAttr("tabindex");
    this.config.cleanup();
  }

})(jQuery, dit.utils, dit.classes);

/* Class will add a controller before the $target element.
* The triggered event will toggle a class on the target element and controller.
* the target element with collapse, or expand.
*
* Note: The COLLAPSED class is added when the Expander element is closed, so
* you can add additional CSS for this state. Inline style, display:none is
* added by the code (mainly only because IE8 doesn't support CSS transitions).
*
* REQUIRES:
* jquery
* dit.js
* dit.utils.js
* dit.classes.expander.js
*
**/

(function($, utils, classes) {

  function Accordion(items, open, close) {
    if (arguments.length) {
      this.items = items;

      for (var i=0; i<items.length; ++i) {
        Accordion.enhance.call(this, items[i], open, close);
      }
    }
  }
  Accordion.enhance = function(target, open, close) {
    var items = this.items;
    var originalOpen = target[open];
    target[open] = function() {
      for(var i=0; i<items.length; ++i) {
        if(items[i] !== target) {
          items[i][close]();
        }
      }
      originalOpen.call(target);
    }
  }

  classes.Accordion = Accordion;
})(jQuery, dit.utils, dit.classes);

// Responsive Functionality.
// Adds functionality to help control JS responsive code.
// Needs corresponding CSS (using media queries) to control
// the values. See getResponsiveValue();
// E.g.
//
// Requires...
// dit.js
//

dit.responsive = (new function () {

  // Constants
  var RESET_EVENT = "dit:responsive:reset";
  var RESPONSIVE_ELEMENT_ID = "dit-responsive-size";

  // Sizing difference must be greater than this to trigger the events.
  // This is and attempt to restrict the number of changes when, for
  // example, resizing the screen by dragging.
  var ARBITRARY_DIFFERENCE_MEASUREMENT = 50;

  // Private
  var _self = this;
  var _rotating = false;
  var _responsiveValues = [];
  var _height = 0;
  var _width = 0;


  /* Detect responsive size in play.
  * Use CSS media queries to control z-index values of the
  * #RESPONSIVE_ELEMENT_ID hidden element. Detected value
  * should match up with index number of _responsiveValues
  * array. dit.responsive.mode() will return a string that
  * should give the current responsive mode.
  * E.g. For _responsiveValues array ["desktop", "table", "mobile"],
  * the expected z-index values would be:
  * desktop = 0
  * tablet = 1
  * mobile = 2
  **/
  function getResponsiveValue() {
    return Number($("#" + RESPONSIVE_ELEMENT_ID).css("z-index"));
  };

  /* Create and append a hidden element to track the responsive
  * size. Note: You need to add CSS to set the z-index property
  * of the element. Do this using media queries so that it fits
  * in with other media query controlled responsive sizing.
  * See _responsiveValues variable for expected values (the
  * array index should match the set z-index value).
  **/
  function addResponsiveTrackingElement() {
    var $responsiveElement = $("<span></span>");
    $responsiveElement.attr("id", RESPONSIVE_ELEMENT_ID);
    $responsiveElement.css({
      "height": "1px",
      "position": "absolute",
      "top": "-1px",
      "visibility": "hidden",
      "width": "1px"
    })

    $(document.body).append($responsiveElement);
  }

  /* Create in-page <style> tag containing set media query
  * breakpoints passed to dit.responsive.init()
  * @queries (Object) Media queries and label - e.g. { desktop: "min-width: 1200px" }
  **/
  function addResponsiveSizes(queries) {
    var $style = $("<style id=\"dit-responsive-css\" type=\"text/css\"></style>");
    var css = "";
    var index = 0;
    for(var query in queries) {
      if(queries.hasOwnProperty(query)) {
        _responsiveValues.push(query);
        css += "@media (" + queries[query] + ") {\n";
        css += " #"  + RESPONSIVE_ELEMENT_ID + "{\n";
        css += "   z-index: " + index + ";\n";
        css += "  }\n";
        css += "}\n\n";
        index++;
      }
    }

    $style.text(css);
    $(document.head).append($style);
  }

  /* Triggers jQuery custom event on body for JS elements
  * listening to resize changes (e.g. screen rotate).
  **/
  function bindResizeEvent() {
    $(window).on("resize", function () {
      if (!_rotating) {
        _rotating = true;
        setTimeout(function () {
          if (_rotating) {
            _rotating = false;
            if(dimensionChangeWasBigEnough()) {
              $(document.body).trigger(RESET_EVENT, [_self.mode()]);
            }
          }
        }, "1000");
      }
    });
  }

  /* Calculate if window dimensions have changed enough
  * to trigger a reset event. Note: This was added
  * because some mobile browsers hide the address bar
  * on scroll, which otherwise gives false positive
  * when trying to detect a resize.
  **/
  function dimensionChangeWasBigEnough() {
    var height = $(window).height();
    var width = $(window).width();
    var result = false;

    if (Math.abs(height - _height) >= ARBITRARY_DIFFERENCE_MEASUREMENT) {
      result = true;
    }

    if (Math.abs(width - _width) >= ARBITRARY_DIFFERENCE_MEASUREMENT) {
      result = true;
    }

    // Update internals with latest values
    _height = height;
    _width = width;

    return result;
  }

  /* Return the detected current responsive mode */
  this.mode = function() {
    return _responsiveValues[getResponsiveValue()];
  };

  this.reset = RESET_EVENT;

  this.init = function(breakpoints) {
    addResponsiveSizes(breakpoints);
    addResponsiveTrackingElement();
    bindResizeEvent();
  }
});


// Header code
//
// Requires
// jQuery
// dit.js
// dit.components.js
//
dit.investHeader = (new function () {
  // Page init
  this.init = function() {
    dit.responsive.init({
      "desktop": "min-width: 768px",
      "tablet" : "max-width: 767px",
      "mobile" : "max-width: 480px"
    });

    headerMenuExpander();
    delete this.init; // Run once
  }

  // Set up header menu expander
  function headerMenuExpander() {
    var $this = $('.header-links-list');
    new dit.classes.Expander($this, {
      hover: false,
      blur: true,
      wrap: false,
      $control: $('.header-menu-activator')
    });
  }
});

$(document).ready(function() {
  dit.investHeader.init();
});
