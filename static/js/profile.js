window.onload = () => {
    const fullname = document.querySelector("#fullname")
    const coins = document.querySelector("#coins")
    const role = document.querySelector("#role")
    const birth_date = document.querySelector("#date")
    const position = document.querySelector("#position")
    const division = document.querySelector("#division")
    const telegram = document.querySelector("#telegram")
    const whatsapp = document.querySelector("#whatsapp")
    const vk = document.querySelector("#vk")
    const updateButton = document.querySelector("#updateButton")

    async function loadProfile() {
        fetch("/api/v1/me.my_profile")
        .then(data => data.json())
        .then(data => {
            console.log(data)
            fullname.innerHTML = data.fullname
            coins.innerHTML = 'Монет: '+data.coins
            if (data.role === 'hr') role.innerHTML = 'HR'
            else if (data.role === 'employee') role.innerHTML = 'Сотрудник'
            else if (data.role === 'supervisor') role.innerHTML = 'Руководитель'
            birth_date.innerHTML = (data.birth_date).substring(0, 10)
            position.innerHTML = data.position
            division.innerHTML = data.division_title
            telegram.value = data.telegram
            whatsapp.value = data.whatsapp
            vk.value = data.vk
        })
    }

    async function updateButtonHandler() {
        if (telegram.value != '' && whatsapp.value != '' && vk.value != '') {
            json = {
                telegram: telegram.value,
                whatsapp: whatsapp.value,
                vk: vk.value
            }
            const settings = {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify(json)
            }
            console.log(json)
            
            fetch("/api/v1/me", settings)
            .then(data => {
                console.log(data)
                if (data.status == 200) {
                    location.reload()
                } else {
                    alert('Ошибка')
                }
            })
        }
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
        })
    }

    checkRole()
    loadProfile()
    updateButton.addEventListener('click', updateButtonHandler)
}