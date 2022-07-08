'use strict';

// import config
import { APP_NAME, MSG_KEY_SELECTION, MSG_KEY_CURRENT_URL } from './config.js';

// message interface
chrome.runtime.onMessage.addListener(async function(message, sender, sendResponse) {
        switch(message.type) {
            case MSG_KEY_CURRENT_URL:
                console.log(`${APP_NAME} - url requested`)
                const url = window.location.href;
                sendResponse(url);
                break;

            case MSG_KEY_SELECTION:
                console.log(`${APP_NAME} - selection requested`)
                const selection = window.getSelection().toString();
                sendResponse(selection);
                break;

            default:
                console.error(`${APP_NAME} - Unrecognised message: ${message.type}`);
        }
    }
);
