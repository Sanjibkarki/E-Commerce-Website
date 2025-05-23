
var token = localStorage.getItem('token')

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

fetch('/api/list/', {
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
        var items = data

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
            fetch(`/api/session_delete/${PName}`, {
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
/*
localStorage.removeItem("theme")
const number = localStorage.length;
if (number === 0){
    document.getElementById("title").style.display = "none";
    
    document.getElementById("text").textContent = "Your cart is Empty"
}
items = [];
for (let i = 0; i < number; i++) {
    const key = localStorage.key(i);
    const json = JSON.parse(localStorage.getItem(key));
    
    items.push({key,position: json.position, data: json.item });
    
}
items.sort((a, b) => a.position - b.position);
*/
    document.getElementById('order').addEventListener('click', () => {
        var token = localStorage.getItem('token')
        const a = prompt("Enter Your Number")
        fetch('/api/create/', {
            credentials: "same-origin",
            method: 'POST',
            headers: {
                "Authorization": 'Bearer ' + token,
                "Accept": "application/json",
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({"number": a})
        })

    })


/*
    let a =0;
 
    const requestData = []
    for (const item of items) {
        requestData.push({
            PName : item.PName,
            PPrice : +item.PPrice,
            Size : item.size,
            Quantity : item.quantity,
            product : "{{id}}"
        })
        
    console.log(requestData)
    const button = document.querySelectorAll(".cancel")
    button.forEach((btn)=>{
        btn.addEventListener('click',function(e){
           const element = e.target.id;
           localStorage.removeItem(element)
           window.location.reload();
           
        })
    })
    */
