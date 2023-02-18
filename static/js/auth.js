window.onload = () => {
    const form = document.querySelector("form")
    const codeSendButton = document.querySelector(".codeSendButton")

    const validateEmail = (email) => {
        return String(email)
        .toLowerCase()
        .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
    };

    async function validateAuth(event) {
        // return validateEmail(mail)
        event.preventDefault()
        //console.log("lol")
        let formData = new FormData(form)

        // validate formData
        let mail = formData.get("email")
        let code = formData.get("code")
        if (validateEmail(mail)) {
            let user = {
                mail: mail,
                code: code
            }
            console.log(user)
            const settings = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify(user)
            }
            fetch("/api/v1/auth", settings)
            .then(data => {
                if (data.status == 200) {
                    window.location.replace("/roadmap");
                } else {
                    alert('Некорректные данные!')
                }
            })
        } else {
            alert("Некорректный email!")
        }

        // for (let [k, v] of formData) {
        //     console.log(k, v)
        // }
    }

    async function codeSendButtonHandler() {
        let mail = document.querySelector(".email").value
        if (validateEmail(mail)) {
            const settings = {
                // headers: {
                //     "token": 'uaqFXhzjxuiVNfyTmSGeVfjukPfSDihfTifTShMtaMOaQRpFAl'
                // }
            }
            // проверка мыла
            let url = "/api/v1/auth.send_mail_code?mail=" + mail
            console.log(url)
            await fetch(url, settings)
        } else {
            alert("Некорректный email!")
        }
    }

    form.addEventListener("submit", validateAuth)
    codeSendButton.addEventListener("click", codeSendButtonHandler)
}