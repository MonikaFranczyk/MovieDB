let button = document.querySelector('.show-stars-button');
let tableSpace = document.querySelector('.table-place');
let movieSpace = document.querySelector('.modal-body');

function get_stars(){
        return fetch(`/api/stars`, {
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((response) => response.json())
}

function get_movie(id){
    return fetch(`/api/stars/${id}`, {
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((response) => response.json())
}

function createTable() {
    let table = `<table>
            <thead>
            <th>Name</th>
            <th>Birthday</th>
            <th>Count</th>
            </thead>
            <tbody class="row-place"></tbody>
            </table>`
            tableSpace.innerHTML = table
            }

function addRow(data){
    let rowPlace = document.querySelector('.row-place');
    data.forEach((actor) => {
        const htmlTemplate = `<tr>
                <td class="show-movie" id="${actor['id']}" data-toggle="modal" data-target="#testStar">${actor['name']}</td>
                            <td>${actor['birthday']}</td>
                            <td>${actor['count']}</td></tr>`
        rowPlace.innerHTML += htmlTemplate
    })
}

function showMovie(actor) {
    console.log(actor[0]['string_agg'])
    let htmlMovie = `<p>${actor[0]['string_agg']}</p>`
    movieSpace.innerHTML += htmlMovie
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
        movieSpace.innerHTML = ''
        get_movie(actor.id).then(data => {
            showMovie(data)
            })
        })
    )}


