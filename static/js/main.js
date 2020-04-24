/* REMOVE Socket IO API is no longer in use */
    var socket = io();
    $(document).ready(function() {
        socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

        socket.on('connect', function() {
            socket.emit('joined', {});
        });

        socket.on('connect', function() {
            socket.emit('admin_joined', {});
        });

        /* TEMPORARILY COMMENTED: DO NOT DELETE */
        socket.on('status', function(data) {
            $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
        });

        socket.on('message', function(data) {
            $('#chat').val($('#chat').val() + data.msg + '\n');
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
        });

        $('#text').keypress(function(e) {
            var code = e.keyCode || e.which;
            if (code == 13) {
                text = $('#text').val();
                $('#text').val('');
                socket.emit('text', {msg: text});
            }
        });

    });

    // Having trouble calling theses functions 3-11-2020 unless inline
    function select_room(room) {
        console.log("Joining room: " + room);
        // async function
        socket.join_room(room, function() {
            window.location.href = "/chat";
            console.log(socket.id + " now in rooms ", socket.rooms);
        });

    }

    function leave_room() {
        socket.emit('left', {}, function() {
            socket.disconnect();
            // go back to the login page
            window.location.href = "{{url_for('main.support')}}";
        });
    }

