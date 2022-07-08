<script>

    // import config
    import { APP_NAME, MSG_KEY_SELECTION, ENDPOINT_TTS } from './config.js';

    // import http lib
    import { reqPOST } from './http.js';

    // variables
    let disabled = false;


    function getCurrentTabId(){
        return new Promise((resolve, reject) => {
            chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
                resolve(tabs[0].id);
            });
        })
    }

    async function sendMessage(messageType){
        const tabId = await getCurrentTabId();
        return new Promise((resolve, reject) => {
            chrome.tabs.sendMessage(tabId, {type: messageType}, (res) => {
                resolve(res);
            });
        })
    }

    async function tts(){
        
        // set disabled flag
        disabled = true;

        // get current selection
        const selection = await sendMessage(MSG_KEY_SELECTION);

        // convert to text
        console.log(selection)
        
        // build form
        let data = new FormData();
        data.append('text', selection);

        // send post request
        await reqPOST(ENDPOINT_TTS, data );

        // set disabled flag
        disabled = false;
    }

</script>


<main>
    <div class="container">
        <p class="title">{APP_NAME}</p>
        <br>
        <div style="text-align: center; margin: 0px auto;">
            <button disabled={disabled} on:click={tts}>Text-to-Speech</button>
        </div>
    </div>
</main>


<style>

    :global(:root) {
        --black-dark: #222;
        --black: #444;
        --red: #e44e4e;
        --main-color: hsl(219, 42%, 41%);
        --font-size-very-very-very-small: 0.7em;
        --font-size-very-very-small: 0.8em;
        --font-size-very-small: 0.9em;
        --font-size-small: 1.05em;
        --font-size-normal: 1.3em;
        --font-size-large: 1.8em;
        --font-size-very-large: 2em;
        --font-bold: 600;
        --font-normal: 400;
        --max-width: 500px;
        --max-width-small: 400px;
    }

    main {
        width: var(--max-width);
        overflow-y: scroll;
        background-color: white;
        margin: 0px;
        padding: 8px;
    }

    .container {
        margin: 0px;
        padding: 16px;
        border: 1px solid var(--black);
        background-color: white;
    }

    p {
        padding: 0px;
    }

    .title {
        text-align: left;
        color: var(--black-dark);
        margin: 0px;
        font-weight: var(--font-bold);
        font-size: var(--font-size-large);
        max-width: var(--max-width);
    }

    button {
        background-color: white;
        border-width: 1px;
        border-style: solid;
        border-color: black;
        cursor: pointer;
        border-radius: 4px;
        text-align: center;
        padding: 16px;
    }

    button:hover:enabled {
        background-color: gray;
    }

</style>