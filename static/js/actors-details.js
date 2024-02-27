let p = document.createElement("p")

function getShowsForActors(id){

    if (document.getElementById(id).parentElement.childNodes.length < 4){
        fetch('/api/actors-details/'+id).then(response => response.json()).then(function(data){
        document.getElementById(id).parentElement.append(p)
        document.getElementById(id).parentElement.lastElementChild.innerHTML = data['show']})
    } else {
        document.getElementById(id).parentElement.lastElementChild.remove()
    }
}
