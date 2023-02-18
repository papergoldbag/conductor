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
            console.log(data.easy_view)
            drawRoadmap(roadmap)
        })
    }

    function drawRoadmap(roadmap) {
        //console.log(roadmap[1][1][0][1]) // неделя -> день -> таск
        // roadmapHTML.innerHTML += 'test'
        //console.log(roadmap)
        let htm = ""
        /*
        for (const [week, weekArr] of Object.entries(roadmap)) {
            
            for (const [day, tasks] of Object.entries(weekArr)) {
                
                
            }
        }
        jsRoadmap()
        */
    }

    loadRoadmap()
    //console.log(roadmap)
}