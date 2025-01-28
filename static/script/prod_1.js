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

var token = localStorage.getItem('token')
var len = localStorage.length;
document.getElementById("add").addEventListener('click', () => {
    const name = document.getElementById("name").textContent
    const price = document.getElementById("price").textContent
    const size = document.getElementById("size").value
    const quantity = document.getElementById("quantity").value

    if (quantity > 5 || quantity < 0 || isNaN(quantity)) {
        alert("Your quantity should be lesser than 5 and greater than 0");
        return;
    }
    const item = { "PName": name, "PPrice": price, "Size": size, "Quantity": quantity };

    fetch('/api/session/', {
        method: 'POST',
        headers: {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(item),
    })
    setTimeout(itemfetch, 1000)

})
function itemfetch() {
    fetch('/api/session/', {
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
            var data = data.cartItem
            var object = Object.values(data)
            var length = 0
            for (let i = 0; i < object.length; i++) {
                length = length + (+object[i]["Quantity"])
            }
            document.getElementById("number").textContent = length
        })
}

