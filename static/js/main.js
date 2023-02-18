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
    let raw_roadmap = {}
    let roadmap = []
    // let roadmap = {
    //     1: [],
    //     2: [],
    //     3: [],
    //     4: [],
    //     5: [],
    //     6: [],
    //     7: [],
    //     8: [],
    //     9: [],
    //     10: []
    // }

    const dropdownTriggers = document.querySelectorAll("nav .dropdown-trigger")
    //console.log(dropdownTriggers)

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
            console.log(data)
            // for (let task of data.tasks) {
            //     roadmap[task.week_num].push(task)
            // }
            for (let week of data.weeks) {
                roadmap[week] = []
            }
            for (let [week, arrDay] of data.week_to_days) {
                console.log(week, arrDay)
                // for (let day of arrDay) {
                //     let o = {day: []}
                //     roadmap[week].push( o )
                // }
            }
        })
        console.log(roadmap) 
        // for (let arr of roadmap) {
        //     arr.sort((a, b) => a.day_num)
        // }
    }

    loadRoadmap()
}