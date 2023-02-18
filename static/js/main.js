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

    //let dropdownTriggers = document.querySelectorAll("nav .dropdown-trigger")
    //console.log(dropdownTriggers)

    function drawMain(task) {
        console.log(task)
        let taskType = task.type
        htm = `
        <h1>${task.title}</h1>
        <p style="margin-top: 10px;">${task.text}</p>
        `
        if (taskType == "auto_test") {
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
                    <input type="text" placeholder="Поле для ответа" style="width: 100%">
                </div>
                </div>
                `
            }

            htm += `</div>`
        } else if (taskType == "hr_confirmation") {

        } else if (taskType == "feedback") {

        }
        // <div style="margin-top: 10px;">
        //     <h2 style="display: inline;">Тестирование</h2>
        //     <div style="background: gold; border-radius: 15px; display: inline; padding: 5px; color: white;">+100500</div>
        // </div>
        // `
        mainHTML.innerHTML = htm
    }

    async function loadRoadmapWeekDay(week, day) {
        fetch(`/api/v1/task.week_day_tasks?week_num=${week}&day_num=${day}`)
        .then(response => response.json())
        .then(data => {
            drawMain(data[0])
        })
    }

    function jsTaskCards() {
        tasksCards = document.querySelectorAll("nav .task-card")
        console.log(tasksCards)
        for (let i = 0; i < tasksCards.length; i++) {
            tasksCards[i].addEventListener("click", function() {
                let week = this.getAttribute("data-week")
                let day = this.getAttribute("data-day")

                loadRoadmapWeekDay(week, day)
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
                    <div class="task card purple task-card" data-week='${task.week_num}' data-day='${task.day_num}'>
                    <div class="task-title" style="color: white;">
                        ${task.title}
                    </div>
                    <div class="task-status">
                        <div class="task-status-isdone" style="color: white;">
                            <input type="checkbox" disabled style="color: white;">Не пройдено
                        </div>
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