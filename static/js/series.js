let button = document.querySelector('.show-series-button');
let tableSpace = document.querySelector('.table-place-xy');
let p = document.createElement("p")

function get_stars(){
        return fetch(`/api/series`, {
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((response) => response.json())
}

function get_movie(name){
    return fetch(`/api/series/${name}`, {
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((response) => response.json())
}

function createTable() {
    let table = `<table>
            <thead>
            <th>Character</th>
            </thead>
            <tbody class="row-place"></tbody>
            </table>`
            tableSpace.innerHTML = table
            }

function addRow(data){
    let rowPlace = document.querySelector('.row-place');
    data.forEach((actor) => {
        const htmlTemplate = `<tr>
                <td class="show-movie" id="${actor['character_name']}">${actor['character_name']}</td>
                            </tr>`
        rowPlace.innerHTML += htmlTemplate
    })
}

function showMovie(actor) {
    let btnnn = document.getElementById(actor[0]['character_name'])
    console.log(btnnn.childNodes.length)
    if (btnnn.childNodes.length < 2) {
        console.log(btnnn.parentElement.innerHTML)
        btnnn.append(p)
        btnnn.lastElementChild.innerHTML = actor[0]['name'] +
                     actor[0]['birthday']
    } else {
        btnnn.lastElementChild.remove()
    }
}

button.addEventListener('click', () => {
    createTable()
    get_stars().then(data => {
        addRow(data)
            }).then(() => displayShows())
        })

function displayShows(){
    let btn = document.querySelectorAll('.show-movie')
    btn.forEach((actor) => actor.addEventListener('click', () => {

        get_movie(actor.id).then(data => {
            showMovie(data)
            })
        })
    )}