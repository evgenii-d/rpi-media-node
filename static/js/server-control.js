function uploadAppHandler(event) {
    const container = event.currentTarget
    const element = event.target
    const formData = new FormData()
    const files = container.querySelector('input[type=file]').files

    if (!element.dataset.cmd) return

    switch (element.dataset.cmd) {
        case 'upload':
            if (files.length === 0) { alert('Select file'); return }

            toggleFieldset(container, true)
            formData.append('archive', files[0])

            fetchWrapper('/web-server/archive', { method: 'POST', body: formData },
                {
                    response: () => { toggleFieldset(container, false, 1000) },
                    error: () => { toggleFieldset(container, false, 1000) }
                }
            )
            break
    }
}

function miscHandler(event) {
    const element = event.target
    const protocol = window.location.protocol
    const hostname = window.location.hostname
    const port = 8080

    if (!element.dataset.cmd) return
    switch (element.dataset.cmd) {
        case 'download':
            openURL('/web-server/archive')
            break
        case 'open':
            openURL(`${protocol}//${hostname}:${port}`)
            break
    }
}

function main() {
    const uploadApp = document.getElementById('upload-app')
    uploadApp.addEventListener('click', uploadAppHandler)

    const misc = document.getElementById('misc')
    misc.addEventListener('click', miscHandler)
}

main()
