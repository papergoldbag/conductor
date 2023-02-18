window.onload = () => {
    async function checkRole() {
        console.log('test')
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
}