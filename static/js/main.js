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
    console.log(roadmapHTML)
    roadmapHTML.innerHTML += "<h1>test</h1>"

    //let dropdownTriggers = document.querySelectorAll("nav .dropdown-trigger")
    //console.log(dropdownTriggers)

    function jsRoadmap(roadmap) {
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
            roadmap = data.easy_view
            //console.log(roadmap)
            drawRoadmap(roadmap)
        })
    }

    function drawRoadmap(roadmap) {
        //console.log(roadmap[1][1][0][1]) // неделя -> день -> массив тасков
        // roadmapHTML.innerHTML += 'test'
        console.log(roadmap)
        let htm = ""
        
        for (const [week, weekArr] of Object.entries(roadmap)) {
            htm.innerHTML += '<div class="dropdown-trigger" data-isopen="true"><b>Неделя '+week+'</b></div>';
            htm.innerHTML += "test"+week;
            htm.innerHTML += '<div class="dropdown-content">'; //

                    // <div class="card grey dropdown">
                    //     <div class="dropdown-trigger" data-isopen="true">
                    //         <b>День 1</b>
                    //     </div>
                    //     <div class="dropdown-content"></div>

            //console.log(week, weekArr)
<<<<<<< HEAD
            roadmapHTML.innerHTML += 'hi'

            
            for (const [day, tasks] of Object.entries(weekArr)) {
                roadmapHTML.innerHTML += '<div class="card grey dropdown"><div class="dropdown-trigger" data-isopen="true"><b>День '+day+'</b></div>'
                roadmapHTML.innerHTML += '<div class="dropdown-content">';
                
=======
            // roadmapHTML.innerHTML += 'hi'//
            
            
            for (const [day, tasks] of Object.entries(weekArr)) {

                htm.innerHTML += '<div class="dropdown-content">';
                //roadmapHTML.innerHTML += "test"+day;
                //roadmapHTML.innerHTML += '<div class="card grey dropdown"><div class="dropdown-trigger" data-isopen="true"><b>День '+day+'</b></div>'
                //roadmapHTML.innerHTML += '<div class="dropdown-content">';
                /*
>>>>>>> origin/front
                for (let task of tasks) {
                    console.log(task)
                    roadmapHTML.innerHTML += `
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
                roadmapHTML.innerHTML += '</div>';
                */
            }
<<<<<<< HEAD

            weekNum = week
            for (const [day, tasks] of Object.entries(weekArr)) {
                dayNum = day
                // console.log("dayweek", day, week)
                for (const [] of Object.entries(day)) {
                    console.log(weekNum+"+"+dayNum, task)
                }
            }
            roadmapHTML.innerHTML += '</div>';
=======
            
            // weekNum = week
            // for (const [day, tasks] of Object.entries(weekArr)) {
            //     dayNum = day
            //     // console.log("dayweek", day, week)
            //     for (const [] of Object.entries(day)) {
            //         console.log(weekNum+"+"+dayNum, task)
            //     }
            // }
            // roadmapHTML.innerHTML += '</div>';//
>>>>>>> origin/front
        }
        htm.innerHTML += '</div>';
        jsRoadmap()
    }

    loadRoadmap()
    //console.log(roadmap)
}