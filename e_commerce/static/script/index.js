
var token = localStorage.getItem('token')

/*function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();;
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
*/
/*var i = 0;
const items = [];
for (let i = 0; i < localStorage.length; i++) {
const key = localStorage.key(i);
const json = JSON.parse(localStorage.getItem(key));
 
items.push({key,position: json.position, data: json.item });
 
}
items.sort((a, b) => a.position - b.position);
for (const item of items){
i = i + (+item.data.quantity)
}
*/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();;
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
fetch('http://127.0.0.1:8000/api/list/', {
    credentials: "same-origin",
    method: 'GET',
    headers: {
        "Authorization": 'Bearer ' + token,
        "Accept": "application/json",
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken"),
    },
})
    .then(response =>
        response.json()
    )
    .then(data => {

        var object = Object.values(data)
        var length = 0
        for (let i = 0; i < object.length; i++) {
            length = length + (+object[i]["Quantity"])
        }
        document.getElementById("number").textContent = length
    })
