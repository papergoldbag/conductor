window.onload = () => {
    let navHTML = document.querySelector('nav')
    let mainHTML = document.querySelector('main')
    let curID
    let isNotUser

    async function taskConfirmation(url) {
        fetch(url)
        .then(data => {
            console.log(data)
        })
    }

    function jsRoadmap() {
        dropdownTriggers = document.querySelectorAll(".dropdown-trigger")
        for (let i = 0; i < dropdownTriggers.length; i++) {
            dropdownTriggers[i].addEventListener("click", function() {
                let flag = (this.getAttribute("data-isopen") === 'true')
                console.log(flag)
                console.log(this.nextElementSibling)
                if (flag) {
                    this.nextElementSibling.style.display = "none"
                } else {
                    this.nextElementSibling.style.display = "block"
                }
                this.setAttribute("data-isopen", (!flag).toString())
                console.log(this)
            })
        }

        hrCheckboxes = document.querySelectorAll(".hr-checkbox")
        console.log(hrCheckboxes)
        for (let i = 0; i < dropdownTriggers.length; i++) {
            hrCheckboxes[i].addEventListener('click', function() {
                //console.log(this.getAttribute("data-id"))
                console.log(this.checked)
                if (!this.checked) {
                    this.checked = true
                    return
                }
                let userID = curID
                let taskID = this.getAttribute("data-index")
                let url = "/api/v1/task.confirmation?user_int_id=" + userID + "&task_index="+taskID
                console.log(url)
                taskConfirmation(url)
                //fetch("/api/v1/task.confirmation?user_int_id=" + userID + "&task_index="+taskID)    
            })
        }
     }
    

    function drawRoadmap(weeks) {
        htm = ''
        for (let week of weeks) {
            weekNumber = week.week
            htm += `
            <div class="dropdown-trigger" data-isopen="true">
                <b>Неделя ${weekNumber}</b>
            </div>
            <div class="dropdown-content">
            `

            for (let day of week.days) {
                dayNumber = day.day
                htm += `
                <div class="card grey dropdown">
                <div class="dropdown-trigger" data-isopen="true">
                    <b>День ${dayNumber}</b>
                </div>
                <div class="dropdown-content">
                `
                for (let task of day.tasks) {
                    //console.log(task)
                    htm +=  `
                    <div class="task card purple task-card" data-iscompleted=${task.is_completed} data-week='${task.week_num}' data-day='${task.day_num}' data-id=${task.index}>
                    <div class="task-title" style="color: white;">
                        ${task.title}
                    </div>
                    <div class="task-status">
                        <div class="task-status-isdone" style="color: white; display: flex">
                            <input type="checkbox" onclick="return false;"`;
                            // task.is_completed = true
                            if (task.is_completed) {
                                htm += ' checked>';
                                // task.is_good = true
                                if (task.is_good != null && task.type != 'feedback') {
                                    if (task.is_good) {
                                        htm += `<div style='width: 13px; height: 13px; border-radius: 50%; background: lime; margin-top: 4px;'></div>`
                                    } else {
                                        htm += `<div style='width: 13px; height: 13px; border-radius: 50%; background: tomato; margin-top: 4px;'></div>`
                                    }
                                }
                                htm += '<span style="color: #f0f0f0">Сотрудник выполнил это задание</span>'
                                if (task.type === 'hr_confirmation') {
                                    htm += '<br><input data-index="'+task.index+'" class="hr-checkbox" type="checkbox"'
                                    if (task.is_confirmed_by_int_id !== null) htm += 'checked'
                                    htm +='><b style="color: #f0f0f0">Подтвердить выполнение задания</b>'
                                }
                            } else {
                                htm += '>'

                                htm += '<span  style="color: #f0f0f0">Сотрудник не выполнил это задание</span>'
                                if (task.type === 'hr_confirmation') {
                                    htm += '<br><input data-index="'+task.index+'" class="hr-checkbox" type="checkbox"'
                                    if (task.is_confirmed_by_int_id !== null) htm += 'checked'
                                    htm +='><b style="color: #f0f0f0">Подтвердить выполнение задания</b>'
                                }
                            }
                            //htm += ` style="color: white;">
                        htm += `</div>
                        <div class="task-status-reward" style="color: white;">
                            +${task.coins}
                        </div>
                        </div>
                    </div>
                    `
                }
                htm += `
                </div>
                </div>
                `
            }
            htm += `</div><br><br><br>`
        }
        //console.log(htm)
        mainHTML.innerHTML += htm
        jsRoadmap()
    }

    async function loadRoadmap(id) {
        fetch('/api/v1/task.user_roadmap?user_int_id='+id)
        .then(data => data.json())
        .then(roadmap => {
            //console.log(roadmap.easy_view2)
            drawRoadmap(roadmap.easy_view2.weeks)
        })
    }

    function drawUserProfile(user) {
        htm = `
        <div class="profile card grey" style="width: 95%; height: 174px;">
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
                curID = id
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
            if (role === 'employee') {
                document.querySelector('.header-links').innerHTML = `<a href="/roadmap"><button class="secondary">Roadmap</button></a>` + document.querySelector('.header-links').innerHTML
            }
        })
    }

    checkRole()
    loadUsers()
}