/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"installer": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/static/app_installer/dist/";
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push([5,"react","lodashLib","extVendors","polyfill","semanticUI"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/@babel/polyfill/lib/noConflict.js":
/*!********************************************************!*\
  !*** ./node_modules/@babel/polyfill/lib/noConflict.js ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


__webpack_require__(/*! core-js/es6 */ "./node_modules/core-js/es6/index.js");

__webpack_require__(/*! core-js/fn/array/includes */ "./node_modules/core-js/fn/array/includes.js");

__webpack_require__(/*! core-js/fn/string/pad-start */ "./node_modules/core-js/fn/string/pad-start.js");

__webpack_require__(/*! core-js/fn/string/pad-end */ "./node_modules/core-js/fn/string/pad-end.js");

__webpack_require__(/*! core-js/fn/symbol/async-iterator */ "./node_modules/core-js/fn/symbol/async-iterator.js");

__webpack_require__(/*! core-js/fn/object/get-own-property-descriptors */ "./node_modules/core-js/fn/object/get-own-property-descriptors.js");

__webpack_require__(/*! core-js/fn/object/values */ "./node_modules/core-js/fn/object/values.js");

__webpack_require__(/*! core-js/fn/object/entries */ "./node_modules/core-js/fn/object/entries.js");

__webpack_require__(/*! core-js/fn/promise/finally */ "./node_modules/core-js/fn/promise/finally.js");

__webpack_require__(/*! core-js/web */ "./node_modules/core-js/web/index.js");

__webpack_require__(/*! regenerator-runtime/runtime */ "./node_modules/regenerator-runtime/runtime.js");

/***/ }),

/***/ "./node_modules/@babel/polyfill/noConflict.js":
/*!****************************************************!*\
  !*** ./node_modules/@babel/polyfill/noConflict.js ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


__webpack_require__(/*! ./lib/noConflict */ "./node_modules/@babel/polyfill/lib/noConflict.js");

/***/ }),

/***/ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/index.js?!./node_modules/postcss-loader/src/index.js?!./node_modules/semantic-ui-css/semantic.min.css":
/*!********************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader??ref--5-2!./node_modules/postcss-loader/src??postcss!./node_modules/semantic-ui-css/semantic.min.css ***!
  \********************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/index.js?!./node_modules/postcss-loader/src/index.js?!./src/css/installer.css":
/*!********************************************************************************************************************************************************************!*\
  !*** ./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader??ref--5-2!./node_modules/postcss-loader/src??postcss!./src/css/installer.css ***!
  \********************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "./node_modules/redux-devtools-extension/index.js":
/*!********************************************************!*\
  !*** ./node_modules/redux-devtools-extension/index.js ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

var compose = __webpack_require__(/*! redux */ "./node_modules/redux/es/redux.js").compose;

exports.__esModule = true;
exports.composeWithDevTools = typeof window !== 'undefined' && window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ ? window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ : function () {
  if (arguments.length === 0) return undefined;
  if (_typeof(arguments[0]) === 'object') return compose;
  return compose.apply(null, arguments);
};

exports.devToolsEnhancer = typeof window !== 'undefined' && window.__REDUX_DEVTOOLS_EXTENSION__ ? window.__REDUX_DEVTOOLS_EXTENSION__ : function () {
  return function (noop) {
    return noop;
  };
};

/***/ }),

/***/ "./node_modules/redux-thunk/es/index.js":
/*!**********************************************!*\
  !*** ./node_modules/redux-thunk/es/index.js ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
function createThunkMiddleware(extraArgument) {
  return function (_ref) {
    var dispatch = _ref.dispatch,
        getState = _ref.getState;
    return function (next) {
      return function (action) {
        if (typeof action === 'function') {
          return action(dispatch, getState, extraArgument);
        }

        return next(action);
      };
    };
  };
}

var thunk = createThunkMiddleware();
thunk.withExtraArgument = createThunkMiddleware;

exports.default = thunk;

/***/ }),

/***/ "./node_modules/semantic-ui-css/semantic.min.css":
/*!*******************************************************!*\
  !*** ./node_modules/semantic-ui-css/semantic.min.css ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {


var content = __webpack_require__(/*! !../mini-css-extract-plugin/dist/loader.js!../css-loader??ref--5-2!../postcss-loader/src??postcss!./semantic.min.css */ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/index.js?!./node_modules/postcss-loader/src/index.js?!./node_modules/semantic-ui-css/semantic.min.css");

if(typeof content === 'string') content = [[module.i, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! ../style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ "./node_modules/style-loader/lib/addStyles.js":
/*!****************************************************!*\
  !*** ./node_modules/style-loader/lib/addStyles.js ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/

var stylesInDom = {};

var	memoize = function (fn) {
	var memo;

	return function () {
		if (typeof memo === "undefined") memo = fn.apply(this, arguments);
		return memo;
	};
};

var isOldIE = memoize(function () {
	// Test for IE <= 9 as proposed by Browserhacks
	// @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
	// Tests for existence of standard globals is to allow style-loader
	// to operate correctly into non-standard environments
	// @see https://github.com/webpack-contrib/style-loader/issues/177
	return window && document && document.all && !window.atob;
});

var getTarget = function (target, parent) {
  if (parent){
    return parent.querySelector(target);
  }
  return document.querySelector(target);
};

var getElement = (function (fn) {
	var memo = {};

	return function(target, parent) {
                // If passing function in options, then use it for resolve "head" element.
                // Useful for Shadow Root style i.e
                // {
                //   insertInto: function () { return document.querySelector("#foo").shadowRoot }
                // }
                if (typeof target === 'function') {
                        return target();
                }
                if (typeof memo[target] === "undefined") {
			var styleTarget = getTarget.call(this, target, parent);
			// Special case to return head of iframe instead of iframe itself
			if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
				try {
					// This will throw an exception if access to iframe is blocked
					// due to cross-origin restrictions
					styleTarget = styleTarget.contentDocument.head;
				} catch(e) {
					styleTarget = null;
				}
			}
			memo[target] = styleTarget;
		}
		return memo[target]
	};
})();

var singleton = null;
var	singletonCounter = 0;
var	stylesInsertedAtTop = [];

var	fixUrls = __webpack_require__(/*! ./urls */ "./node_modules/style-loader/lib/urls.js");

module.exports = function(list, options) {
	if (typeof DEBUG !== "undefined" && DEBUG) {
		if (typeof document !== "object") throw new Error("The style-loader cannot be used in a non-browser environment");
	}

	options = options || {};

	options.attrs = typeof options.attrs === "object" ? options.attrs : {};

	// Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
	// tags it will allow on a page
	if (!options.singleton && typeof options.singleton !== "boolean") options.singleton = isOldIE();

	// By default, add <style> tags to the <head> element
        if (!options.insertInto) options.insertInto = "head";

	// By default, add <style> tags to the bottom of the target
	if (!options.insertAt) options.insertAt = "bottom";

	var styles = listToStyles(list, options);

	addStylesToDom(styles, options);

	return function update (newList) {
		var mayRemove = [];

		for (var i = 0; i < styles.length; i++) {
			var item = styles[i];
			var domStyle = stylesInDom[item.id];

			domStyle.refs--;
			mayRemove.push(domStyle);
		}

		if(newList) {
			var newStyles = listToStyles(newList, options);
			addStylesToDom(newStyles, options);
		}

		for (var i = 0; i < mayRemove.length; i++) {
			var domStyle = mayRemove[i];

			if(domStyle.refs === 0) {
				for (var j = 0; j < domStyle.parts.length; j++) domStyle.parts[j]();

				delete stylesInDom[domStyle.id];
			}
		}
	};
};

function addStylesToDom (styles, options) {
	for (var i = 0; i < styles.length; i++) {
		var item = styles[i];
		var domStyle = stylesInDom[item.id];

		if(domStyle) {
			domStyle.refs++;

			for(var j = 0; j < domStyle.parts.length; j++) {
				domStyle.parts[j](item.parts[j]);
			}

			for(; j < item.parts.length; j++) {
				domStyle.parts.push(addStyle(item.parts[j], options));
			}
		} else {
			var parts = [];

			for(var j = 0; j < item.parts.length; j++) {
				parts.push(addStyle(item.parts[j], options));
			}

			stylesInDom[item.id] = {id: item.id, refs: 1, parts: parts};
		}
	}
}

function listToStyles (list, options) {
	var styles = [];
	var newStyles = {};

	for (var i = 0; i < list.length; i++) {
		var item = list[i];
		var id = options.base ? item[0] + options.base : item[0];
		var css = item[1];
		var media = item[2];
		var sourceMap = item[3];
		var part = {css: css, media: media, sourceMap: sourceMap};

		if(!newStyles[id]) styles.push(newStyles[id] = {id: id, parts: [part]});
		else newStyles[id].parts.push(part);
	}

	return styles;
}

function insertStyleElement (options, style) {
	var target = getElement(options.insertInto)

	if (!target) {
		throw new Error("Couldn't find a style target. This probably means that the value for the 'insertInto' parameter is invalid.");
	}

	var lastStyleElementInsertedAtTop = stylesInsertedAtTop[stylesInsertedAtTop.length - 1];

	if (options.insertAt === "top") {
		if (!lastStyleElementInsertedAtTop) {
			target.insertBefore(style, target.firstChild);
		} else if (lastStyleElementInsertedAtTop.nextSibling) {
			target.insertBefore(style, lastStyleElementInsertedAtTop.nextSibling);
		} else {
			target.appendChild(style);
		}
		stylesInsertedAtTop.push(style);
	} else if (options.insertAt === "bottom") {
		target.appendChild(style);
	} else if (typeof options.insertAt === "object" && options.insertAt.before) {
		var nextSibling = getElement(options.insertAt.before, target);
		target.insertBefore(style, nextSibling);
	} else {
		throw new Error("[Style Loader]\n\n Invalid value for parameter 'insertAt' ('options.insertAt') found.\n Must be 'top', 'bottom', or Object.\n (https://github.com/webpack-contrib/style-loader#insertat)\n");
	}
}

function removeStyleElement (style) {
	if (style.parentNode === null) return false;
	style.parentNode.removeChild(style);

	var idx = stylesInsertedAtTop.indexOf(style);
	if(idx >= 0) {
		stylesInsertedAtTop.splice(idx, 1);
	}
}

function createStyleElement (options) {
	var style = document.createElement("style");

	if(options.attrs.type === undefined) {
		options.attrs.type = "text/css";
	}

	if(options.attrs.nonce === undefined) {
		var nonce = getNonce();
		if (nonce) {
			options.attrs.nonce = nonce;
		}
	}

	addAttrs(style, options.attrs);
	insertStyleElement(options, style);

	return style;
}

function createLinkElement (options) {
	var link = document.createElement("link");

	if(options.attrs.type === undefined) {
		options.attrs.type = "text/css";
	}
	options.attrs.rel = "stylesheet";

	addAttrs(link, options.attrs);
	insertStyleElement(options, link);

	return link;
}

function addAttrs (el, attrs) {
	Object.keys(attrs).forEach(function (key) {
		el.setAttribute(key, attrs[key]);
	});
}

function getNonce() {
	if (false) {}

	return __webpack_require__.nc;
}

function addStyle (obj, options) {
	var style, update, remove, result;

	// If a transform function was defined, run it on the css
	if (options.transform && obj.css) {
	    result = typeof options.transform === 'function'
		 ? options.transform(obj.css) 
		 : options.transform.default(obj.css);

	    if (result) {
	    	// If transform returns a value, use that instead of the original css.
	    	// This allows running runtime transformations on the css.
	    	obj.css = result;
	    } else {
	    	// If the transform function returns a falsy value, don't add this css.
	    	// This allows conditional loading of css
	    	return function() {
	    		// noop
	    	};
	    }
	}

	if (options.singleton) {
		var styleIndex = singletonCounter++;

		style = singleton || (singleton = createStyleElement(options));

		update = applyToSingletonTag.bind(null, style, styleIndex, false);
		remove = applyToSingletonTag.bind(null, style, styleIndex, true);

	} else if (
		obj.sourceMap &&
		typeof URL === "function" &&
		typeof URL.createObjectURL === "function" &&
		typeof URL.revokeObjectURL === "function" &&
		typeof Blob === "function" &&
		typeof btoa === "function"
	) {
		style = createLinkElement(options);
		update = updateLink.bind(null, style, options);
		remove = function () {
			removeStyleElement(style);

			if(style.href) URL.revokeObjectURL(style.href);
		};
	} else {
		style = createStyleElement(options);
		update = applyToTag.bind(null, style);
		remove = function () {
			removeStyleElement(style);
		};
	}

	update(obj);

	return function updateStyle (newObj) {
		if (newObj) {
			if (
				newObj.css === obj.css &&
				newObj.media === obj.media &&
				newObj.sourceMap === obj.sourceMap
			) {
				return;
			}

			update(obj = newObj);
		} else {
			remove();
		}
	};
}

var replaceText = (function () {
	var textStore = [];

	return function (index, replacement) {
		textStore[index] = replacement;

		return textStore.filter(Boolean).join('\n');
	};
})();

function applyToSingletonTag (style, index, remove, obj) {
	var css = remove ? "" : obj.css;

	if (style.styleSheet) {
		style.styleSheet.cssText = replaceText(index, css);
	} else {
		var cssNode = document.createTextNode(css);
		var childNodes = style.childNodes;

		if (childNodes[index]) style.removeChild(childNodes[index]);

		if (childNodes.length) {
			style.insertBefore(cssNode, childNodes[index]);
		} else {
			style.appendChild(cssNode);
		}
	}
}

function applyToTag (style, obj) {
	var css = obj.css;
	var media = obj.media;

	if(media) {
		style.setAttribute("media", media)
	}

	if(style.styleSheet) {
		style.styleSheet.cssText = css;
	} else {
		while(style.firstChild) {
			style.removeChild(style.firstChild);
		}

		style.appendChild(document.createTextNode(css));
	}
}

function updateLink (link, options, obj) {
	var css = obj.css;
	var sourceMap = obj.sourceMap;

	/*
		If convertToAbsoluteUrls isn't defined, but sourcemaps are enabled
		and there is no publicPath defined then lets turn convertToAbsoluteUrls
		on by default.  Otherwise default to the convertToAbsoluteUrls option
		directly
	*/
	var autoFixUrls = options.convertToAbsoluteUrls === undefined && sourceMap;

	if (options.convertToAbsoluteUrls || autoFixUrls) {
		css = fixUrls(css);
	}

	if (sourceMap) {
		// http://stackoverflow.com/a/26603875
		css += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))) + " */";
	}

	var blob = new Blob([css], { type: "text/css" });

	var oldSrc = link.href;

	link.href = URL.createObjectURL(blob);

	if(oldSrc) URL.revokeObjectURL(oldSrc);
}


/***/ }),

/***/ "./node_modules/style-loader/lib/urls.js":
/*!***********************************************!*\
  !*** ./node_modules/style-loader/lib/urls.js ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


/**
 * When source maps are enabled, `style-loader` uses a link element with a data-uri to
 * embed the css on the page. This breaks all relative urls because now they are relative to a
 * bundle instead of the current page.
 *
 * One solution is to only use full urls, but that may be impossible.
 *
 * Instead, this function "fixes" the relative urls to be absolute according to the current page location.
 *
 * A rudimentary test suite is located at `test/fixUrls.js` and can be run via the `npm test` command.
 *
 */

module.exports = function (css) {
	// get current location
	var location = typeof window !== "undefined" && window.location;

	if (!location) {
		throw new Error("fixUrls requires window.location");
	}

	// blank or null?
	if (!css || typeof css !== "string") {
		return css;
	}

	var baseUrl = location.protocol + "//" + location.host;
	var currentDir = baseUrl + location.pathname.replace(/\/[^\/]*$/, "/");

	// convert each url(...)
	/*
 This regular expression is just a way to recursively match brackets within
 a string.
 	 /url\s*\(  = Match on the word "url" with any whitespace after it and then a parens
    (  = Start a capturing group
      (?:  = Start a non-capturing group
          [^)(]  = Match anything that isn't a parentheses
          |  = OR
          \(  = Match a start parentheses
              (?:  = Start another non-capturing groups
                  [^)(]+  = Match anything that isn't a parentheses
                  |  = OR
                  \(  = Match a start parentheses
                      [^)(]*  = Match anything that isn't a parentheses
                  \)  = Match a end parentheses
              )  = End Group
              *\) = Match anything and then a close parens
          )  = Close non-capturing group
          *  = Match anything
       )  = Close capturing group
  \)  = Match a close parens
 	 /gi  = Get all matches, not the first.  Be case insensitive.
  */
	var fixedCss = css.replace(/url\s*\(((?:[^)(]|\((?:[^)(]+|\([^)(]*\))*\))*)\)/gi, function (fullMatch, origUrl) {
		// strip quotes (if they exist)
		var unquotedOrigUrl = origUrl.trim().replace(/^"(.*)"$/, function (o, $1) {
			return $1;
		}).replace(/^'(.*)'$/, function (o, $1) {
			return $1;
		});

		// already a full url? no change
		if (/^(#|data:|http:\/\/|https:\/\/|file:\/\/\/|\s*$)/i.test(unquotedOrigUrl)) {
			return fullMatch;
		}

		// convert the url to a full url
		var newUrl;

		if (unquotedOrigUrl.indexOf("//") === 0) {
			//TODO: should we add protocol?
			newUrl = unquotedOrigUrl;
		} else if (unquotedOrigUrl.indexOf("/") === 0) {
			// path should be relative to the base url
			newUrl = baseUrl + unquotedOrigUrl; // already starts with '/'
		} else {
			// path should be relative to current directory
			newUrl = currentDir + unquotedOrigUrl.replace(/^\.\//, ""); // Strip leading './'
		}

		// send back the fixed url(...)
		return "url(" + JSON.stringify(newUrl) + ")";
	});

	// send back the fixed css
	return fixedCss;
};

/***/ }),

/***/ "./src/Installer.jsx":
/*!***************************!*\
  !*** ./src/Installer.jsx ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

__webpack_require__(/*! @babel/polyfill/noConflict */ "./node_modules/@babel/polyfill/noConflict.js");

__webpack_require__(/*! semantic-ui-css/semantic.min.css */ "./node_modules/semantic-ui-css/semantic.min.css");

__webpack_require__(/*! ./css/installer.css */ "./src/css/installer.css");

var _semanticUiReact = __webpack_require__(/*! semantic-ui-react */ "./node_modules/semantic-ui-react/dist/es/index.js");

var _react = __webpack_require__(/*! react */ "./node_modules/react/index.js");

var _react2 = _interopRequireDefault(_react);

var _AppStoreSelector = __webpack_require__(/*! ./components/AppStoreSelector */ "./src/components/AppStoreSelector.jsx");

var _AppStoreSelector2 = _interopRequireDefault(_AppStoreSelector);

var _AppsList = __webpack_require__(/*! ./components/AppsList */ "./src/components/AppsList.jsx");

var _AppsList2 = _interopRequireDefault(_AppsList);

var _ErrorList = __webpack_require__(/*! ./components/ErrorList */ "./src/components/ErrorList.jsx");

var _ErrorList2 = _interopRequireDefault(_ErrorList);

var _reactRedux = __webpack_require__(/*! react-redux */ "./node_modules/react-redux/es/index.js");

var _reactDom = __webpack_require__(/*! react-dom */ "./node_modules/react-dom/index.js");

var _reactDom2 = _interopRequireDefault(_reactDom);

var _store = __webpack_require__(/*! ./store */ "./src/store/index.js");

var _store2 = _interopRequireDefault(_store);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var AppInstaller = function (_Component) {
    _inherits(AppInstaller, _Component);

    function AppInstaller(props) {
        _classCallCheck(this, AppInstaller);

        return _possibleConstructorReturn(this, (AppInstaller.__proto__ || Object.getPrototypeOf(AppInstaller)).call(this, props));
    }

    _createClass(AppInstaller, [{
        key: 'render',
        value: function render() {
            return _react2.default.createElement(
                _reactRedux.Provider,
                { store: _store2.default },
                _react2.default.createElement(
                    'div',
                    null,
                    _react2.default.createElement(
                        _semanticUiReact.Container,
                        { id: 'main-container' },
                        _react2.default.createElement(
                            _semanticUiReact.Grid,
                            { centered: true },
                            _react2.default.createElement(
                                _semanticUiReact.Grid.Row,
                                { centered: true },
                                _react2.default.createElement(
                                    _semanticUiReact.Grid.Column,
                                    { width: 15 },
                                    _react2.default.createElement(_ErrorList2.default, null)
                                )
                            ),
                            _react2.default.createElement(
                                _semanticUiReact.Grid.Row,
                                { centered: true },
                                _react2.default.createElement(
                                    _semanticUiReact.Grid.Column,
                                    { width: 15 },
                                    _react2.default.createElement(
                                        _semanticUiReact.Message,
                                        { warning: true },
                                        _react2.default.createElement(
                                            _semanticUiReact.Message.Header,
                                            null,
                                            "Warning!"
                                        ),
                                        _react2.default.createElement(
                                            'p',
                                            null,
                                            "Please note that the web server will be restarted after installing or uninstalling any application."
                                        )
                                    )
                                )
                            ),
                            _react2.default.createElement(
                                _semanticUiReact.Grid.Row,
                                { centered: true },
                                _react2.default.createElement(
                                    _semanticUiReact.Grid.Column,
                                    { width: 15 },
                                    _react2.default.createElement(_AppStoreSelector2.default, null)
                                )
                            ),
                            _react2.default.createElement(
                                _semanticUiReact.Grid.Row,
                                null,
                                _react2.default.createElement(
                                    _semanticUiReact.Grid.Column,
                                    { width: 16 },
                                    _react2.default.createElement(_AppsList2.default, null)
                                )
                            )
                        )
                    )
                )
            );
        }
    }]);

    return AppInstaller;
}(_react.Component);

var elem = document.getElementById("installer-app");
if (!elem) {
    elem = document.createElement('div', { "id": "installer-app" });
    document.body.appendChild(elem);
}
_reactDom2.default.render(_react2.default.createElement(AppInstaller, null), elem);
if (false) {}

/***/ }),

/***/ "./src/actions/appStores.js":
/*!**********************************!*\
  !*** ./src/actions/appStores.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.setAppStores = setAppStores;
exports.selectAppStore = selectAppStore;
exports.appStoresLoading = appStoresLoading;

var _constants = __webpack_require__(/*! ./constants */ "./src/actions/constants.js");

function setAppStores(stores) {
    return {
        type: _constants.SET_APP_STORES,
        payload: stores
    };
}
function selectAppStore(StoreID) {
    return {
        type: _constants.SELECT_APP_STORE,
        payload: StoreID
    };
}
function appStoresLoading(loading) {
    return {
        type: _constants.APP_STORES_LOADING,
        payload: loading
    };
}

/***/ }),

/***/ "./src/actions/apps.js":
/*!*****************************!*\
  !*** ./src/actions/apps.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.addApps = addApps;
exports.updateInstalledApp = updateInstalledApp;
exports.actionInProgress = actionInProgress;
exports.deleteInstalledApps = deleteInstalledApps;
exports.setInstalledApps = setInstalledApps;
exports.installedAppsLoading = installedAppsLoading;
exports.installedAppsTotalCount = installedAppsTotalCount;

var _constants = __webpack_require__(/*! ./constants */ "./src/actions/constants.js");

function addApps(apps) {
    return {
        type: _constants.ADD_INSTALLED_APPS,
        payload: apps
    };
}
function updateInstalledApp(app) {
    return {
        type: _constants.UPDATE_INSTALLED_APP,
        payload: app
    };
}
function actionInProgress(loading) {
    return {
        type: _constants.SET_ACTION_IN_PROGRESS,
        payload: loading
    };
}
function deleteInstalledApps(appIDs) {
    return {
        type: _constants.DELETE_INSTALLED_APPS,
        payload: appIDs
    };
}
function setInstalledApps(apps) {
    return {
        type: _constants.SET_INSTALLED_APPS,
        payload: apps
    };
}
function installedAppsLoading(loading) {
    return {
        type: _constants.INSTALLED_APPS_LOADING,
        payload: loading
    };
}
function installedAppsTotalCount(count) {
    return {
        type: _constants.SET_APPS_TOTAL_COUNT,
        payload: count
    };
}

/***/ }),

/***/ "./src/actions/constants.js":
/*!**********************************!*\
  !*** ./src/actions/constants.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
  value: true
});
var SET_INSTALLED_APPS = exports.SET_INSTALLED_APPS = "SET_INSTALLED_APPS";
var SET_STORE_APPS = exports.SET_STORE_APPS = "SET_STORE_APPS";
var UPDATE_INSTALLED_APP = exports.UPDATE_INSTALLED_APP = "UPDATE_INSTALLED_APP";
var SET_SORT_BY = exports.SET_SORT_BY = "SET_SORT_BY";
var SET_SEARCH_TEXT = exports.SET_SEARCH_TEXT = "SET_SEARCH_TEXT";
var SET_ACTIVE_PAGE = exports.SET_ACTIVE_PAGE = "SET_ACTIVE_PAGE";
var SET_ITEMS_PER_PAGE = exports.SET_ITEMS_PER_PAGE = "SET_ITEMS_PER_PAGE";
var SET_SORT_TYPE = exports.SET_SORT_TYPE = "SET_SORT_TYPE";
var UPDATE_STORE_APP = exports.UPDATE_STORE_APP = "UPDATE_STORE_APP";
var SET_ERRORS = exports.SET_ERRORS = "SET_ERRORS";
var ADD_ERRORS = exports.ADD_ERRORS = "ADD_ERRORS";
var DELETE_ERROR = exports.DELETE_ERROR = "DELETE_ERROR";
var SET_ACTION_IN_PROGRESS = exports.SET_ACTION_IN_PROGRESS = "SET_ACTION_IN_PROGRESS";
var SET_APP_STORES = exports.SET_APP_STORES = "SET_APP_STORES";
var SELECT_APP_STORE = exports.SELECT_APP_STORE = "SELECT_APP_STORE";
var APP_STORES_LOADING = exports.APP_STORES_LOADING = "APP_STORES_LOADING";
var ADD_INSTALLED_APPS = exports.ADD_INSTALLED_APPS = "ADD_INSTALLED_APPS";
var ADD_STORE_APPS = exports.ADD_STORE_APPS = "ADD_STORE_APPS";
var DELETE_INSTALLED_APPS = exports.DELETE_INSTALLED_APPS = "DELETE_INSTALLED_APPS";
var DELETE_STORE_APPS = exports.DELETE_STORE_APPS = "DELETE_STORE_APPS";
var INSTALLED_APPS_LOADING = exports.INSTALLED_APPS_LOADING = "INSTALLED_APPS_LOADING";
var STORE_APPS_LOADING = exports.STORE_APPS_LOADING = "STORE_APPS_LOADING";
var SET_APPS_TOTAL_COUNT = exports.SET_APPS_TOTAL_COUNT = "SET_APPS_TOTAL_COUNT";
var SET_STORE_TOTAL_COUNT = exports.SET_STORE_TOTAL_COUNT = "SET_STORE_TOTAL_COUNT";
var SET_URLS = exports.SET_URLS = "SET_URLS";
var SET_USERNAME = exports.SET_USERNAME = "SET_USERNAME";
var SET_TOKEN = exports.SET_TOKEN = "SET_TOKEN";

/***/ }),

/***/ "./src/actions/errors.js":
/*!*******************************!*\
  !*** ./src/actions/errors.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.setErrors = setErrors;
exports.deleteError = deleteError;
exports.addError = addError;

var _constants = __webpack_require__(/*! ./constants */ "./src/actions/constants.js");

function setErrors(errors) {
    return {
        type: _constants.SET_ERRORS,
        payload: errors
    };
}
function deleteError(error) {
    return {
        type: _constants.DELETE_ERROR,
        payload: error
    };
}
function addError(errors) {
    return {
        type: _constants.ADD_ERRORS,
        payload: errors
    };
}

/***/ }),

/***/ "./src/actions/filter.js":
/*!*******************************!*\
  !*** ./src/actions/filter.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.setSortBy = setSortBy;
exports.setSearchText = setSearchText;
exports.setActivePage = setActivePage;
exports.setItemsPerPage = setItemsPerPage;
exports.setSortType = setSortType;

var _constants = __webpack_require__(/*! ./constants */ "./src/actions/constants.js");

function setSortBy(attributeName) {
    return {
        type: _constants.SET_SORT_BY,
        payload: attributeName
    };
}
function setSearchText(txt) {
    return {
        type: _constants.SET_SEARCH_TEXT,
        payload: txt
    };
}
function setActivePage(pageNumber) {
    return {
        type: _constants.SET_ACTIVE_PAGE,
        payload: pageNumber
    };
}
function setItemsPerPage(count) {
    return {
        type: _constants.SET_ITEMS_PER_PAGE,
        payload: count
    };
}
function setSortType(type) {
    return {
        type: _constants.SET_SORT_TYPE,
        payload: type
    };
}

/***/ }),

/***/ "./src/actions/storeApps.js":
/*!**********************************!*\
  !*** ./src/actions/storeApps.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.addStoreApps = addStoreApps;
exports.updateStoreApp = updateStoreApp;
exports.deleteStoreApps = deleteStoreApps;
exports.setStoreApps = setStoreApps;
exports.storeAppsLoading = storeAppsLoading;
exports.storeAppsTotalCount = storeAppsTotalCount;

var _constants = __webpack_require__(/*! ./constants */ "./src/actions/constants.js");

function addStoreApps(apps) {
    return {
        type: _constants.ADD_STORE_APPS,
        payload: apps
    };
}
function updateStoreApp(app) {
    return {
        type: _constants.UPDATE_STORE_APP,
        payload: app
    };
}
function deleteStoreApps(appIDs) {
    return {
        type: _constants.DELETE_STORE_APPS,
        payload: appIDs
    };
}
function setStoreApps(apps) {
    return {
        type: _constants.SET_STORE_APPS,
        payload: apps
    };
}
function storeAppsLoading(loading) {
    return {
        type: _constants.STORE_APPS_LOADING,
        payload: loading
    };
}
function storeAppsTotalCount(count) {
    return {
        type: _constants.SET_STORE_TOTAL_COUNT,
        payload: count
    };
}

/***/ }),

/***/ "./src/api/apps.jsx":
/*!**************************!*\
  !*** ./src/api/apps.jsx ***!
  \**************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});
exports.getStoresApps = getStoresApps;
exports.getInstalledApps = getInstalledApps;
exports.mergeApps = mergeApps;

var _utils = __webpack_require__(/*! ./utils */ "./src/api/utils.jsx");

var requests = new _utils.ApiRequests();
function getStoresApps(store) {
	return requests.doExternalGet(store.url + 'app/?server_type__name=' + store.server_type + '&cartoview_version=' + window.appInstallerProps.cartoview_version);
}
function getInstalledApps() {
	var urls = window.appInstallerProps.urls;

	return requests.doGet(urls.appsURL);
}
function getAppByName(installedApps, name) {
	var app = installedApps.find(function (app) {
		return app.name === name;
	});
	var index = installedApps.findIndex(function (app) {
		return app.name === name;
	});
	return [app, index];
}
function mergeApps(storeApps, installedApps) {
	for (var index = 0; index < storeApps.length; index++) {
		var app = storeApps[index];
		var installedApp = getAppByName(installedApps, app.name);
		if (installedApp[0]) {
			app.installedApp = installedApp[0];
		} else {
			app.installedApp = undefined;
		}
	}
	return storeApps;
}

/***/ }),

/***/ "./src/api/compare.js":
/*!****************************!*\
  !*** ./src/api/compare.js ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.versionCompare = versionCompare;
/**
 * Compares two software version numbers (e.g. "1.7.1" or "1.2b").
 *
 * This function was born in http://stackoverflow.com/a/6832721.
 *
 * @param {string} v1 The first version to be compared.
 * @param {string} v2 The second version to be compared.
 * @param {object} [options] Optional flags that affect comparison behavior:
 * lexicographical: (true/[false]) compares each part of the version strings lexicographically instead of naturally; 
 *                  this allows suffixes such as "b" or "dev" but will cause "1.10" to be considered smaller than "1.2".
 * zeroExtend: ([true]/false) changes the result if one version string has less parts than the other. In
 *             this case the shorter string will be padded with "zero" parts instead of being considered smaller.
 *
 * @returns {number|NaN}
 * - 0 if the versions are equal
 * - a negative integer iff v1 < v2
 * - a positive integer iff v1 > v2
 * - NaN if either version string is in the wrong format
 */
function versionCompare(v1, v2, options) {
    var lexicographical = options && options.lexicographical || false,
        zeroExtend = options && options.zeroExtend || true,
        v1parts = (v1 || "0").split('.'),
        v2parts = (v2 || "0").split('.');

    function isValidPart(x) {
        return (lexicographical ? /^\d+[A-Za-zαß]*$/ : /^\d+[A-Za-zαß]?$/).test(x);
    }
    if (!v1parts.every(isValidPart) || !v2parts.every(isValidPart)) {
        return NaN;
    }
    if (zeroExtend) {
        while (v1parts.length < v2parts.length) {
            v1parts.push("0");
        }while (v2parts.length < v1parts.length) {
            v2parts.push("0");
        }
    }
    if (!lexicographical) {
        v1parts = v1parts.map(function (x) {
            var match = /[A-Za-zαß]/.exec(x);
            return Number(match ? x.replace(match[0], "." + x.charCodeAt(match.index)) : x);
        });
        v2parts = v2parts.map(function (x) {
            var match = /[A-Za-zαß]/.exec(x);
            return Number(match ? x.replace(match[0], "." + x.charCodeAt(match.index)) : x);
        });
    }
    for (var i = 0; i < v1parts.length; ++i) {
        if (v2parts.length == i) {
            return 1;
        }
        if (v1parts[i] == v2parts[i]) {
            continue;
        } else if (v1parts[i] > v2parts[i]) {
            return 1;
        } else {
            return -1;
        }
    }
    if (v1parts.length != v2parts.length) {
        return -1;
    }
    return 0;
}

/***/ }),

/***/ "./src/api/stores.jsx":
/*!****************************!*\
  !*** ./src/api/stores.jsx ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});
exports.getStores = getStores;

var _utils = __webpack_require__(/*! ./utils */ "./src/api/utils.jsx");

var requests = new _utils.ApiRequests();
function getStores() {
	var urls = window.appInstallerProps.urls;

	return requests.doGet(urls.storesURL);
}

/***/ }),

/***/ "./src/api/utils.jsx":
/*!***************************!*\
  !*** ./src/api/utils.jsx ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

exports.getCRSFToken = getCRSFToken;

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function updateProgress(evt) {
	if (evt.lengthComputable) {
		var percentComplete = evt.loaded / evt.total * 100;
	}
}

function transferComplete(evt) {
	console.log("The transfer is complete.");
}
function getCRSFToken() {
	var csrfToken = void 0,
	    csrfMatch = document.cookie.match(/csrftoken=(\w+)/);
	if (csrfMatch && csrfMatch.length > 0) {
		csrfToken = csrfMatch[1];
	}
	return csrfToken;
}
function transferFailed(evt) {
	console.error("An error occurred while transferring the file.");
}

var ApiRequests = exports.ApiRequests = function () {
	function ApiRequests() {
		_classCallCheck(this, ApiRequests);
	}

	_createClass(ApiRequests, [{
		key: "getHeaders",
		value: function getHeaders() {
			return [];
		}
	}, {
		key: "doPost",
		value: function doPost(url, data) {
			var extraHeaders = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};
			var options = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : {};

			var headers = _extends({}, this.getHeaders(), extraHeaders);
			return fetch(url, _extends({
				method: 'POST',
				redirect: 'follow',
				credentials: options['mode'] && options['mode'] === 'cors' ? 'omit' : 'include'
			}, options, {
				headers: headers,
				body: data
			})).then(function (response) {
				return response.json();
			});
		}
	}, {
		key: "doDelete",
		value: function doDelete(url) {
			var extraHeaders = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
			var options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};

			var headers = _extends({}, this.getHeaders(), extraHeaders);
			return fetch(url, _extends({
				method: 'DELETE',
				redirect: 'follow',
				credentials: options['mode'] && options['mode'] === 'cors' ? 'omit' : 'include'
			}, options, {
				headers: headers
			})).then(function (response) {
				return response.text();
			});
		}
	}, {
		key: "doExternalGet",
		value: function doExternalGet(url) {
			var extraHeaders = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
			var options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};

			var headers = _extends({}, this.getHeaders(), extraHeaders);
			return fetch(url, _extends({
				method: 'GET',
				mode: 'cors',
				redirect: 'follow'
			}, options, {
				headers: headers
			})).then(function (response) {
				return response.json();
			});
		}
	}, {
		key: "doGet",
		value: function doGet(url) {
			var extraHeaders = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};
			var options = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : {};

			var headers = _extends({}, this.getHeaders(), extraHeaders);
			var mode = options['mode'];
			return fetch(url, _extends({
				method: 'GET',
				redirect: 'follow',
				credentials: mode && mode === 'cors' ? 'omit' : 'include'
			}, options, {
				headers: headers
			})).then(function (response) {
				return response.json();
			});
		}
	}, {
		key: "uploadWithProgress",
		value: function uploadWithProgress(url, data, resultFunc) {
			var progressFunc = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : updateProgress;
			var loadFunc = arguments.length > 4 && arguments[4] !== undefined ? arguments[4] : transferComplete;
			var errorFunc = arguments.length > 5 && arguments[5] !== undefined ? arguments[5] : transferFailed;


			var xhr = new XMLHttpRequest();
			xhr.upload.addEventListener("progress", function (evt) {
				progressFunc(evt);
			}, false);
			xhr.addEventListener("load", function (evt) {
				loadFunc(xhr);
			});
			xhr.addEventListener("error", function () {
				errorFunc(xhr);
			});
			xhr.onreadystatechange = function () {
				if (xhr.readyState == XMLHttpRequest.DONE) {
					resultFunc(xhr.responseText);
				}
			};
			xhr.open('POST', url, true);
			xhr.setRequestHeader("Cache-Control", "no-cache");
			xhr.setRequestHeader('Authorization', "ApiKey " + this.username + ":" + this.token);
			xhr.send(data);
		}
	}]);

	return ApiRequests;
}();

/***/ }),

/***/ "./src/components/AppStoreSelector.jsx":
/*!*********************************************!*\
  !*** ./src/components/AppStoreSelector.jsx ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _semanticUiReact = __webpack_require__(/*! semantic-ui-react */ "./node_modules/semantic-ui-react/dist/es/index.js");

var _appStores = __webpack_require__(/*! ../actions/appStores */ "./src/actions/appStores.js");

var _propTypes = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");

var _propTypes2 = _interopRequireDefault(_propTypes);

var _react = __webpack_require__(/*! react */ "./node_modules/react/index.js");

var _react2 = _interopRequireDefault(_react);

var _reactRedux = __webpack_require__(/*! react-redux */ "./node_modules/react-redux/es/index.js");

var _stores = __webpack_require__(/*! ../api/stores */ "./src/api/stores.jsx");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var AppStoreSelector = function (_React$Component) {
	_inherits(AppStoreSelector, _React$Component);

	function AppStoreSelector() {
		var _ref;

		var _temp, _this, _ret;

		_classCallCheck(this, AppStoreSelector);

		for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
			args[_key] = arguments[_key];
		}

		return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = AppStoreSelector.__proto__ || Object.getPrototypeOf(AppStoreSelector)).call.apply(_ref, [this].concat(args))), _this), _this.onChange = function (event, _ref2) {
			var value = _ref2.value;
			var selectStore = _this.props.selectStore;

			selectStore(value);
		}, _this.getDefaultStore = function () {
			var _this$props = _this.props,
			    appStores = _this$props.appStores,
			    selectStore = _this$props.selectStore;

			var defaultStoreID = undefined;
			for (var index = 0; index < appStores.stores.length; index++) {
				var store = appStores.stores[index];
				if (store.is_default) {
					defaultStoreID = store.id;
				}
			}
			selectStore(defaultStoreID);
			return defaultStoreID;
		}, _temp), _possibleConstructorReturn(_this, _ret);
	}

	_createClass(AppStoreSelector, [{
		key: 'componentDidMount',
		value: function componentDidMount() {
			var _this2 = this;

			var _props = this.props,
			    setStores = _props.setStores,
			    setStoresLoading = _props.setStoresLoading;

			(0, _stores.getStores)().then(function (data) {
				setStores(data.results);
				_this2.getDefaultStore();
				setStoresLoading(false);
			});
		}
	}, {
		key: 'getStoresOptions',
		value: function getStoresOptions() {
			var appStores = this.props.appStores;

			var storesOptions = appStores.stores.map(function (store) {
				return {
					text: store.name + ' (' + store.server_type + ')',
					value: store.id
				};
			});
			return storesOptions;
		}
	}, {
		key: 'render',
		value: function render() {
			var appStores = this.props.appStores;

			return _react2.default.createElement(
				'div',
				null,
				appStores.loading ? _react2.default.createElement(
					_semanticUiReact.Dimmer,
					{ active: true, inverted: true },
					_react2.default.createElement(_semanticUiReact.Loader, { inverted: true, content: 'Loading' })
				) : _react2.default.createElement(_semanticUiReact.Dropdown, { onChange: this.onChange,
					placeholder: 'Select an App Store',
					value: appStores.selectedStoreID,
					fluid: true,
					selection: true,
					options: this.getStoresOptions() })
			);
		}
	}]);

	return AppStoreSelector;
}(_react2.default.Component);

AppStoreSelector.propTypes = {
	setStores: _propTypes2.default.func.isRequired,
	setStoresLoading: _propTypes2.default.func.isRequired,
	selectStore: _propTypes2.default.func.isRequired,
	appStores: _propTypes2.default.object.isRequired
};
var mapStateToProps = function mapStateToProps(state) {
	return {
		appStores: state.appStores
	};
};
var mapDispatchToProps = function mapDispatchToProps(dispatch) {
	return {
		setStores: function setStores(stores) {
			return dispatch((0, _appStores.setAppStores)(stores));
		},
		setStoresLoading: function setStoresLoading(loading) {
			return dispatch((0, _appStores.appStoresLoading)(loading));
		},
		selectStore: function selectStore(selectedStoreID) {
			return dispatch((0, _appStores.selectAppStore)(selectedStoreID));
		}
	};
};

exports.default = (0, _reactRedux.connect)(mapStateToProps, mapDispatchToProps)(AppStoreSelector);

/***/ }),

/***/ "./src/components/AppsList.jsx":
/*!*************************************!*\
  !*** ./src/components/AppsList.jsx ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _lodash = __webpack_require__(/*! lodash */ "./node_modules/lodash/lodash.js");

var _ = _interopRequireWildcard(_lodash);

var _apps = __webpack_require__(/*! ../actions/apps */ "./src/actions/apps.js");

var appsActions = _interopRequireWildcard(_apps);

var _errors = __webpack_require__(/*! ../actions/errors */ "./src/actions/errors.js");

var errorActions = _interopRequireWildcard(_errors);

var _storeApps = __webpack_require__(/*! ../actions/storeApps */ "./src/actions/storeApps.js");

var storeActions = _interopRequireWildcard(_storeApps);

var _utils = __webpack_require__(/*! ../api/utils */ "./src/api/utils.jsx");

var _semanticUiReact = __webpack_require__(/*! semantic-ui-react */ "./node_modules/semantic-ui-react/dist/es/index.js");

var _apps2 = __webpack_require__(/*! ../api/apps */ "./src/api/apps.jsx");

var _Filter = __webpack_require__(/*! ./Filter */ "./src/components/Filter.jsx");

var _Filter2 = _interopRequireDefault(_Filter);

var _Pagination = __webpack_require__(/*! ./Pagination */ "./src/components/Pagination.jsx");

var _Pagination2 = _interopRequireDefault(_Pagination);

var _CardsLoading = __webpack_require__(/*! ./CardsLoading */ "./src/components/CardsLoading.jsx");

var _CardsLoading2 = _interopRequireDefault(_CardsLoading);

var _propTypes = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");

var _propTypes2 = _interopRequireDefault(_propTypes);

var _react = __webpack_require__(/*! react */ "./node_modules/react/index.js");

var _react2 = _interopRequireDefault(_react);

var _reactRedux = __webpack_require__(/*! react-redux */ "./node_modules/react-redux/es/index.js");

var _compare = __webpack_require__(/*! ../api/compare */ "./src/api/compare.js");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var requests = new _utils.ApiRequests();
var colorsMapping = {
	"Alpha": "red",
	"Beta": "yellow",
	"Stable": "green"
};

var AppsList = function (_React$Component) {
	_inherits(AppsList, _React$Component);

	function AppsList() {
		var _ref;

		var _temp, _this, _ret;

		_classCallCheck(this, AppsList);

		for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
			args[_key] = arguments[_key];
		}

		return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = AppsList.__proto__ || Object.getPrototypeOf(AppsList)).call.apply(_ref, [this].concat(args))), _this), _this.sortApps = function () {
			var _this$props = _this.props,
			    apps = _this$props.apps,
			    appFilters = _this$props.appFilters;


			return _.orderBy(apps.storeApps, [appFilters.sortBy], [appFilters.sortType]);
		}, _this.getTotalPages = function () {
			var _this$props2 = _this.props,
			    apps = _this$props2.apps,
			    appFilters = _this$props2.appFilters;

			return Math.ceil(apps.storeCount / appFilters.itemsPerPage);
		}, _this.searchApps = function (apps) {
			var appFilters = _this.props.appFilters;

			if (appFilters.searchText != "") {
				return _.filter(apps, function (app) {
					var title = app.title,
					    description = app.description;

					var searchText = appFilters.searchText.toLowerCase();
					title = title.toLowerCase();
					description = description.toLowerCase();
					return title.includes(searchText) || description.includes(searchText);
				});
			}
			return apps;
		}, _this.getApps = function () {
			var appFilters = _this.props.appFilters;

			var apps = _this.sortApps();
			apps = _this.searchApps(apps);
			if (appFilters.searchText === "") {
				apps = _this.paginate(apps);
			}
			return apps;
		}, _this.paginate = function (apps) {
			var appFilters = _this.props.appFilters;

			var startIndex = (appFilters.activePage - 1) * appFilters.itemsPerPage;
			var endIndex = appFilters.activePage * appFilters.itemsPerPage;
			return apps.slice(startIndex, endIndex);
		}, _this.getInstalledByName = function (name) {
			var apps = _this.props.apps;

			return apps.installed.find(function (app) {
				return app.name == name;
			});
		}, _this.installApp = function (app) {
			return function () {
				var _this$props3 = _this.props,
				    appStores = _this$props3.appStores,
				    setInProgress = _this$props3.setInProgress,
				    updateStoreApp = _this$props3.updateStoreApp,
				    addInstalledApps = _this$props3.addInstalledApps,
				    addError = _this$props3.addError;

				app.installing = true;
				setInProgress(true);
				updateStoreApp(app);
				var data = JSON.stringify({
					'app_name': app.name,
					"store_id": appStores.selectedStoreID,
					"app_version": app.latest_version.version
				});
				requests.doPost(window.appInstallerProps.urls.install, data, {
					"Content-Type": "application/json",
					"X-CSRFToken": (0, _utils.getCRSFToken)()
				}).then(function (data) {
					if (!Object.keys(data).includes("details")) {
						addInstalledApps([data]);
						updateStoreApp(_extends({}, app, { compatible: true, installing: false }));
						setInProgress(false);
					} else {
						addError([data.details]);
					}
				}).catch(function (error) {
					app.installing = false;
					setInProgress(false);
					updateStoreApp(app);
					addError([error.message]);
				});
			};
		}, _this.uninstallApp = function (app) {
			return function () {
				var _this$props4 = _this.props,
				    deleteInstalledApps = _this$props4.deleteInstalledApps,
				    setInProgress = _this$props4.setInProgress,
				    updateStoreApp = _this$props4.updateStoreApp,
				    addError = _this$props4.addError;

				var installedApp = _this.getInstalledByName(app.name);
				app.uninstalling = true;
				setInProgress(true);
				updateStoreApp(app);
				requests.doDelete(window.appInstallerProps.urls.appsURL + (installedApp.id + '/uninstall/'), {
					"Content-Type": "application/json",
					"X-CSRFToken": (0, _utils.getCRSFToken)()
				}).then(function (data) {
					if (!Object.keys(data).includes("details")) {
						deleteInstalledApps([data.id]);
						updateStoreApp(_extends({}, app, { uninstalling: false }));
						setInProgress(false);
					} else {
						addError([data.details]);
					}
				}).catch(function (error) {
					app.uninstalling = false;
					setInProgress(false);
					updateStoreApp(app);
					addError([error.message]);
				});
			};
		}, _temp), _possibleConstructorReturn(_this, _ret);
	}

	_createClass(AppsList, [{
		key: 'componentDidUpdate',
		value: function componentDidUpdate(prevProps) {
			var _this2 = this;

			var appStores = prevProps.appStores;

			if (this.props.appStores.selectedStoreID && appStores.selectedStoreID != this.props.appStores.selectedStoreID) {
				var _props = this.props,
				    setStoreAppsList = _props.setStoreAppsList,
				    setStoreCount = _props.setStoreCount,
				    setStoreLoading = _props.setStoreLoading;

				var store = this.props.appStores.stores.find(function (store) {
					return store.id === _this2.props.appStores.selectedStoreID;
				});
				(0, _apps2.getStoresApps)(store).then(function (data) {
					var storeApps = data.objects.map(function (storeApp) {
						storeApp.compatible = false;
						storeApp.installing = false;
						storeApp.uninstalling = false;
						var cartoview_versions = storeApp.latest_version.cartoview_version;
						for (var index = 0; index < cartoview_versions.length; index++) {
							var cartoview_version = cartoview_versions[index];
							if ((0, _compare.versionCompare)(cartoview_version.version, window.appInstallerProps.cartoview_version, { 'lexicographical': true }) == 0) {
								storeApp.compatible = true;
								break;
							}
						}
						return storeApp;
					});
					setStoreAppsList(storeApps);
					setStoreCount(data.meta.total_count);
					setStoreLoading(false);
				});
				var _props2 = this.props,
				    setInstalled = _props2.setInstalled,
				    setInstalledLoading = _props2.setInstalledLoading,
				    setIntalledCount = _props2.setIntalledCount;

				(0, _apps2.getInstalledApps)().then(function (data) {
					setInstalled(data.results);
					setIntalledCount(data.count);
					setInstalledLoading(false);
				});
			}
		}
	}, {
		key: 'render',
		value: function render() {
			var _this3 = this;

			var _props3 = this.props,
			    apps = _props3.apps,
			    appStores = _props3.appStores,
			    appFilters = _props3.appFilters;

			var totalPages = this.getTotalPages();
			return _react2.default.createElement(
				'div',
				null,
				apps.storeAppsLoading || apps.installedAppsLoading || appStores.loading ? _react2.default.createElement(_CardsLoading2.default, null) : _react2.default.createElement(
					_semanticUiReact.Grid,
					{ centered: true },
					_react2.default.createElement(
						_semanticUiReact.Grid.Row,
						{ centered: true },
						_react2.default.createElement(
							_semanticUiReact.Grid.Column,
							{ width: 15, textAlign: 'center' },
							_react2.default.createElement(_Filter2.default, null)
						)
					),
					_react2.default.createElement(
						_semanticUiReact.Grid.Row,
						null,
						_react2.default.createElement(
							_semanticUiReact.Grid.Column,
							null,
							_react2.default.createElement(
								_semanticUiReact.Card.Group,
								{ centered: true },
								this.getApps().map(function (app) {
									var installedApp = _this3.getInstalledByName(app.name);
									return _react2.default.createElement(
										_semanticUiReact.Card,
										{ centered: true, key: app.id },
										_react2.default.createElement(_semanticUiReact.Image, {
											wrapped: true,
											fluid: true,
											className: 'card-img ',
											label: { as: 'a', color: colorsMapping[app.status], content: app.status, ribbon: true },
											src: app.latest_version.logo }),
										_react2.default.createElement(
											_semanticUiReact.Card.Content,
											null,
											_react2.default.createElement(
												_semanticUiReact.Card.Header,
												null,
												app.title
											),
											_react2.default.createElement(
												_semanticUiReact.Card.Meta,
												null,
												_react2.default.createElement(
													'span',
													{ className: 'date' },
													app.author
												),
												_react2.default.createElement(_semanticUiReact.Popup, { size: 'small', header: "Description", trigger: _react2.default.createElement(_semanticUiReact.Icon, { circular: true, name: 'info' }), content: app.description })
											)
										),
										_react2.default.createElement(
											_semanticUiReact.Card.Content,
											{ extra: true },
											_react2.default.createElement(
												'div',
												{ className: 'ui three buttons' },
												installedApp && (0, _compare.versionCompare)(app.latest_version.version, installedApp.version, { 'lexicographical': true }) > 0 && _react2.default.createElement(
													_semanticUiReact.Button,
													{ onClick: _this3.installApp(app), loading: app.installing, disabled: !app.compatible || apps.inProgress, basic: true, color: app.compatible ? 'blue' : 'black' },
													app.compatible == true ? "Upgrade" : "Incompatible"
												),
												!installedApp && _react2.default.createElement(
													_semanticUiReact.Button,
													{ loading: app.installing, onClick: _this3.installApp(app), disabled: !app.compatible || apps.inProgress, basic: true, color: app.compatible == true ? 'green' : 'black' },
													app.compatible == true ? "Install" : "Incompatible"
												),
												installedApp && _react2.default.createElement(
													_semanticUiReact.Button,
													{ loading: app.uninstalling, onClick: _this3.uninstallApp(app), disabled: apps.inProgress, basic: true, color: 'red' },
													"Uninstall"
												),
												installedApp && _react2.default.createElement(
													_semanticUiReact.Button,
													{ disabled: apps.inProgress, basic: true, color: 'yellow' },
													"Suspend"
												)
											)
										),
										_react2.default.createElement(
											_semanticUiReact.Card.Content,
											{ extra: true },
											_react2.default.createElement(
												_semanticUiReact.Grid,
												{ centered: true },
												_react2.default.createElement(
													_semanticUiReact.Grid.Row,
													{ centered: true, columns: installedApp ? 2 : 1 },
													installedApp && _react2.default.createElement(
														_semanticUiReact.Grid.Column,
														{ textAlign: 'center' },
														_react2.default.createElement(
															_semanticUiReact.Label,
															{ size: 'tiny' },
															_react2.default.createElement(_semanticUiReact.Icon, { name: 'hdd' }),
															'Installed:v' + installedApp.version
														)
													),
													_react2.default.createElement(
														_semanticUiReact.Grid.Column,
														{ textAlign: 'center' },
														_react2.default.createElement(
															_semanticUiReact.Label,
															{ color: 'blue', size: 'tiny' },
															_react2.default.createElement(_semanticUiReact.Icon, { name: 'download' }),
															'Latest:v' + app.latest_version.version
														)
													)
												)
											)
										)
									);
								})
							)
						)
					),
					!apps.storeAppsLoading && !apps.installedAppsLoading && !appStores.loading && appFilters.searchText === "" && totalPages > 0 && _react2.default.createElement(
						_semanticUiReact.Grid.Row,
						{ centered: true },
						_react2.default.createElement(
							_semanticUiReact.Grid.Column,
							{ textAlign: 'center' },
							_react2.default.createElement(_Pagination2.default, null)
						)
					)
				)
			);
		}
	}]);

	return AppsList;
}(_react2.default.Component);

AppsList.propTypes = {
	setInstalled: _propTypes2.default.func.isRequired,
	setInstalledLoading: _propTypes2.default.func.isRequired,
	setIntalledCount: _propTypes2.default.func.isRequired,
	setStoreAppsList: _propTypes2.default.func.isRequired,
	setStoreLoading: _propTypes2.default.func.isRequired,
	setStoreCount: _propTypes2.default.func.isRequired,
	setInProgress: _propTypes2.default.func.isRequired,
	apps: _propTypes2.default.object.isRequired,
	appFilters: _propTypes2.default.object.isRequired,
	appStores: _propTypes2.default.object.isRequired,
	updateStoreApp: _propTypes2.default.func.isRequired,
	addInstalledApps: _propTypes2.default.func.isRequired,
	deleteInstalledApps: _propTypes2.default.func.isRequired,
	addError: _propTypes2.default.func.isRequired
};
var mapStateToProps = function mapStateToProps(state) {
	return {
		apps: state.apps,
		appStores: state.appStores,
		appFilters: state.appFilters
	};
};
var mapDispatchToProps = function mapDispatchToProps(dispatch) {
	return {
		setInstalled: function setInstalled(apps) {
			return dispatch(appsActions.setInstalledApps(apps));
		},
		setInstalledLoading: function setInstalledLoading(loading) {
			return dispatch(appsActions.installedAppsLoading(loading));
		},
		setIntalledCount: function setIntalledCount(count) {
			return dispatch(appsActions.installedAppsTotalCount(count));
		},
		setStoreAppsList: function setStoreAppsList(apps) {
			return dispatch(storeActions.setStoreApps(apps));
		},
		setStoreLoading: function setStoreLoading(loading) {
			return dispatch(storeActions.storeAppsLoading(loading));
		},
		setStoreCount: function setStoreCount(count) {
			return dispatch(storeActions.storeAppsTotalCount(count));
		},
		setInProgress: function setInProgress(loading) {
			return dispatch(appsActions.actionInProgress(loading));
		},
		updateStoreApp: function updateStoreApp(app) {
			return dispatch(storeActions.updateStoreApp(app));
		},
		addInstalledApps: function addInstalledApps(apps) {
			return dispatch(appsActions.addApps(apps));
		},
		addError: function addError(error) {
			return dispatch(errorActions.addError(error));
		},
		deleteInstalledApps: function deleteInstalledApps(apps) {
			return dispatch(appsActions.deleteInstalledApps(apps));
		}
	};
};

exports.default = (0, _reactRedux.connect)(mapStateToProps, mapDispatchToProps)(AppsList);

/***/ }),

/***/ "./src/components/CardsLoading.jsx":
/*!*****************************************!*\
  !*** ./src/components/CardsLoading.jsx ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _semanticUiReact = __webpack_require__(/*! semantic-ui-react */ "./node_modules/semantic-ui-react/dist/es/index.js");

var _propTypes = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");

var _propTypes2 = _interopRequireDefault(_propTypes);

var _react = __webpack_require__(/*! react */ "./node_modules/react/index.js");

var _react2 = _interopRequireDefault(_react);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var CardsLoading = function CardsLoading(props) {
	return _react2.default.createElement(
		_semanticUiReact.Card.Group,
		{ centered: true },
		Array(props.cardsCount).fill().map(function (_, i) {
			return _react2.default.createElement(
				_semanticUiReact.Card,
				{ centered: true, key: i },
				_react2.default.createElement(
					_semanticUiReact.Placeholder,
					null,
					_react2.default.createElement(_semanticUiReact.Placeholder.Image, { square: true })
				),
				_react2.default.createElement(
					_semanticUiReact.Card.Content,
					null,
					_react2.default.createElement(
						_semanticUiReact.Placeholder,
						null,
						_react2.default.createElement(
							_semanticUiReact.Placeholder.Header,
							null,
							_react2.default.createElement(_semanticUiReact.Placeholder.Line, { length: 'very short' }),
							_react2.default.createElement(_semanticUiReact.Placeholder.Line, { length: 'medium' })
						),
						_react2.default.createElement(
							_semanticUiReact.Placeholder.Paragraph,
							null,
							_react2.default.createElement(_semanticUiReact.Placeholder.Line, { length: 'short' })
						)
					)
				),
				_react2.default.createElement(
					_semanticUiReact.Card.Content,
					{ extra: true },
					_react2.default.createElement(
						'div',
						{ className: 'ui three buttons' },
						_react2.default.createElement(
							_semanticUiReact.Button,
							{ basic: true, disabled: true, color: 'green' },
							"Install"
						),
						_react2.default.createElement(
							_semanticUiReact.Button,
							{ basic: true, disabled: true, color: 'red' },
							"Uninstall"
						),
						_react2.default.createElement(
							_semanticUiReact.Button,
							{ basic: true, disabled: true, color: 'red' },
							"Suspend"
						)
					)
				)
			);
		})
	);
};
CardsLoading.propTypes = {
	cardsCount: _propTypes2.default.number.isRequired
};
CardsLoading.defaultProps = {
	cardsCount: 9
};
exports.default = CardsLoading;

/***/ }),

/***/ "./src/components/ErrorList.jsx":
/*!**************************************!*\
  !*** ./src/components/ErrorList.jsx ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _errors = __webpack_require__(/*! ../actions/errors */ "./src/actions/errors.js");

var errorActions = _interopRequireWildcard(_errors);

var _semanticUiReact = __webpack_require__(/*! semantic-ui-react */ "./node_modules/semantic-ui-react/dist/es/index.js");

var _propTypes = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");

var _propTypes2 = _interopRequireDefault(_propTypes);

var _react = __webpack_require__(/*! react */ "./node_modules/react/index.js");

var _react2 = _interopRequireDefault(_react);

var _reactRedux = __webpack_require__(/*! react-redux */ "./node_modules/react-redux/es/index.js");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var ErrorList = function (_React$Component) {
	_inherits(ErrorList, _React$Component);

	function ErrorList() {
		_classCallCheck(this, ErrorList);

		return _possibleConstructorReturn(this, (ErrorList.__proto__ || Object.getPrototypeOf(ErrorList)).apply(this, arguments));
	}

	_createClass(ErrorList, [{
		key: 'render',
		value: function render() {
			var _props = this.props,
			    appErrors = _props.appErrors,
			    deleteError = _props.deleteError;

			return _react2.default.createElement(
				'div',
				null,
				appErrors.errors.map(function (err, index) {
					return _react2.default.createElement(_semanticUiReact.Message, {
						onDismiss: function onDismiss() {
							return deleteError(err);
						},
						key: index,
						header: 'Error!',
						icon: _react2.default.createElement(_semanticUiReact.Icon, { name: 'info circle' }),
						content: err
					});
				})
			);
		}
	}]);

	return ErrorList;
}(_react2.default.Component);

ErrorList.propTypes = {
	appErrors: _propTypes2.default.object.isRequired,
	deleteError: _propTypes2.default.func.isRequired
};
var mapStateToProps = function mapStateToProps(state) {
	return {
		appErrors: state.appErrors
	};
};
var mapDispatchToProps = function mapDispatchToProps(dispatch) {
	return {
		deleteError: function deleteError(error) {
			return dispatch(errorActions.deleteError(error));
		}
	};
};

exports.default = (0, _reactRedux.connect)(mapStateToProps, mapDispatchToProps)(ErrorList);

/***/ }),

/***/ "./src/components/Filter.jsx":
/*!***********************************!*\
  !*** ./src/components/Filter.jsx ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _filter = __webpack_require__(/*! ../actions/filter */ "./src/actions/filter.js");

var filterActions = _interopRequireWildcard(_filter);

var _semanticUiReact = __webpack_require__(/*! semantic-ui-react */ "./node_modules/semantic-ui-react/dist/es/index.js");

var _propTypes = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");

var _propTypes2 = _interopRequireDefault(_propTypes);

var _react = __webpack_require__(/*! react */ "./node_modules/react/index.js");

var _react2 = _interopRequireDefault(_react);

var _reactRedux = __webpack_require__(/*! react-redux */ "./node_modules/react-redux/es/index.js");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var sortTypeOptions = [{ key: 't', text: 'Ascending', value: 'asc' }, { key: 'f', text: 'Descending', value: 'desc' }];
var sortByOptions = [{ key: 't', text: 'Title', value: 'title' }, { key: 'c', text: 'Compatibility', value: 'compatible' }, { key: 'd', text: 'Downloads', value: 'downloads' }];

var Filters = function (_React$Component) {
	_inherits(Filters, _React$Component);

	function Filters() {
		var _ref;

		var _temp, _this, _ret;

		_classCallCheck(this, Filters);

		for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
			args[_key] = arguments[_key];
		}

		return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = Filters.__proto__ || Object.getPrototypeOf(Filters)).call.apply(_ref, [this].concat(args))), _this), _this.handleChange = function (e, _ref2) {
			var value = _ref2.value;

			_this.props.setSortBy(value);
		}, _this.sortTypeChanged = function (e, _ref3) {
			var value = _ref3.value;

			_this.props.setSortType(value);
		}, _this.handleTextChange = function (e, _ref4) {
			var value = _ref4.value;
			var setSearchText = _this.props.setSearchText;

			setSearchText(value);
		}, _temp), _possibleConstructorReturn(_this, _ret);
	}

	_createClass(Filters, [{
		key: 'render',
		value: function render() {
			var appFilters = this.props.appFilters;

			return _react2.default.createElement(
				_semanticUiReact.Segment,
				null,
				_react2.default.createElement(
					_semanticUiReact.Form,
					null,
					_react2.default.createElement(
						_semanticUiReact.Form.Field,
						null,
						_react2.default.createElement(_semanticUiReact.Input, {
							icon: _react2.default.createElement(_semanticUiReact.Icon, { name: 'search' }),
							placeholder: 'Search...',
							value: appFilters.searchText,
							onChange: this.handleTextChange
						})
					),
					_react2.default.createElement(
						_semanticUiReact.Form.Group,
						{ widths: 'equal', inline: true },
						_react2.default.createElement(_semanticUiReact.Form.Select, { onChange: this.handleChange, label: 'Sort By', value: appFilters.sortBy, options: sortByOptions, placeholder: 'Sort Attribute' }),
						_react2.default.createElement(_semanticUiReact.Form.Select, { onChange: this.sortTypeChanged, label: 'Sort Type', value: appFilters.sortType, options: sortTypeOptions, placeholder: 'Sort Type' })
					)
				)
			);
		}
	}]);

	return Filters;
}(_react2.default.Component);

Filters.propTypes = {
	setSortBy: _propTypes2.default.func.isRequired,
	setSearchText: _propTypes2.default.func.isRequired,
	setSortType: _propTypes2.default.func.isRequired,
	apps: _propTypes2.default.object.isRequired,
	appStores: _propTypes2.default.object.isRequired,
	appFilters: _propTypes2.default.object.isRequired
};
var mapStateToProps = function mapStateToProps(state) {
	return {
		apps: state.apps,
		appStores: state.appStores,
		appFilters: state.appFilters
	};
};
var mapDispatchToProps = function mapDispatchToProps(dispatch) {
	return {
		setSortBy: function setSortBy(attributeName) {
			return dispatch(filterActions.setSortBy(attributeName));
		},
		setSearchText: function setSearchText(text) {
			return dispatch(filterActions.setSearchText(text));
		},
		setSortType: function setSortType(text) {
			return dispatch(filterActions.setSortType(text));
		}
	};
};

exports.default = (0, _reactRedux.connect)(mapStateToProps, mapDispatchToProps)(Filters);

/***/ }),

/***/ "./src/components/Pagination.jsx":
/*!***************************************!*\
  !*** ./src/components/Pagination.jsx ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
	value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _filter = __webpack_require__(/*! ../actions/filter */ "./src/actions/filter.js");

var filterActions = _interopRequireWildcard(_filter);

var _semanticUiReact = __webpack_require__(/*! semantic-ui-react */ "./node_modules/semantic-ui-react/dist/es/index.js");

var _propTypes = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");

var _propTypes2 = _interopRequireDefault(_propTypes);

var _react = __webpack_require__(/*! react */ "./node_modules/react/index.js");

var _react2 = _interopRequireDefault(_react);

var _reactRedux = __webpack_require__(/*! react-redux */ "./node_modules/react-redux/es/index.js");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var AppsPagination = function (_React$Component) {
	_inherits(AppsPagination, _React$Component);

	function AppsPagination() {
		var _ref;

		var _temp, _this, _ret;

		_classCallCheck(this, AppsPagination);

		for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
			args[_key] = arguments[_key];
		}

		return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = AppsPagination.__proto__ || Object.getPrototypeOf(AppsPagination)).call.apply(_ref, [this].concat(args))), _this), _this.handlePaginationChange = function (e, _ref2) {
			var activePage = _ref2.activePage;

			_this.props.setActivePage(activePage);
		}, _this.getTotalPages = function () {
			var _this$props = _this.props,
			    apps = _this$props.apps,
			    appFilters = _this$props.appFilters;

			return Math.ceil(apps.storeCount / appFilters.itemsPerPage);
		}, _temp), _possibleConstructorReturn(_this, _ret);
	}

	_createClass(AppsPagination, [{
		key: 'render',
		value: function render() {
			var appFilters = this.props.appFilters;

			return _react2.default.createElement(_semanticUiReact.Pagination, {
				activePage: appFilters.activePage,
				onPageChange: this.handlePaginationChange,
				totalPages: this.getTotalPages(),
				ellipsisItem: { content: _react2.default.createElement(_semanticUiReact.Icon, { name: 'ellipsis horizontal' }), icon: true },
				firstItem: { content: _react2.default.createElement(_semanticUiReact.Icon, { name: 'angle double left' }), icon: true },
				lastItem: { content: _react2.default.createElement(_semanticUiReact.Icon, { name: 'angle double right' }), icon: true },
				prevItem: { content: _react2.default.createElement(_semanticUiReact.Icon, { name: 'angle left' }), icon: true },
				nextItem: { content: _react2.default.createElement(_semanticUiReact.Icon, { name: 'angle right' }), icon: true }
			});
		}
	}]);

	return AppsPagination;
}(_react2.default.Component);

AppsPagination.propTypes = {
	setActivePage: _propTypes2.default.func.isRequired,
	apps: _propTypes2.default.object.isRequired,
	appFilters: _propTypes2.default.object.isRequired
};
var mapStateToProps = function mapStateToProps(state) {
	return {
		apps: state.apps,
		appFilters: state.appFilters
	};
};
var mapDispatchToProps = function mapDispatchToProps(dispatch) {
	return {
		setActivePage: function setActivePage(pageNumber) {
			return dispatch(filterActions.setActivePage(pageNumber));
		}
	};
};

exports.default = (0, _reactRedux.connect)(mapStateToProps, mapDispatchToProps)(AppsPagination);

/***/ }),

/***/ "./src/css/installer.css":
/*!*******************************!*\
  !*** ./src/css/installer.css ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {


var content = __webpack_require__(/*! !../../node_modules/mini-css-extract-plugin/dist/loader.js!../../node_modules/css-loader??ref--5-2!../../node_modules/postcss-loader/src??postcss!./installer.css */ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/index.js?!./node_modules/postcss-loader/src/index.js?!./src/css/installer.css");

if(typeof content === 'string') content = [[module.i, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! ../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ "./src/reducers/apps.js":
/*!******************************!*\
  !*** ./src/reducers/apps.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

exports.apps = apps;

var _constants = __webpack_require__(/*! ../actions/constants */ "./src/actions/constants.js");

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

var appsInitailState = {
    installed: [],
    storeApps: [],
    installedAppsLoading: true,
    storeAppsLoading: true,
    installedCount: 0,
    storeCount: 0,
    inProgress: false
};
function apps() {
    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : appsInitailState;
    var action = arguments[1];

    switch (action.type) {
        case _constants.ADD_INSTALLED_APPS:
            return _extends({}, state, { installed: [].concat(_toConsumableArray(state.installed), _toConsumableArray(action.payload)) });
        case _constants.ADD_STORE_APPS:
            return _extends({}, state, { storeApps: [].concat(_toConsumableArray(state.storeApps), _toConsumableArray(action.payload)) });
        case _constants.DELETE_INSTALLED_APPS:
            return _extends({}, state, {
                installed: state.installed.map(function (app) {
                    return !action.payload.includes(app.id);
                })
            });
        case _constants.DELETE_STORE_APPS:
            return _extends({}, state, {
                storeApps: state.storeApps.map(function (app) {
                    return !action.payload.includes(app.id);
                })
            });
        case _constants.SET_INSTALLED_APPS:
            return _extends({}, state, { installed: action.payload });
        case _constants.SET_STORE_APPS:
            return _extends({}, state, { storeApps: action.payload });
        case _constants.UPDATE_INSTALLED_APP:
            return _extends({}, state, {
                installed: state.installed.map(function (app) {
                    if (app.id === action.payload.id) {
                        return _extends({}, app, action.payload);
                    }
                    return app;
                })
            });
        case _constants.UPDATE_STORE_APP:
            return _extends({}, state, {
                storeApps: state.storeApps.map(function (storeApp) {
                    if (storeApp.id === action.payload.id) {
                        return _extends({}, storeApp, action.payload);
                    }
                    return storeApp;
                })
            });
        case _constants.INSTALLED_APPS_LOADING:
            return _extends({}, state, { installedAppsLoading: action.payload });
        case _constants.STORE_APPS_LOADING:
            return _extends({}, state, { storeAppsLoading: action.payload });
        case _constants.SET_APPS_TOTAL_COUNT:
            return _extends({}, state, { installedCount: action.payload });
        case _constants.SET_STORE_TOTAL_COUNT:
            return _extends({}, state, { storeCount: action.payload });
        case _constants.SET_ACTION_IN_PROGRESS:
            return _extends({}, state, { inProgress: action.payload });
        default:
            return state;
    }
}

/***/ }),

/***/ "./src/reducers/errors.js":
/*!********************************!*\
  !*** ./src/reducers/errors.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

exports.appErrors = appErrors;

var _constants = __webpack_require__(/*! ../actions/constants */ "./src/actions/constants.js");

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

var errorsInitailState = {
    errors: []
};
function appErrors() {
    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : errorsInitailState;
    var action = arguments[1];

    switch (action.type) {
        case _constants.ADD_ERRORS:
            return _extends({}, state, { errors: [].concat(_toConsumableArray(state.errors), _toConsumableArray(action.payload)) });
        case _constants.DELETE_ERROR:
            return _extends({}, state, {
                errors: state.errors.filter(function (error) {
                    return error !== action.payload;
                })
            });
        case _constants.SET_ERRORS:
            return _extends({}, state, { errors: action.payload });
        default:
            return state;
    }
}

/***/ }),

/***/ "./src/reducers/filter.js":
/*!********************************!*\
  !*** ./src/reducers/filter.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

exports.appFilters = appFilters;

var _constants = __webpack_require__(/*! ../actions/constants */ "./src/actions/constants.js");

var appConfig = {
    searchText: '',
    sortBy: 'title',
    activePage: 1,
    itemsPerPage: 9,
    sortType: 'asc'
};
function appFilters() {
    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : appConfig;
    var action = arguments[1];

    switch (action.type) {
        case _constants.SET_SEARCH_TEXT:
            return _extends({}, state, { searchText: action.payload });
        case _constants.SET_SORT_BY:
            return _extends({}, state, { sortBy: action.payload });
        case _constants.SET_ACTIVE_PAGE:
            return _extends({}, state, { activePage: action.payload });
        case _constants.SET_ITEMS_PER_PAGE:
            return _extends({}, state, { itemsPerPage: action.payload });
        case _constants.SET_SORT_TYPE:
            return _extends({}, state, { sortType: action.payload });
        default:
            return state;
    }
}

/***/ }),

/***/ "./src/reducers/index.js":
/*!*******************************!*\
  !*** ./src/reducers/index.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _errors = __webpack_require__(/*! ./errors */ "./src/reducers/errors.js");

var _filter = __webpack_require__(/*! ./filter */ "./src/reducers/filter.js");

var _stores = __webpack_require__(/*! ./stores */ "./src/reducers/stores.js");

var _apps = __webpack_require__(/*! ./apps */ "./src/reducers/apps.js");

var _redux = __webpack_require__(/*! redux */ "./node_modules/redux/es/redux.js");

exports.default = (0, _redux.combineReducers)({
    apps: _apps.apps,
    appStores: _stores.appStores,
    appFilters: _filter.appFilters,
    appErrors: _errors.appErrors
    // urls,
    // username,
    // token,
}); // import {
//     token,
//     urls,
//     username
// } from './other'

/***/ }),

/***/ "./src/reducers/stores.js":
/*!********************************!*\
  !*** ./src/reducers/stores.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; };

exports.appStores = appStores;

var _constants = __webpack_require__(/*! ../actions/constants */ "./src/actions/constants.js");

var appStoresInitailState = {
    stores: [],
    selectedStoreID: null,
    loading: true
};
function appStores() {
    var state = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : appStoresInitailState;
    var action = arguments[1];

    switch (action.type) {
        case _constants.SELECT_APP_STORE:
            return _extends({}, state, { selectedStoreID: action.payload });
        case _constants.SET_APP_STORES:
            return _extends({}, state, { stores: action.payload });
        case _constants.APP_STORES_LOADING:
            return _extends({}, state, { loading: action.payload });
        default:
            return state;
    }
}

/***/ }),

/***/ "./src/store/configureStore.js":
/*!*************************************!*\
  !*** ./src/store/configureStore.js ***!
  \*************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.configureStore = configureStore;

var _redux = __webpack_require__(/*! redux */ "./node_modules/redux/es/redux.js");

var _reduxThunk = __webpack_require__(/*! redux-thunk */ "./node_modules/redux-thunk/es/index.js");

var _reduxThunk2 = _interopRequireDefault(_reduxThunk);

var _reduxDevtoolsExtension = __webpack_require__(/*! redux-devtools-extension */ "./node_modules/redux-devtools-extension/index.js");

var _reducers = __webpack_require__(/*! ../reducers */ "./src/reducers/index.js");

var _reducers2 = _interopRequireDefault(_reducers);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function configureStore(initialState) {
    return (0, _redux.createStore)(_reducers2.default, initialState, (0, _reduxDevtoolsExtension.composeWithDevTools)((0, _redux.applyMiddleware)(_reduxThunk2.default)));
}

/***/ }),

/***/ "./src/store/index.js":
/*!****************************!*\
  !*** ./src/store/index.js ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});
exports.store = undefined;
exports.storeWithInitial = storeWithInitial;

var _configureStore = __webpack_require__(/*! ./configureStore */ "./src/store/configureStore.js");

var store = exports.store = (0, _configureStore.configureStore)();
function storeWithInitial(initialState) {
    return (0, _configureStore.configureStore)(initialState);
}
exports.default = store;

/***/ }),

/***/ 5:
/*!*********************************!*\
  !*** multi ./src/Installer.jsx ***!
  \*********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /Users/hishamkaram/Projects-Active/geonode_oauth_client/cartoview/app_manager/static/app_installer/src/Installer.jsx */"./src/Installer.jsx");


/***/ })

/******/ });
//# sourceMappingURL=installer.bundle.js.map