window.onload = () => {
    const fullname = document.querySelector("#fullname")
    const role = document.querySelector("#role")
    const birth_date = document.querySelector("#date")
    const division = document.querySelector("#division")
    const telegram = document.querySelector("#telegram")
    const whatsapp = document.querySelector("#whatsapp")
    const vk = document.querySelector("#vk")

    async function loadProfile() {
        fetch("/api/v1/me.my_profile")
        .then(data => data.json())
        .then(data => {
            console.log(data)
            fullname.innerHTML = data.fullname
            role.innerHTML = data.role
            birth_date.innerHTML = (data.birth_date).substring(0, 10)
        })
    }

    async function checkRole() {
        fetch("/api/v1/me.my_profile")
        .then(data => data.json())
        .then(data => {
            let role = data.role
            if (role === 'hr') {
                document.querySelector('.header-links').innerHTML += `<a href="/adduser"><button class="secondary">Управление</button></a>`
            }
        })
    }

    checkRole()
    loadProfile()
}