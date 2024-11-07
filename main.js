
// JavaScript client
// Sends utterance to Python WebSocket server

var ws = new WebSocket("ws://127.0.0.1:8000/");
    ws.onopen = function () {
        ws.send('Hello, Server!!');
        //send a message to server once ws is opened.
        console.log("It's working onopen log / awake");
    };
    ws.onmessage = function (event) {
        var received_msg = evt.data;
        console.log(received_msg);
    };
    ws.onerror = function (error) {
        console.log('Error Logged: ' + error); //log errors
    };

    