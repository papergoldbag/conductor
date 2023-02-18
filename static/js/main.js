window.onload = () => {
    // const headerMenu = document.querySelector(".menu-button")
    // let isHeaderMenuOpen = false

    // const headerMenuLogic = () => {
    //     if (!isHeaderMenuOpen) {
    //         isHeaderMenuOpen = true
    //     } else {
    //         isHeaderMenuOpen = false
    //     }
    //     console.log(isHeaderMenuOpen)
    // }

    // headerMenu.addEventListener("click", headerMenuLogic)
    let roadmap = []
    let roadmapHTML = document.querySelector(".roadmap")
    let dropdownTriggers
    let mainHTML = document.querySelector("main")
    let asideHTML = document.querySelector("aside .links-list")

    let curTaskId

    //let dropdownTriggers = document.querySelectorAll("nav .dropdown-trigger")
    //console.log(dropdownTriggers)

    async function sendTest(curTaskId, arr) {
        console.log(curTaskId)  
        console.log(arr)
        for (let x of arr) {
            if (x == '') return
        }
        json = {
            task_num: curTaskId,
            answers: arr
        }
        const settings = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(json)
        }
        console.log(json)
        
        fetch("/api/v1/send_answers.send_quizz", settings)
        .then(data => {
            console.log(data)
            if (data.status == 200) {
                location.reload()
            } else {
                alert('Ошибка')
            }
        })
    }

    function drawMainAndAside(task) {
        console.log(task)
        let taskType = task.type
        htm = `
        <h1>${task.title}</h1>
        <p style="margin-top: 10px;">${task.text}</p>
        `
        if (taskType == "auto_test") {
            if (!task.is_completed) {
                htm += `
                    <div style="margin-top: 10px;">
                        <h2 style="display: inline;">Тестирование</h2>
                        <div style="background: gold; border-radius: 15px; display: inline; padding: 5px; color: white;">+${task.coins}</div>
                    </div>
                    <div class="quizz">
                `
                for (let i = 0; i < task.quizzes.length; i++) {
                    htm += `
                    <div class="quizz-elem card grey" style="padding: 15px;">
                    <div class="quizz-question">
                        ${i+1}) ${task.quizzes[i].question}
                    </div>
                    <div class="question-answer">
                        <input class="question-answer-input" type="text" placeholder="Поле для ответа" style="width: 100%">
                    </div>
                    </div>
                    `
                }

                htm += `</div><button class="primary sendTestButton" style="float: right;">Завершить тест</button>`
            }
        } else if (taskType == "hr_confirmation") {
            if (task.is_completed) {
                htm += `<input type="checkbox" checked disabled><span>Ваш HR проверил это задание</span>`
            } else {
                htm += `<input type="checkbox" disabled><span>Ваш HR ещё не проверил это задание</span>`
            }
        } else if (taskType == "feedback") {
            if (!task.is_completed) {
                htm += `
                    <div style="margin-top: 10px;">
                        <h2 style="display: inline;">Тестирование</h2>
                        <div style="background: gold; border-radius: 15px; display: inline; padding: 5px; color: white;">+${task.coins}</div>
                    </div>
                    <div class="quizz">
                `
                for (let i = 0; i < task.quizzes.length; i++) {
                    htm += `
                    <div class="quizz-elem card grey" style="padding: 15px;">
                    <div class="quizz-question">
                        ${i+1}) ${task.quizzes[i].question}
                    </div>
                    <div class="question-answer">
                        <input class="question-answer-input" type="text" placeholder="Поле для ответа" style="width: 100%">
                    </div>
                    </div>
                    `
                }

                htm += `</div><button class="primary sendTestButton" style="float: right;">Завершить тест</button>`
                /*
                htm +=  `
                <div style="margin-top: 10px;">
                    <h2 style="display: inline;">Обратный отзыв</h2>
                    <div style="background: gold; border-radius: 15px; display: inline; padding: 5px; color: white;">+${task.coins}</div>
                </div>
                <div class="quizz-elem card grey" style="padding: 15px;">
                <div class="quizz-question">
                    Обратный отзыв
                </div>
                <div class="question-answer">
                    <input class="question-answer-input" type="text" placeholder="ваш обратный отзыв )" style="width: 100%">
                </div>
                </div> 
                <button class="primary sendTestButton" style="float: right;">Завершить тест</button>
                `*/
            }
        }
        console.log(task.is_completed)
        if (task.is_completed) {
            htm += "<h1>Задание уже выполнено!</h1>"
        }
        // <div style="margin-top: 10px;">
        //     <h2 style="display: inline;">Тестирование</h2>
        //     <div style="background: gold; border-radius: 15px; display: inline; padding: 5px; color: white;">+100500</div>
        // </div>
        // `
        mainHTML.innerHTML = htm

        if (taskType != 'hr_confirmation' && !task.is_completed) {
            let sendTestButton = document.querySelector('main .sendTestButton')
            sendTestButton.addEventListener('click', () => {
                let inputs = document.querySelectorAll('.question-answer-input')
                //console.log(inputs)
                let arr = []
                for (let input of inputs) {
                    arr.push(input.value)
                }
                sendTest(curTaskId, arr)
            })
        }

        htm = ""
        for (let link of task.attachments) {
            //console.log(link)
            htm += `<a style='text-decoration: none' href=${link.url}><button class="secondary">${link.title}</button></a>`
        }
        asideHTML.innerHTML = htm
    }

    async function loadRoadmapWeekDay(week, day) {
        fetch(`/api/v1/task.week_day_tasks?week_num=${week}&day_num=${day}`)
        .then(response => response.json())
        .then(data => {
            drawMainAndAside(data[0])
        })
    }

    function jsTaskCards() {
        tasksCards = document.querySelectorAll("nav .task-card")
        console.log(tasksCards)
        for (let i = 0; i < tasksCards.length; i++) {
            tasksCards[i].addEventListener("click", function() {
                let week = this.getAttribute("data-week")
                let day = this.getAttribute("data-day")
                let id = this.getAttribute("data-id")
                let is_completed = (this.getAttribute("data-iscompleted") === 'true')
                console.log(is_completed)
                // if (!is_completed) {
                    curTaskId = id
                    //console.log(curTaskId)
                    loadRoadmapWeekDay(week, day)
                // } else {
                    
                // }
            })
        }
    }

    function jsRoadmap() {
        dropdownTriggers = document.querySelectorAll("nav .dropdown-trigger")

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
    }
    
    async function loadRoadmap() {
        const settings = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            }
            //body: JSON.stringify(user)
        }
        fetch("/api/v1/me.my_roadmap", settings)
        .then(response => response.json())
        .then(data => {
            roadmap = data.easy_view2
            drawRoadmap(roadmap)
        })
    }

    function drawRoadmap(roadmap) {
        weeks = roadmap.weeks
        htm = ""

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
                            <input type="checkbox" disabled`;
                            // task.is_completed = true
                            if (task.is_completed) {
                                htm += ' checked>';
                                // task.is_good = true
                                if (task.is_good != null) {
                                    if (task.is_good) {
                                        htm += `<div style='width: 15px; height: 15px; border-radius: 50%; background: lime'></div>`
                                    } else {
                                        htm += `<div style='width: 15px; height: 15px; border-radius: 50%; background: tomato'></div>`
                                    }
                                }
                            } else {
                                htm += '>'
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
            htm += `</div>`
        }
        //console.log(htm)
        roadmapHTML.innerHTML = htm
        jsRoadmap()
        jsTaskCards()
    }

    loadRoadmap()
    //console.log(roadmap)
}