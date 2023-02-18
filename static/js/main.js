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

    const dropdownTriggers = document.querySelectorAll("nav .dropdown-trigger")
    console.log(dropdownTriggers)

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

    function foo(el) {
        console.log(el)
    }
}