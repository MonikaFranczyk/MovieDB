let name = document.querySelector('.name')
let genre = document.querySelector('.genre')
let table = document.querySelector('.actors-genre')


function getData(name, genre) {
    console.log(name, genre)
    return fetch(`/api/actors/?name=${name}&genre=${genre}`)
        .then((response) => response.json())
}

function makeTable(data) {
    data.forEach((actor) => {
        const htmlTemplate = `<tr><td>${actor['name']}</td></tr>`
        table.innerHTML += htmlTemplate
    })
}

name.addEventListener('input', () => {
    table.innerHTML = ''
        getData(name.value, genre.value)
        .then(data => {
            makeTable(data)
        })
})

genre.addEventListener('change', () => {
    table.innerHTML = ''
    console.log(name.value)
    // console.log(genre.value)
    getData(name.value, genre.value)
        .then(data => {
            makeTable(data)
        })
})
