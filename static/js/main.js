window.onload = () => {
    const headerMenu = document.querySelector(".menu-button")
    let isHeaderMenuOpen = false

    const headerMenuLogic = () => {
        if (!isHeaderMenuOpen) {
            isHeaderMenuOpen = true
        } else {
            isHeaderMenuOpen = false
        }
        console.log(isHeaderMenuOpen)
    }

    headerMenu.addEventListener("click", headerMenuLogic)
}