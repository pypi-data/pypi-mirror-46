"use strict";
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (Object.hasOwnProperty.call(mod, k)) result[k] = mod[k];
    result["default"] = mod;
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
require("es6-promise/auto"); // polyfill Promise on IE
require("@jupyterlab/application/style/index.css");
require("@jupyterlab/theme-light-extension/style/index.css");
const services_1 = require("@jupyterlab/services");
const mathjax2_1 = require("@jupyterlab/mathjax2");
const rendermime_1 = require("@jupyterlab/rendermime");
const coreutils_1 = require("@jupyterlab/coreutils");
const app_1 = require("./components/app");
// Our custom styles
require("../../styles/index.css");
const React = __importStar(require("react"));
const ReactDOM = __importStar(require("react-dom"));
function main() {
    let manager = new services_1.ServiceManager();
    manager.ready.then(() => {
        let kind = coreutils_1.PageConfig.getOption('kind');
        let path = coreutils_1.PageConfig.getOption('path');
        const rendermime = new rendermime_1.RenderMimeRegistry({
            initialFactories: rendermime_1.standardRendererFactories,
            latexTypesetter: new mathjax2_1.MathJaxTypesetter({
                url: coreutils_1.PageConfig.getOption('mathjaxUrl'),
                config: coreutils_1.PageConfig.getOption('mathjaxConfig')
            })
        });
        ReactDOM.render(React.createElement(app_1.App, { kind: kind, path: path, serviceManager: manager, renderMime: rendermime }), document.getElementById('everything-container'));
    });
}
window.addEventListener('load', main);
