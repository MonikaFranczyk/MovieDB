let buttons = document.querySelectorAll('.show-episodes')
let placeForTable = document.querySelectorAll('.place-for-table')
let clickedElement = null

function get_data(season) {
    return fetch(`show-episodes/${season}`, {
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((response) => response.json())
}

function makeTable(episodes){
    let headers = `<th>Title</th><th>Overview</th>`
    placeForTable[0].innerHTML = headers
    episodes.forEach((episode) => {

        const htmlTemplate = `
            <tr>
                <td>${episode['title']}</td>
                <td>${episode['overview']}</td>
            </tr>
            `
            placeForTable[0].innerHTML += htmlTemplate
        console.log(placeForTable[0])
    })
}

buttons.forEach(button => button.addEventListener('click', (e) => {
    if (placeForTable[0].hasChildNodes() && e.target.id == clickedElement) {
        placeForTable[0].innerHTML = ''
    } else {
        clickedElement = e.target.id
        placeForTable[0].innerHTML = ''
        get_data(e.target.id).then(episodes => {
        makeTable(episodes)
    }
        )}
    })
)

