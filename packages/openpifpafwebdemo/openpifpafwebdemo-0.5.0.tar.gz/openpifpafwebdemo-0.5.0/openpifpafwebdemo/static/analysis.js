(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else if(typeof exports === 'object')
		exports["openpifpafwebdemo"] = factory();
	else
		root["openpifpafwebdemo"] = factory();
})(window, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
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
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./js/src/frontend.ts");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./js/src/camera.ts":
/*!**************************!*\
  !*** ./js/src/camera.ts ***!
  \**************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var defaultCapabilities = { audio: false, video: { width: 640, height: 480 } };
var Camera = /** @class */ (function () {
    function Camera(ui) {
        var _this = this;
        this.ui = ui;
        this.video = ui.getElementsByTagName('video')[0];
        this.captureCanvas = ui.getElementsByTagName('canvas')[0];
        this.originalCaptureCanvasSize = [this.captureCanvas.width,
            this.captureCanvas.height];
        this.captureContext = this.captureCanvas.getContext('2d');
        this.buttonNextCamera = ui.getElementsByClassName('nextCamera')[0];
        this.captureCounter = 0;
        navigator.mediaDevices.enumerateDevices().then(function (devices) {
            _this.cameraIds = devices
                .filter(function (device) { return device.kind === 'videoinput'; })
                .map(function (device) { return device.deviceId; });
            // On iOS, all deviceId and label for devices are empty.
            // So making up labels here that should be used for facingMode instead.
            if (_this.cameraIds.length >= 2 && _this.cameraIds.every(function (i) { return i === ''; })) {
                _this.cameraIds = ['user', 'environment'];
            }
        }).catch(function (err) {
            console.log(err.name + ': ' + err.message);
        });
        this.setCamera();
        this.buttonNextCamera.onclick = this.nextCamera.bind(this);
    }
    Camera.prototype.setCamera = function (cameraId) {
        return __awaiter(this, void 0, void 0, function () {
            var capabilities, stream;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (cameraId && cameraId === this.cameraId)
                            return [2 /*return*/];
                        capabilities = __assign({}, defaultCapabilities, { video: __assign({}, defaultCapabilities.video) });
                        if (cameraId === 'user' || cameraId === 'environment') {
                            capabilities.video.facingMode = cameraId;
                        }
                        else {
                            capabilities.video.deviceId = cameraId;
                        }
                        return [4 /*yield*/, navigator.mediaDevices.getUserMedia(capabilities)];
                    case 1:
                        stream = _a.sent();
                        this.video.srcObject = stream;
                        this.cameraId = cameraId;
                        return [2 /*return*/];
                }
            });
        });
    };
    Camera.prototype.imageData = function () {
        // update capture canvas size
        var landscape = this.video.clientWidth > this.video.clientHeight;
        var targetSize = landscape ? this.originalCaptureCanvasSize : this.originalCaptureCanvasSize.slice().reverse();
        if (this.captureCanvas.width !== targetSize[0])
            this.captureCanvas.width = targetSize[0];
        if (this.captureCanvas.height !== targetSize[1])
            this.captureCanvas.height = targetSize[1];
        // capture
        this.captureCounter += 1;
        this.captureContext.drawImage(this.video, 0, 0, this.captureCanvas.width, this.captureCanvas.height);
        return { image_id: this.captureCounter, image: this.captureCanvas.toDataURL() };
    };
    Camera.prototype.nextCamera = function () {
        var nextCameraId = undefined;
        if (this.cameraId && this.cameraIds.length > 1) {
            var currentCameraIndex = this.cameraIds.indexOf(this.cameraId);
            var nextCameraIndex = currentCameraIndex + 1;
            if (nextCameraIndex >= this.cameraIds.length)
                nextCameraIndex = 0;
            nextCameraId = this.cameraIds[nextCameraIndex];
        }
        else if (this.cameraIds.length > 1) {
            // assume the default (unset this.cameraId) was camera 0, so go to 1
            nextCameraId = this.cameraIds[1];
        }
        else {
            nextCameraId = this.cameraIds[0];
        }
        this.setCamera(nextCameraId);
    };
    return Camera;
}());
exports.Camera = Camera;


/***/ }),

/***/ "./js/src/frontend.ts":
/*!****************************!*\
  !*** ./js/src/frontend.ts ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

/* global document */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var camera_1 = __webpack_require__(/*! ./camera */ "./js/src/camera.ts");
var visualization_1 = __webpack_require__(/*! ./visualization */ "./js/src/visualization.ts");
var backend_location = '';
if (document.location.search && document.location.search[0] === '?') {
    backend_location = document.location.search.substr(1);
}
if (!backend_location && document.location.hostname === 'vita-epfl.github.io') {
    backend_location = 'https://vitademo.epfl.ch';
}
var fpsSpan = document.getElementById('fps');
var captureCounter = 0;
var fps = 0.0;
var lastProcessing = null;
var c = new camera_1.Camera(document.getElementById('capture'));
var vis = new visualization_1.Visualization(document.getElementById('visualization'));
function newImage() {
    return __awaiter(this, void 0, void 0, function () {
        var data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    data = c.imageData();
                    return [4 /*yield*/, new Promise(function (resolve, reject) {
                            var xhr = new XMLHttpRequest();
                            xhr.open('POST', backend_location + '/process', true);
                            xhr.onload = function () {
                                return __awaiter(this, void 0, void 0, function () {
                                    var duration, body;
                                    return __generator(this, function (_a) {
                                        switch (_a.label) {
                                            case 0:
                                                if (lastProcessing != null) {
                                                    duration = Date.now() - lastProcessing;
                                                    fps = 0.5 * fps + 0.5 * (1000.0 / duration);
                                                    fpsSpan.textContent = "" + fps.toFixed(1);
                                                }
                                                lastProcessing = Date.now();
                                                body = JSON.parse(this['responseText']);
                                                return [4 /*yield*/, vis.draw(data.image, body)];
                                            case 1:
                                                _a.sent();
                                                resolve();
                                                return [2 /*return*/];
                                        }
                                    });
                                });
                            };
                            xhr.onerror = function () { return reject(); };
                            xhr.setRequestHeader('Content-Type', 'application/json');
                            xhr.send(JSON.stringify(data));
                        })];
                case 1:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
exports.newImage = newImage;
function loop_forever() {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (false) {}
                    return [4 /*yield*/, newImage()];
                case 1:
                    _a.sent();
                    return [4 /*yield*/, new Promise(function (resolve) { return requestAnimationFrame(function () { return resolve(); }); })];
                case 2:
                    _a.sent();
                    return [3 /*break*/, 0];
                case 3: return [2 /*return*/];
            }
        });
    });
}
loop_forever();


/***/ }),

/***/ "./js/src/visualization.ts":
/*!*********************************!*\
  !*** ./js/src/visualization.ts ***!
  \*********************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

"use strict";

Object.defineProperty(exports, "__esModule", { value: true });
var COCO_PERSON_SKELETON = [
    [16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13],
    [6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3],
    [2, 4], [3, 5], [4, 6], [5, 7]
];
var COLORS = [
    '#1f77b4',
    '#aec7e8',
    '#ff7f0e',
    '#ffbb78',
    '#2ca02c',
    '#98df8a',
    '#d62728',
    '#ff9896',
    '#9467bd',
    '#c5b0d5',
    '#8c564b',
    '#c49c94',
    '#e377c2',
    '#f7b6d2',
    '#7f7f7f',
    '#c7c7c7',
    '#bcbd22',
    '#dbdb8d',
    '#17becf',
    '#9edae5',
];
var Visualization = /** @class */ (function () {
    function Visualization(ui) {
        this.canvas = ui.getElementsByTagName('canvas')[0];
        this.originalCanvasSize = [this.canvas.width, this.canvas.height];
        this.context = this.canvas.getContext('2d');
        this.lineWidth = 10;
        this.markerSize = 4;
    }
    Visualization.prototype.draw = function (image, data) {
        var _this = this;
        var scores = data.map(function (entry) { return entry.score; });
        // adjust height of output canvas
        if (data && data.length > 0) {
            var landscape = data[0].width_height[0] > data[0].width_height[1];
            var targetSize = landscape ? this.originalCanvasSize : this.originalCanvasSize.slice().reverse();
            if (this.canvas.width !== targetSize[0])
                this.canvas.width = targetSize[0];
            if (this.canvas.height !== targetSize[1])
                this.canvas.height = targetSize[1];
        }
        // draw on output canvas
        var i = new Image();
        i.onload = function () {
            _this.context.drawImage(i, 0, 0, _this.canvas.width, _this.canvas.height);
            data.forEach(function (entry) { return _this.drawSkeleton(entry.coordinates, entry.detection_id); });
        };
        i.src = image;
    };
    Visualization.prototype.drawSkeletonLines = function (keypoints) {
        var _this = this;
        COCO_PERSON_SKELETON.forEach(function (joint_pair, connection_index) {
            var joint1i = joint_pair[0], joint2i = joint_pair[1];
            var joint1xyv = keypoints[joint1i - 1];
            var joint2xyv = keypoints[joint2i - 1];
            var color = COLORS[connection_index % COLORS.length];
            _this.context.strokeStyle = color;
            _this.context.lineWidth = _this.lineWidth;
            if (joint1xyv[2] === 0.0 || joint2xyv[2] === 0.0)
                return;
            _this.context.beginPath();
            _this.context.moveTo(joint1xyv[0] * _this.canvas.width, joint1xyv[1] * _this.canvas.height);
            _this.context.lineTo(joint2xyv[0] * _this.canvas.width, joint2xyv[1] * _this.canvas.height);
            _this.context.stroke();
        });
    };
    Visualization.prototype.drawSkeleton = function (keypoints, detection_id) {
        var _this = this;
        this.drawSkeletonLines(keypoints);
        keypoints.forEach(function (xyv, joint_id) {
            if (xyv[2] === 0.0)
                return;
            _this.context.beginPath();
            _this.context.fillStyle = '#ffffff';
            _this.context.arc(xyv[0] * _this.canvas.width, xyv[1] * _this.canvas.height, _this.markerSize, 0, 2 * Math.PI);
            _this.context.fill();
        });
    };
    return Visualization;
}());
exports.Visualization = Visualization;


/***/ })

/******/ });
});
//# sourceMappingURL=analysis.js.map