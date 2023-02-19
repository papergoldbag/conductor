window.onload = () => {
    let navHTML = document.querySelector('nav')
    let mainHTML = document.querySelector('main')
    let isNotUser

    async function loadRoadmap(id) {
        fetch('/api/v1/task.user_roadmap?user_int_id='+id)
        .then(data => data.json())
        .then(roadmap => {
            console.log(roadmap)
            //drawUserProfile(user)
        })
    }

    function drawUserProfile(user) {
        htm = `
        <div class="profile card grey" style="width: 95%;">
            <h1>${user.fullname}</h1>
            <div>
                <div style="background: lime; border-radius: 15px; display: inline; padding: 5px; color: white;">`;
                if (user.role === 'hr') htm += 'HR';
                else if (user.role === 'supervisor') htm += 'Руководитель';
                else if (user.role === 'employee') htm += 'Сотрудник';
                htm += `</div>
                <span class="date">${user.birth_date.substring(0, 10)}</span>
                <span class="division" style="background: purple; border-radius: 15px; display: inline; padding: 5px; color: white;">${user.division_title}</span>
            </div>
            <div style="margin-top: 10px;">
                <div style="display: flex">
                    <div style="width: 50%;">
                        <p>Telegram</p>`;
                        if (user.telegram != null) htm += `<a href="${user.telegram}">${user.telegram}</a>`
                        else htm += `<b>Не указано</b>`
                        htm += `
                    </div>
                    <div style="width: 50%;">
                        <!--<p>WhatsApp</p>
                        <a href=""></a>-->
                    </div>
                </div>
                <div style="display: flex">
                    <div style="width: 50%;">
                        <p>VK</p>`
                        if (user.vk != null) htm += `<a href="${user.vk}">${user.vk}</a>`
                        else htm += `<b>Не указано</b>`
                        htm += `
                    </div>
                    <div style="width: 50%;">
                        <p>Email</p>
                        `
                        if (user.email != null) htm += `<a href="mailto:${user.email}">${user.email}</a>`
                        else htm += `<b>Не указано</b>`
                    htm  += `</div>
                </div>
            </div>
        </div>
        `
        mainHTML.innerHTML = htm
        if (user.roadmap_int_id != null && isNotUser) loadRoadmap(user.int_id)
    }

    async function getUserById(id) {
        fetch('/api/v1/user.by_int_id?user_int_id='+id)
        .then(data => data.json())
        .then(user => {
            console.log(user)
            drawUserProfile(user)
        })
    }

    function jsUsers() {
        let usersHTML = document.querySelectorAll(".user")
        for (let user of usersHTML) {
            user.addEventListener('click', function() {
                let id = this.getAttribute('data-id')
                getUserById(id)
            })
        }
    }

    function drawUsersList(users) {
        let htm = ''
        for (let user of users) {
            htm += `
            <div data-id="${user.int_id}" class="card grey user" style="width: 98%; cursor: pointer">
            <h2>${user.fullname}</h2>`
            if (user.role === 'hr') {
                htm += `<h3>HR</h3>`
            }
            else if (user.role === 'employee') {
                htm += `<h3>Сотрудник</h3>`
            }
            else if (user.role === 'supervisor') {
                htm += `<h3>Руководитель</h3>`
            }
            htm += `<p>${user.position}</p>
            <b>${user.division_title}</b>
            </div>
            `
        }
        htm += '<br><br><br>'
        navHTML.innerHTML += htm
        jsUsers()
    }

    async function loadUsers() {
        fetch("/api/v1/user")
        .then(data => data.json())
        .then(users => {
            drawUsersList(users)
        })
    }

    async function checkRole() {
        fetch("/api/v1/me.my_profile")
        .then(data => data.json())
        .then(data => {
            let role = data.role
            if (role === 'hr' || role === 'supervisor') {
                document.querySelector('.header-links').innerHTML += `<a href="/adduser"><button class="secondary">Управление</button></a>`
                isNotUser = true
            } else {
                isNotUser = false
            }
        })
    }

    checkRole()
    loadUsers()
}