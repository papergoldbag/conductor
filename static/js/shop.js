window.onload = () => {
    let mainBlock = document.querySelector('main')
    let balance

    async function getBalance() {

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
                        </div>
                        <button class="primary">$${good.cost}</button> 
                    </div>
                </div>
                `
            }
            htm += '<br><br><br>'
            mainBlock.innerHTML += htm
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
            mainBlock.innerHTML += `<h1>$${data.coins}</h1>`
        })
    }

    checkRole()
    loadShop()
    getBalance()
}