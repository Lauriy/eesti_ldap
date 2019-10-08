const birthdaySocket = new WebSocket('ws://' + window.location.host + '/ws/birthday/' + year + '/' + month + '/' + day + '/');

birthdaySocket.onmessage = (e) => {
    var data = JSON.parse(e.data);
    console.log(data);
};

birthdaySocket.onclose = () => {
    console.error('Socket closed unexpectedly.');
};

// document.querySelector('#query-birthday-data-button').onclick = () => {
//     birthdaySocket.send(JSON.stringify({
//         'message': 123
//     }));
// };
