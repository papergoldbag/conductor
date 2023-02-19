window.onload = () => {
    let mainBlock = document.querySelector('main')
    let balance

    async function buyProduct(id) {
        fetch("/api/v1/shop.buy_product?product_int_id=" + id)
        .then(data => data.json())
        .then(data => {
            console.log(data.is_done)
            location.reload()
        })
    }

    function jsBuyButtons() {
        let btns = document.querySelectorAll(".goodBuyButton")
        console.log(btns)
        for (let i = 0; i < btns.length; i++) {
            btns[i].addEventListener('click', function() {
                // console.log(this.getAttribute('data-id'))
                let id = this.getAttribute('data-id')
                buyProduct(id)
            })
        }
    }

    async function loadShop() {
        // let htm = ''
        // fetch("/api/v1/shop")
        // .then(data => data.json())
        // .then(shop => {

        // })
        fetch("/api/v1/shop")
        .then(data => data.json())
        .then(shop => {
            let htm = ''
            console.log(shop)
            for (let good of shop) {
                htm += `
                <div class="card grey" style="width: 95%; display: flex; align-items: center">
                    <img width="200px" src="/static/img/shopper.jpg">
                    <div style="width: calc(95% - 200px); padding: 15px; display: flex; justify-content: space-between;">
                        <div>
                            <h1>${good.title}</h1>
                            <p>${good.description}</p>
                        </div>`
                        if (good.already_bought) {
                            htm += `<span>Уже куплено</span> `
                        }
                        else htm+=`<button class='goodBuyButton primary' data-id='${good.int_id}'>$${good.cost}</button> `
                    htm +=`</div>
                </div>
                `
            }
            htm += '<br><br><br>'
            document.querySelector('#shop').innerHTML = htm
            jsBuyButtons()
        })
        // mainBlock.innerHTML += htm
        
    }

    async function checkRole() {
        fetch("/api/v1/me.my_profile")
        .then(data => data.json())
        .then(data => {
            let role = data.role
            if (role === 'hr' || role === 'supervisor') {
                document.querySelector('.header-links').innerHTML += `<a href="/adduser"><button class="secondary">Управление</button></a>`
            }
            if (role === 'employee') {
                document.querySelector('.header-links').innerHTML = `<a href="/roadmap"><button class="secondary">Roadmap</button></a>` + document.querySelector('.header-links').innerHTML
            }
            document.querySelector("#balance").innerHTML += `<h1>Монет: ${data.coins}</h1>`
        })
    }

    checkRole()
    loadShop()
    //getBalance()
}