function removeChildElements(p) { while (p.firstChild) { p.firstChild.remove() } }
function openURL(url) { window.open(url, '_blank').focus() }

function capitalizeFirstLetter(word) {
    return word[0].toUpperCase() + word.slice(1)
}

function onlyDigits(event) {
    const input = event.target
    input.value = input.value.match(/^[0-9]*$/g)
}

function toggleFieldset(element, state, delay = 0) {
    setTimeout(() => {
        if (Array.isArray(element)) {
            element.forEach(fieldset => {
                fieldset.disabled = state
                fieldset.dataset.loading = state
            })
        } else {
            element.disabled = state
            element.dataset.loading = state
        }
    }, delay)
}

function fetchWrapper(url, init, callbacks = {}) {
    init.method = init.method ? init.method : 'GET'

    if ('body' in init) {
        bodyType = init.body.constructor.name.toLowerCase()
        switch (bodyType) {
            case 'formdata':
                break
            default:
                init.headers = { 'Content-Type': 'application/json;charset=utf-8' }
                init.body = JSON.stringify(init.body)
        }
    }

    fetch(url, init).then(async response => {
        const data = await response.json()
        if ('response' in callbacks) callbacks.response()
        switch (response.status) {
            case 200:
            case 201:
                if ('success' in callbacks) callbacks.success()
                break
            default:
                if ('default' in callbacks) callbacks.default()
                break
        }
        console.info(init.method, url, response.status, response.statusText)
        console.info(data)
    }).catch((error) => {
        if ('error' in callbacks) callbacks.error()
        console.error(error)
    })
}
