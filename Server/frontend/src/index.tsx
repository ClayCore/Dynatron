import React from 'react';
import ReactDOM from 'react-dom';
import App, { isMobile } from '~/App';
import initFonts from './utils/icon-library';

(function () {
    // Padding for main page loader
    const LOAD_PADDING = 1000;

    function $(what: string) {
        return document.querySelector(what);
    }

    function _(what: string) {
        return document.querySelectorAll(what);
    }

    function onReady(callback: Function) {
        let intervalId = window.setInterval(function () {
            if ($('body') !== undefined) {
                window.clearInterval(intervalId);
                callback.call(onReady);
            }
        }, LOAD_PADDING);
    }

    // Makes sure we're not running in a production environment while debugging etc.
    function checkEnv() {
        return !process.env.NODE_ENV || process.env.NODE_ENV === 'development'
            ? true
            : false;
    }

    function linkStyles() {
        if (isMobile()) {
            require('./scss/mobile/master.scss');
        } else {
            require('./scss/desktop/master.scss');
        }
    }

    function init() {
        // Wait for DOM to finish loading
        window.addEventListener('DOMContentLoaded', () => {
            let entryPoint = $('#root');
            let body = $('body');

            initFonts();
            linkStyles();

            // Add the loader only to the root webpage
            onReady(function () {
                body!.classList.add('loaded');
            });

            // Render everything
            ReactDOM.render(<App />, entryPoint);
        });
    }

    init();
})();
