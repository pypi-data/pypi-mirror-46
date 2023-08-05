
$(document).ready(function() {

    time_0 = (new Date()).getTime();
    counter = 0

    update_fps = function() {
        counter += 1
        if ((counter % 5) == 0) {
            tdif = (new Date()).getTime() - time_0;
            time_0 = (new Date()).getTime();
            fps = Math.round(5 * 1.0 / (tdif / 1000.0));
            $('#actual').text(fps);
        }
    }

    $('#fps').on('change', function() {
        var cmd = 'interval=' + $(this).val();
        console.log(cmd)
        ws_imagestream.send(cmd);
    });

    ws_imagestream = new_web_socket('imagestream');

    ws_imagestream.onmessage = function(e) {
        var interval = parseInt($('#fps').val());
        if (e.data instanceof Blob) {
            if (interval > 0) {
                update_fps()
                image.src = URL.createObjectURL(e.data);
                image.onload = function() {
                    URL.revokeObjectURL(image.src);
                }
            }
        }
        if (window.stream_mode == "get") {
            setTimeout(function(){ws_imagestream.send('?')}, interval);
        }
    }
/*
        interval = parseInt(document.getElementById('fps').value);
        if (interval > 0) {
            cmd = '?';
            if (e.data instanceof Blob) {
                image.src = URL.createObjectURL(e.data);
                image.onload = function() {
                    counter += 1;
                    URL.revokeObjectURL(image.src);
                    if ((counter % 5) == 0) {
                        tdif = (new Date()).getTime() - time_0;
                        time_0 = (new Date()).getTime();
                        fps = Math.round(5 * 1.0 / (tdif / 1000.0));
                        document.getElementById('actual').innerText = fps
                    }
                    setTimeout(function(){ws_imagestream.send('?')}, interval);
                    return;
                }
            }
        } else {
            interval = 1000;
            cmd = 'pause';
        }
        setTimeout(function(){ws_imagestream.send(cmd)}, interval);
    }
*/
    ws_imagestream.onopen = function() {
        console.log('connected ws_imagestream...');
        ws_imagestream.send('?');
    };
    ws_imagestream.onclose = function() {
        console.log('closed ws_imagestream');
    };
    ws_imagestream.send('?');
});

function new_web_socket(uri_path) {
    var protocol = 'ws:';
    if (window.location.protocol === 'https:') {
        protocol = 'wss:';
    }
    var host = window.location.host;
    var path = window.location.pathname;
    var url = protocol + '//' + host + path + uri_path;
    console.log(url)
    var ws = new WebSocket(url);
    return ws;
}
