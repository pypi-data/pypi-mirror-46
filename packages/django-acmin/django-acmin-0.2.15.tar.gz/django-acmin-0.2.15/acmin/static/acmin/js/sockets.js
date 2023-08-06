$(function () {
    var ws_path = "ws://localhost:8000/whr/";
    console.log("Connecting to " + ws_path);
    var webSocketBridge = new channels.WebSocketBridge();
    webSocketBridge.connect(ws_path);
    webSocketBridge.listen(function (result) {
        var data = JSON.stringify(result)
        var tx = document.getElementById("messages");
        tx.innerHTML = tx.innerHTML + data + "\n<br/>"
    });

    // save blog post
    $(".post-button").click(function () {
        var message = document.getElementById("message").value
        webSocketBridge.send(
            {
                //path: "/api/hotel/ads/?position=4&imei=48:53:5A:FF:13:36",
                path: "/XXX/device/1000024/",
                method: "GET",
                data: {"hello": 1, "world": 2}
            });
        $(".content-post").val('');
    });


    // Helpful debugging
    webSocketBridge.socket.onopen = function () {
        console.log("Connected to notification socket");
    }
    webSocketBridge.socket.onclose = function () {
        console.log("Disconnected to notification socket");
    }
});


