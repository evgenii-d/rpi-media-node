function detailsHandler(event) {
    const input = event.target

    fetchWrapper('node-details/name',
        { method: 'POST', body: input.value },
        {
            default: () => { input.value = input.dataset.name },
            success: () => { input.dataset.name = input.value },
            error: () => { input.value = input.dataset.name }
        }
    )
}

function machineControlHandler(event) {
    const container = event.currentTarget
    const command = event.target.dataset.cmd

    if (!command) return
    toggleFieldset(container, true)
    fetchWrapper('/machine-control', { method: 'POST', body: command },
        {
            response: () => { toggleFieldset(container, false, 1000) },
            error: () => { toggleFieldset(container, false, 1000) }
        }
    )
}

function toggleApp(container, element) {
    const name = element.dataset.name
    switch (name) {
        case 'Media Player':
            url = '/media-player/state'
            break
        case 'Web Browser':
            url = '/web-browser/state'
            break
        case 'Web Server':
            url = '/web-server/state'
            break
    }

    toggleFieldset(container, true)
    fetchWrapper(url,
        { method: 'POST', body: element.checked ? 'on' : 'off' },
        {
            response: () => { toggleFieldset(container, false, 1000) },
            error: () => {
                toggleFieldset(container, false, 1000)
                element.checked = !element.checked
            }
        }
    )
}

function appsHandler(event) {
    const container = event.currentTarget
    const element = event.target

    switch (element.nodeName) {
        case 'BUTTON':
            url = '/media-player/state'
            openURL(element.dataset.url)
            break
        case 'INPUT':
            toggleApp(container, element)
            break
    }
}

function main() {
    const details = document.getElementById('details')
    details.addEventListener('change', detailsHandler)

    const machineControl = document.getElementById('machine-control')
    machineControl.addEventListener('click', machineControlHandler)

    const apps = document.getElementById('apps')
    apps.addEventListener('click', appsHandler)

    const appsList = [
        { name: 'Media Player', page: '/media-control', api: '/media-player' },
        { name: 'Web Browser', page: '/browser-control', api: '/web-browser' },
        { name: 'Web Server', page: '/server-control', api: '/web-server' }
    ]
    const table = document.createElement('table')
    const tbody = document.createElement('tbody')

    appsList.forEach(app => {
        fetch(`${app.api}/state`)
            .then((response) => response.json())
            .then((state) => {
                template = `
                    <tr>
                        <td>
                            <label>
                                <input type="checkbox" 
                                data-state="${state}"
                                data-name="${app.name}"
                                ${state === 'on' ? 'checked=true' : ''}
                                class=thorn-kit>${app.name}
                            </label>
                        </td>
                        <td><button class=thorn-kit data-url="${app.page}">&#9881;</button></td>
                    </tr>`
                tbody.insertAdjacentHTML('beforeend', template)
            })
    })

    table.append(tbody)
    apps.append(table)

    fetch('/node-details/hostname')
        .then((response) => response.json())
        .then((hostname) => {
            const element = document.querySelector('#details h1')
            element.textContent = hostname
        })

    fetch('/node-details/name')
        .then((response) => response.json())
        .then((name) => {
            const nodeName = document.querySelector('#details input')
            nodeName.dataset.name = name
            nodeName.value = name
        })
}

main()
