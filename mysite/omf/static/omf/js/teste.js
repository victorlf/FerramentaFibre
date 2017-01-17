var socket = io.connect("/teste");

socket.on('connect', function (){
   $('#1').append('<p>Conectado</p>');
});