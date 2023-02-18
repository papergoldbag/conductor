window.onload = () => {
    const fio = document.querySelector('#fio')
    const email = document.querySelector('#email')
    const role = document.querySelector('#role')
    const position = document.querySelector('#position')
    const birth = document.querySelector('#birth')
    const template = document.querySelector('#template')
    const division = document.querySelector('#division')

    const createEmployeeButton = document.querySelector('#createEmployeeButton')
    createEmployeeButton.addEventListener('click', () => {
        //console.log(birth.value)
        if (fio.value != '' && email.value != '' && role.options[role.selectedIndex].value != '' && position.value != '' && birth.value != '' && division.options[division.selectedIndex].value != '' && template.options[template.selectedIndex].value != '') {
            let json = {
                fullname: fio.value,
                email: email.value,
                role: role.options[role.selectedIndex].value,
                position: position.value,
                birth_date: birth.value + "T23:06:47.155Z",
                roadmap_template_int_id: parseInt(template.options[template.selectedIndex].value),
                division_int_id: parseInt(division.options[division.selectedIndex].value)
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
                if (data.status == 200) {
                    alert('Сотрудник успешно создан')
                } else {
                    alert('Ошибка')
                }
            })
        } else alert('Неправильные входные данные')
        
    })

    async function loadRoles() {
        fetch("/api/v1/roles.roles_with_title")
        .then(data => data.json())
        .then(data => {
            // console.log(data.roles)
            for (const [val, desc] of Object.entries(data.roles)) {
                // console.log(`${key}: ${value}`);
                role.innerHTML += `<option value="${val}">${desc}</option>`
            }
            // for (let role_ of data.roles) {
            //     role.innerHTML += `<option value="${role_.}">${role_}</option>`
            // }
        })
    }

    async function loadTemplates() {
        fetch("/api/v1/roadmap_template.mini")
        .then(data => data.json())
        .then(data => {
            //console.log(data)
            for (let template_ of data) {
                template.innerHTML += `<option value="${template_.int_id}">${template_.title}</option>`
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

    loadRoles()
    loadTemplates()
    loadDivisions()
}