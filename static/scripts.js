// get data from flask app
var f = JSON.parse(document.getElementById("div1").dataset.fighternames);
var fighternames = JSON.parse(f);
var random_fighter = JSON.parse(document.getElementById("div2").dataset.random);
var input = document.querySelector('input');
input.addEventListener('keyup', autocompelte);
console.log(fighternames);
console.log(random_fighter);


function autocompelte()
{
    let html = '';
    // check for input value
    if (input.value) 
    {
        // iter through list of fighters
        for (var names of fighternames) 
        {
            // create name 
            if (names.startsWith(input.value)) 
            {                    
                var name = "";
                for (let i = 0; i < names.length; i++)
                {
                    if (names[i] === " ") {
                        name += names[i];
                        name += names[i + 1].toUpperCase();
                        i++;
                    }
                    else {
                        name += names[i];
                    }
                }
                html += `<li><button class="auto-comp-button">${name.charAt(0).toUpperCase() + name.slice(1)}</button></li>`;
            }
        }
    }
    var list = document.querySelector('#auto-comp');
    // add names to ul
    list.innerHTML = html;
    // add li to input when clicekd 
    list.addEventListener('click', function(e) 
    {
        if (e.target.tagName.toLowerCase() === 'button')
        {
            input.value = e.target.innerHTML;

            list.style.display = "none";
        }
    });
};


function track_guesses(name, input) {
    let guesses = parseInt(document.getElementById("div3").dataset.numguesses);
    // show answer
    if (guesses === 7)
    {
        input.value = name;
        document.form.submit();
    }
}


function set_correct_colour(string, allowance, guess, fighter_stat, i) 
{
    var target = document.querySelectorAll(`.${string}`);
    if (guess === fighter_stat)
    {
        target[i].style.backgroundColor = "rgb(0, 255, 0)";
    }
    // if guess within allowance
    else if (guess < fighter_stat && guess >= (fighter_stat - allowance) || guess > fighter_stat && guess <= (fighter_stat + allowance))
    {
        target[i].style.backgroundColor = "yellow";
    }
}


function check(){
    weight_class = {
        "Flyweight" : 1,
        "Bantamweight" : 2,
        "Featherweight" : 3,
        "Lightweight" : 4,
        "Welterweight" : 5,
        "Middleweight" : 6,
        "LightHeavyweight" : 7,
        "Heavyweight" : 8
    }

    // check guess for hometown and change color
    var row_of_guesses = 0;
    var hometown = document.getElementsByClassName("hometown");
    for (let i = 0; i < hometown.length; i++)
    {
        row_of_guesses++;
        if (hometown[i].innerHTML.trim() === random_fighter.hometown.trim())
        {
            let target = document.querySelectorAll(".hometown");
            target[i].style.backgroundColor = "rgb(0, 255, 0)";
        }
    }

    // check guess for debut and change color
    var debut = document.getElementsByClassName("debut");
    var allowance = 1;
    for (let i = 0; i < row_of_guesses; i++)
    {
        let arr = debut[i].innerHTML.trim().split(",");
        let guess_year = parseInt(arr[arr.length - 1]);

        let farr = random_fighter.debut.trim().split(",");
        let random_fighter_year = parseInt(farr[farr.length - 1]);

        set_correct_colour("debut", allowance, guess_year, random_fighter_year, i);
    }

    // check guess for age and change color
    var age = document.getElementsByClassName("age");
    allowance = 3;
    for (let i = 0; i < row_of_guesses; i++)
    {
        let guess_age = age[i].innerHTML;
        let random_fighter_age = parseInt(random_fighter.age);
        set_correct_colour("age", allowance, guess_age, random_fighter_age, i);
    }
    
    // check guess for weight and change color
    var weight = document.getElementsByClassName("weight");
    allowance = 2;
    for (let i = 0; i < row_of_guesses; i++)
    {
        let guess_weight = weight_class[weight[i].innerHTML.trim()];
        let random_fighter_weight = weight_class[random_fighter.weight.trim()];
        set_correct_colour("weight", allowance, guess_weight, random_fighter_weight, i);
    }   

    // check guess for height and change color
    var height = document.getElementsByClassName("high");
    allowance = 3;

    for (let i = 0; i < row_of_guesses; i++)
    {
        let guess_height = Math.floor(parseFloat(JSON.parse(height[i].dataset.t)));
        let random_fighter_height = parseFloat(random_fighter.height);
        set_correct_colour("height", allowance, guess_height, random_fighter_height, i);
    }

    // check guess for fighter_name and change color
    var fighter_name = document.getElementsByClassName("name");
    for (let i = 0; i < row_of_guesses; i++)
    {
        var target = document.querySelectorAll("tr");
        if (fighter_name[i].innerHTML.toLowerCase().trim() === random_fighter.name.trim())
        {
            target[i + 1].style.backgroundColor = "rgb(0, 255, 0)";
            document.querySelector('input').disabled = true;
        }
    }
    
    // sets colour for wrong guess
    let guesses = parseInt(document.getElementById("div3").dataset.numguesses);
    var t = document.querySelectorAll("td");
    if (guesses === 8){
        for (let i = 41; i < 47; i++) {
            t[i + 1].style.backgroundColor = "rgb(255, 0, 0)";
            document.querySelector('input').disabled = true;
        }
    }
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

document.addEventListener('DOMContentLoaded', track_guesses(random_fighter.name, input));
// set_wrong_colour()
modal();
check();