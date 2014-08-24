/*window.onload = function() {
    var terminal = document.getElementById('console');
    var input = document.getElementById('console-input');
    var ws = new WebSocket('ws://' + location.host + '/sock');
    terminal.value = '';
    
    ws.onmessage = function(evt) {
        terminal.value += evt.data + '\n';
        terminal.scrollTop = terminal.scrollHeight
    }
    
    input.onkeypress = function(evt) {
        if (evt.keyCode == 13 || evt.which == 13) {
            ws.send(input.value);
            input.value = '';
            return false;
        }
    }
}*/

$(function() {
    var ws = new WebSocket('ws://' + location.host + '/sock');
    var term = $('#terminal').terminal(function(command, term) {
        ws.send(command);
    }, { prompt: '>', greeting: false });
    
    ws.onmessage = function(evt) {
        term.echo(evt.data);
    }
});
