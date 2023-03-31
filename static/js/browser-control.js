function startPageHandler(event) {
    const container = event.currentTarget
    const button = event.target
    const input = container.querySelector('input')

    if (!button.dataset.cmd) return
    if (input.value.length === 0) {
        alert('Set start page')
        return
    }

    toggleFieldset(container, true)
    fetchWrapper('/web-browser/url',
        { method: 'POST', body: input.value },
        {
            response: () => { toggleFieldset(container, false, 1000) },
            error: () => { toggleFieldset(container, false, 1000) }
        }
    )
}

function main() {
    const setStartupPage = document.getElementById('set-startup-page')
    const input = setStartupPage.querySelector('input')
    setStartupPage.addEventListener('click', startPageHandler)

    fetch('/web-browser/url')
        .then(response => response.json())
        .then(data => { input.value = data })
}

main()
