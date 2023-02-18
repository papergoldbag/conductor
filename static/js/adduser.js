window.onload = () => {
    const fio = document.querySelector('#fio')
    const email = document.querySelector('#email')
    const role = document.querySelector('#role')
    const birth = document.querySelector('#birth')
    const template = document.querySelector('#template')
    const division = document.querySelector('#division')

    const createEmployeeButton = document.querySelector('#createEmployeeButton')
    createEmployeeButton.addEventListener('click', () => {
        //console.log(birth.value)
        if (fio.value != '' && email.value != '' && role.options[role.selectedIndex].value != '' && birth.value != '' && division.options[division.selectedIndex].value != '' && template.options[template.selectedIndex].value != '') {
            let json = {
                fullname: fio.value,
                email: fio.value,
                role: role.options[role.selectedIndex].value,
                birth_date: birth.value,
                roadmap_int_id: template.options[template.selectedIndex].value,
                division_int_id: division.options[division.selectedIndex].value
            }
            const settings = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify(json)
            }
            console.log(json)

            fetch("/api/v1/user.create", settings)
            .then(data => {
                console.log(data)
                // if (data.status == 200) {
                //     location.reload()
                // } else {
                //     alert('Ошибка')
                // }
            })
        } else alert('Неправильные входные данные')
        
    })

    async function loadTemplates() {
        fetch("/api/v1/roadmap_template")
        .then(data => data.json())
        .then(data => {
            for (let template_ of data) {
                template.innerHTML += `<option value="${division_.int_id}">${division_.title}</option>`
            }
        })
    }

    async function loadDivisions() {
        fetch("/api/v1/divisions")
        .then(data => data.json())
        .then(data => {
            for (let division_ of data) {
                division.innerHTML += `<option value="${division_.int_id}">${division_.title}</option>`
            }
        })
    }

    loadTemplates()
    loadDivisions()
}