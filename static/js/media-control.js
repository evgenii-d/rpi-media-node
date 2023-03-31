function updateUsedSpace() {
    const div = document.getElementById('used-space')

    fetch('/media-files/size').then(r => r.json())
        .then(size => {
            div.textContent = `Used space: ${size} Mb`
        }).catch((error) => {
            div.textContent = 'Used space: —'
            console.error(error)
        })
}

function playerControlHandler(event) {
    const container = event.currentTarget
    const command = event.target.dataset.cmd
    const input = container.querySelector('input[type=text]')
    let data

    if (!command) return

    switch (command) {
        case 'volume':
            data = { command, value: event.target.value }
            fetchWrapper('/media-player/settings',
                { method: 'POST', body: { volume: +event.target.value } }
            )
            break
        case 'goto':
            if (input.value === '') {
                alert('Set video ID')
                console.info('Empty input')
                return
            }
            data = { command, value: input.value }
            break
        default:
            data = { command }
            break
    }
    toggleFieldset(container, true)
    fetchWrapper('/media-player/control', { method: 'POST', body: data },
        {
            response: () => { toggleFieldset(container, false, 1000) },
            error: () => { toggleFieldset(container, false, 1000) }
        }
    )
}

function playerSettingsHandler(event) {
    const container = event.currentTarget
    const element = event.target
    let data

    if (element.tagName !== 'INPUT') return
    toggleFieldset(container, true)

    switch (element.type) {
        case 'radio':
            data = { module: element.value }
            break
        case 'checkbox':
            data = { playback: [] }
            checkboxes = container.querySelectorAll('input[type=checkbox]')

            checkboxes.forEach(checkbox => {
                if (checkbox.checked) data.playback.push(checkbox.value)
            })
            break
    }

    fetchWrapper('/media-player/settings', { method: 'POST', body: data },
        {
            response: () => { toggleFieldset(container, false, 1000) },
            error: () => { toggleFieldset(container, false, 1000) }
        }
    )
}

function uploadMediaHandler(event) {
    const mediaControl = document.getElementById('media-control')
    const controlPlayList = document.getElementById('playlist-control')
    const container = event.currentTarget
    const element = event.target
    const formData = new FormData()
    const files = container.querySelector('input[type=file]').files

    if (element.tagName !== 'BUTTON') return

    for (let i = 0; i < files.length; i++) {
        formData.append('media', files[i])
    }

    if (files.length === 0) { alert('Select files'); return }

    toggleFieldset([container, mediaControl, controlPlayList], true)
    fetchWrapper('/media-files/add',
        { method: 'POST', body: formData },
        {
            response: () => {
                toggleFieldset([container, mediaControl, controlPlayList], false)
                updateUsedSpace()
                loadMediaFiles()
            },
            error: () => {
                toggleFieldset([container, mediaControl, controlPlayList], false)
            }
        }
    )
}

async function fetchPlaylists() {
    try {
        const response = await fetch('/media-files/playlists')
        return await response.json()
    } catch (error) { console.error(error) }
}

async function fetchDefaultPlaylist() {
    try {
        const response = await fetch('/media-files/playlists/default')
        return await response.json()
    } catch (error) { console.error(error) }
}

async function fetchPlaylistContent(id) {
    try {
        const response = await fetch(`/media-files/playlists/content/${id}`)
        return await response.json()
    } catch (error) { console.error(error) }
}

async function fetchMediaFiles() {
    try {
        const response = await fetch('/media-files')
        return await response.json()
    } catch (error) { console.error(error) }
}

async function loadMediaFiles() {
    const table = document.querySelector('#media-control table tbody')
    const files = await fetchMediaFiles()

    removeChildElements(table)
    if (files.length === 0) {
        const tr = '<tr><td colspan=2 class=no-files>No files</td></tr>'
        table.parentNode.classList.remove('hover')
        table.insertAdjacentHTML('beforeend', tr)
        return
    }

    files.forEach(file => {
        const tr = `
            <tr>
                <td><input type=checkbox class=thorn-kit value="${file}"></td>
                <td><a href="static/media/${file}" download>${file}</a></td>
            </tr>`
        table.insertAdjacentHTML('beforeend', tr)
    })
}

function orderHandler(event) {
    const element = event.target
    const table = event.target.parentNode.parentNode.parentNode

    if (element.type !== 'submit') return

    const prevNode = element.parentNode.parentNode.previousElementSibling
    const nextNode = element.parentNode.parentNode.nextElementSibling
    const currentNode = element.parentNode.parentNode

    if (element.hasAttribute('data-up') && prevNode) {
        table.insertBefore(currentNode, prevNode)
    }

    if (element.hasAttribute('data-down') && nextNode) {
        table.insertBefore(nextNode, currentNode)
    }
}

async function loadPlaylistContent(id) {
    const table = document.querySelector('#playlist-control table tbody')
    const content = await fetchPlaylistContent(id)

    removeChildElements(table)
    if (content.length === 0) {
        const tr = '<tr><td colspan=4 class=no-files>No files</td></tr>'
        table.parentNode.classList.remove('hover')
        table.insertAdjacentHTML('beforeend', tr)
        return
    }

    content.forEach((file, i) => {
        const tr = `
            <tr>
                <td><input type=checkbox class=thorn-kit value="${file}"></td>
                <td>${file}</td>
                <td data-number>${i + 1}</td>
                <td data-order>
                    <button class=thorn-kit data-up>&uarr;</button>
                    <button class=thorn-kit data-down>&darr;</button>
                </td>
            </tr>`

        table.insertAdjacentHTML('beforeend', tr)
        table.lastElementChild.querySelector('[data-order]')
            .addEventListener('click', orderHandler)
    })
}

async function updatePlaylistsList() {
    const playlists = await fetchPlaylists()
    const defaultPlaylist = await fetchDefaultPlaylist()
    const playlistsList = document.getElementById('playlists-list')

    removeChildElements(playlistsList)

    playlists.forEach(item => {
        const option = document.createElement('option')
        option.value = item
        option.textContent = item
        defaultPlaylist === item ? option.selected = true : ''
        playlistsList.append(option)
    })

    if (+playlistsList.value > 0) {
        loadPlaylistContent(+playlistsList.value)
    }
}

function mediaControlHandler(event) {
    const element = event.target
    const command = element.dataset.cmd
    const uploadMedia = document.getElementById('upload-media')
    const container = document.getElementById('media-control')
    const playlistControl = document.getElementById('playlist-control')
    let checkboxes
    let apiURL
    let init

    if (!command) return

    switch (command) {
        case 'delete':
            checkboxes = container.querySelectorAll('table tbody input[type=checkbox]:checked')
            if (checkboxes.length === 0) { alert('Select files'); return }

            apiURL = 'media-files/delete'
            init = { method: 'DELETE', body: [] }
            checkboxes.forEach(checkbox => { init.body.push(checkbox.value) })
            break
        case 'toggle':
            checkboxes = container.querySelectorAll('table tbody input[type=checkbox]')
            checkboxes.forEach(checkbox => (checkbox.checked = element.checked))
            return
        case 'create':
            checkboxes = container.querySelectorAll('table tbody input[type=checkbox]:checked')
            if (checkboxes.length === 0) { alert('Select files'); return }

            apiURL = '/media-files/playlists/add'
            init = { method: 'POST', body: [] }
            checkboxes.forEach(checkbox => { init.body.push(checkbox.value) })
            break
    }

    toggleFieldset([container, uploadMedia, playlistControl], true)
    fetchWrapper(apiURL, init,
        {
            response: () => {
                toggleFieldset([container, uploadMedia, playlistControl], false, 1000)
                loadMediaFiles()
                updateUsedSpace()
                updatePlaylistsList()
            },
            default: () => {
                alert('Exceed max number of playlists')
            },
            error: () => {
                toggleFieldset([container, uploadMedia, playlistControl], false, 1000)
            }
        }
    )
}

async function showDefaultPlaylist() {
    const defaultPlaylist = document.getElementById('default-playlist')
    const id = await fetchDefaultPlaylist()
    defaultPlaylist.textContent = id
}

function playlistControlHandler(event) {
    const element = event.target
    const command = element.dataset.cmd
    const playlistsFieldset = document.getElementById('playlist-control')
    const playlistsList = document.getElementById('playlists-list')
    const filesTable = document.querySelector('#playlist-control tbody')
    const files = filesTable.querySelectorAll('input[type=checkbox]')
    const selectedFiles = filesTable.querySelectorAll('input[type=checkbox]:checked')
    const updatedList = []

    if (!command) return
    if (+playlistsList.value <= 0 && command !== 'toggle') {
        alert('Create a Playlist'); return
    }

    switch (command) {
        case 'remove':
            if (selectedFiles.length === 0) { alert('Select files'); return }
            selectedFiles.forEach(file => { file.parentNode.parentNode.remove() })
            break
        case 'update':
            toggleFieldset(playlistsFieldset, true)
            files.forEach(file => { updatedList.push(file.value) })

            fetch(`/media-files/playlists/content/${+playlistsList.value}`, {
                method: 'PUT',
                headers: { 'content-type': 'application/json;charset=utf-8' },
                body: JSON.stringify(updatedList)
            }).then(async response => {
                console.info(await response.json())
                toggleFieldset(playlistsFieldset, false, 1000)
            }).catch(() => { toggleFieldset(playlistsFieldset, false, 1000) })
            break
        case 'default':
            fetch('/media-files/playlists/default', {
                method: 'POST',
                headers: { 'content-type': 'application/json;charset=utf-8' },
                body: +playlistsList.value
            }).then(async response => {
                console.info(await response.json())
                showDefaultPlaylist()
            })
            break
        case 'delete':
            fetch('/media-files/playlists/delete', {
                method: 'DELETE',
                headers: { 'content-type': 'application/json;charset=utf-8' },
                body: JSON.stringify([+playlistsList.value])
            }).then(async response => {
                if (response.status === 200) {
                    playlistsList.remove(playlistsList.selectedIndex)
                    if (+playlistsList.value > 0) {
                        updatePlaylistsList()
                    } else {
                        removeChildElements(filesTable)
                        const tr = '<tr><td colspan=4 class=no-files>No files</td></tr>'
                        filesTable.parentNode.classList.remove('hover')
                        filesTable.insertAdjacentHTML('beforeend', tr)
                    }
                }
                console.info(await response.json())
            })
            break
    }
}

function main() {
    const playerControl = document.getElementById('player-control')
    playerControl.addEventListener('click', playerControlHandler)

    const gotoInput = playerControl.querySelector('input[type=text]')
    gotoInput.addEventListener('input', onlyDigits)

    const playerSettings = document.getElementById('player-settings')
    playerSettings.addEventListener('click', playerSettingsHandler)

    const uploadMedia = document.getElementById('upload-media')
    uploadMedia.addEventListener('click', uploadMediaHandler)

    const mediaControl = document.getElementById('media-control')
    mediaControl.addEventListener('click', mediaControlHandler)

    const playlistControl = document.getElementById('playlist-control')
    playlistControl.addEventListener('click', playlistControlHandler)

    const playlistsList = document.getElementById('playlists-list')
    playlistsList.addEventListener('change', event => {
        const playlist_id = +event.target.value
        loadPlaylistContent(playlist_id)
    })


    fetch('/media-player/settings')
        .then((response) => response.json())
        .then((data) => {
            const volume = document.querySelector('#player-control input[type=range]')
            volume.value = data.volume

            const module = document.querySelector(`#player-settings input[type=radio][value=${data.module}]`)
            module.checked = true

            const playbackElements = document.querySelectorAll('#player-settings input[type=checkbox]')
            playbackElements.forEach(element => {
                data.playback.forEach(option => {
                    if (element.value === option) element.checked = true
                })
            })
        })

    loadMediaFiles()
    updateUsedSpace()
    showDefaultPlaylist()
    updatePlaylistsList()
}

main()
