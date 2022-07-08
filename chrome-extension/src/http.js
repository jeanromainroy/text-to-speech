'use strict';


/**
* A GET request using XMLHttpRequest
*
* @param url           The target url
*/
export function reqGET (url, responseType = 'json') {
    return new Promise(function (resolve, reject) {
        const xhr = new XMLHttpRequest()

        // Setup our listener to process compeleted requests
        xhr.onload = function () {
            
            // check for message
            let message
            if (xhr.response) message = xhr.response.message;

            // Process the response
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.response)
            } else {
                reject({
                    status: xhr.status,
                    statusText: xhr.statusText,
                    message: message
                })
            }
        }

        // On error
        xhr.onerror = function (e) {
            reject({
                status: xhr.status,
                statusText: xhr.statusText
            })
        }

        // Setup our HTTP request
        xhr.open('GET', url, true)
        xhr.responseType = responseType;

        // Send the request
        xhr.send()
    })
}

/**
* A POST request using XMLHttpRequest
*
* @param url           The target url
* @param payload       The request body in JSON format, e.g. {"email": "hey@mail.com", "password": "101010"}
*/
export function reqPOST (url, payload = {}) {
    return new Promise(function (resolve, reject) {
        // Create a request
        const xhr = new XMLHttpRequest()

        // Setup our listener to process compeleted requests
        xhr.onload = function () {

            // check for message
            let message
            if (xhr.response) message = xhr.response.message

            // Process the response
            if (xhr.status >= 200 && xhr.status < 300) {
                resolve(xhr.response)
            } else {
                reject({
                    status: xhr.status,
                    statusText: xhr.statusText,
                    message: message
                })
            }
        }

        // On error
        xhr.onerror = function (e) {
            // If failed
            reject({
                status: xhr.status,
                statusText: xhr.statusText
            })
        }

        // Setup our HTTP request
        xhr.open('POST', url, true)

        // Send the request
        xhr.send(payload)
    })
}
