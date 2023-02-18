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

    //let dropdownTriggers = document.querySelectorAll("nav .dropdown-trigger")
    //console.log(dropdownTriggers)

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
                    <div class="task card purple">
                    <div class="task-title" style="color: white;">
                        ${task.title}
                    </div>
                    <div class="task-status">
                        <div class="task-status-isdone" style="color: white;">
                            <input type="checkbox" disabled style="color: white;">Не пройдено
                        </div>
                        <div class="task-status-reward" style="color: white;">
                            +500
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
        console.log(htm)
        roadmapHTML.innerHTML = htm
        jsRoadmap()
    }

    loadRoadmap()
    //console.log(roadmap)
}