window.onload = () => {
    const mainHTML = document.querySelector('main')

    async function loadEvents() {
        fetch('/api/v1/me.get_my_events')
        .then(data => data.json())
        .then(data => {
            console.log(data)
            let htm = ''
            for (let event_ of data) {
                htm += `
                <div class="card grey" style="width: 98%;">
                    <h2>${event_.title}</h2>
                    <p>${event_.desc}</p>
                    <b>${event_.dt.substring(0, 10)}</b>
                </div>
                `
            }
            //  console.log(mainHTML)
            mainHTML.innerHTML = htm
        })
    }

    async function checkRole() {
        fetch("/api/v1/me.my_profile")
        .then(data => data.json())
        .then(data => {
            let role = data.role
            if (role === 'hr' || role === 'supervisor') {
                document.querySelector('.header-links').innerHTML += `<a href="/adduser"><button class="secondary">Управление</button></a>`
            }
        })
    }

    checkRole()
    loadEvents()
}