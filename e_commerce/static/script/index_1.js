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

fetch('http://127.0.0.1:8000/api/session/', {
    credentials: "same-origin",
    method: 'GET',
    headers: {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        "X-CSRFToken": getCookie("csrftoken"),

    },
})
    .then(response =>
        response.json()
    )
    .then(data => {
        console.log(data)
        var data = data.cartItem
        var object = Object.values(data)
        var length = 0
        for (let i = 0; i < object.length; i++) {
            length = length + (+object[i]["Quantity"])
        }
        document.getElementById("number").textContent = length
    })  