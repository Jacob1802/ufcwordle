var input = document.querySelector('input');
input.addEventListener('keyup', autocomplete);
let fighternames = [];

fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        if (data.game_over) {
            document.querySelector('input').disabled = true;
        }
        console.log(data.answer);
        console.log(data.fighter_names);
        fighternames = data.fighter_names;
    })
    .catch(error => console.error('Error fetching data:', error));

function autocomplete() {
    let html = '';
    // Check for input value
    if (input.value) {
        // Iterate through list of fighters
        for (let name of fighternames) {
            // Create name 
            if (name.toLowerCase().startsWith(input.value.toLowerCase())) {
                let formattedName = name.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
                html += `<li><button class="auto-comp-button">${formattedName}</button></li>`;
            }
        }
    }
    let list = document.querySelector('#auto-comp');
    // Add names to ul
    list.innerHTML = html;
    // Add li to input when clicked
    list.addEventListener('click', function(e) {
        if (e.target.tagName.toLowerCase() === 'button') {
            input.value = e.target.innerText;
            list.style.display = "none";
        }
    });
}

function modal(){
    // Get the modal
    var modal = document.getElementById("myModal");

    // Get the button that opens the modal
    var btn = document.getElementById("myBtn");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on the button, open the modal
    btn.onclick = function() {
    modal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
    modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
    }
}

modal();