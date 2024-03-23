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
        var items = data.cartItem
        var a = 1
        
        if (Object.keys(items).length == 0) {
            document.getElementById("text").textContent = "NO ITEMS IN YOUR CART"
            document.getElementById("view").style.display = "None"
            document.getElementById("title").style.display = "None"

            return;
        }
        else {
            var p = Object.values(items)
            p.forEach(item => {
                const tr = document.createElement("tr")
                const th = document.createElement("th")
                const td1 = document.createElement("td")
                td1.className = "PName"
                td1.textContent = item.PName;
                const td2 = document.createElement("td")
                td2.textContent = item.PPrice
                const td3 = document.createElement("td")
                td3.textContent = item.Size
                const td4 = document.createElement("td")
                td4.textContent = item.Quantity
                const td5 = document.createElement("td")
                const btn = document.createElement("button")
                btn.setAttribute("class", "btn btn-primary cancel");
                btn.setAttribute("id", `${p.indexOf(item)}`)

                btn.setAttribute("type", 'button')
                btn.textContent = "cancel";
                td5.appendChild(btn)
                th.setAttribute("scope", "row")
                th.textContent = a;
                tr.appendChild(th)
                tr.appendChild(td1)
                tr.appendChild(td2)
                tr.appendChild(td3)
                tr.appendChild(td4)
                tr.appendChild(td5)
                document.getElementById("view").appendChild(tr)
                a = a + 1

            })
        }

    })

function buttons() {
    const button = document.querySelectorAll(".cancel")

    button.forEach((btn) => {
        btn.addEventListener('click', function (e) {
            const element = e.target.parentElement.parentElement;
            var PName = element.childNodes[1].textContent;
            fetch(`http://127.0.0.1:8000/api/session_delete/${PName}`, {
                credentials: "same-origin",
                method: 'DELETE',
                headers: {
                    "Accept": "application/json",
                    'Content-Type': 'application/json',
                    "X-CSRFToken": getCookie("csrftoken"),

                   
                },
            })
                .then(response => {
                    if (response.ok) {
                        element.remove()
                    } else {
                        console.error('Error deleting session:', response.statusText);
                    }
                })
                .catch(error => console.error('Error deleting session:', error));
        });
    });
}

setTimeout(buttons, 1000);
document.getElementById('click').addEventListener('click',()=>{
    window.location.href = '/login'
})
