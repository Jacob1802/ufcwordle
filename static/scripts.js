// document.addEventListener("DOMContentLoaded", function(event) { 

var f = JSON.parse(document.getElementById("div1").dataset.fighters);
var fighters = JSON.parse(f);
console.log(fighters);
var random_fighter = JSON.parse(document.getElementById("div2").dataset.random);
console.log(random_fighter);
var input = document.querySelector('input');
input.addEventListener('keyup', function(event) 
{
    document.querySelector('ul').style.display = "block";
    let html = '';
    if (input.value) 
    {
        for (var names of fighters) 
        {
            if (names.startsWith(input.value)) 
            {                    
                var word = "";
                for (let i = 0; i < names.length; i++)
                {
                    if (names[i] === " ") {
                        word += names[i];
                        word += names[i + 1].toUpperCase();
                        i++;
                    }
                    else {
                        word += names[i];
                    }
                }
                html += `<li><button onclick="return false">${word.charAt(0).toUpperCase() + word.slice(1)}</button></li>`;
            }
        }
    }
    document.querySelector('ul').innerHTML = html;
});


var list = document.querySelector('ul');
list.addEventListener('click', function(e) 
{
    if (e.target.tagName.toLowerCase() === 'button')
    {
        input.value = e.target.innerHTML;

        document.querySelector('ul').style.display = "none";
    }
});


function set_colours(string, allowance, guess, fighter_stat, i) 
{
    var target = document.querySelectorAll(`.${string}`);
    if (guess === fighter_stat)
    {
        target[i].style.backgroundColor = "rgb(0, 255, 0)";
    }
    // if guess no more than allowance lower
    else if (guess < fighter_stat && guess >= (fighter_stat - allowance))
    {
        target[i].style.backgroundColor = "yellow";
    }
    // if guess no more than allowance higher
    else if (guess > fighter_stat && guess <= (fighter_stat + allowance))   
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

    var hometown = document.getElementsByClassName("hometown");
    for (let i = 0; i < hometown.length; i++)
    {
        if (hometown[i].innerHTML.trim() === random_fighter.hometown.trim())
        {
            let target = document.querySelectorAll(".hometown");
            target[i].style.backgroundColor = "rgb(0, 255, 0)";
        }
    }

    var debut = document.getElementsByClassName("debut");
    var allowance = 1;
    for (let i = 0; i < debut.length; i++)
    {
        let arr = debut[i].innerHTML.trim().split(",");
        let guess_year = parseInt(arr[arr.length - 1]);

        let farr = random_fighter.debut.trim().split(",");
        let random_fighter_year = parseInt(farr[farr.length - 1]);

        set_colours("debut", allowance, guess_year, random_fighter_year, i);
    }

    
    var age = document.getElementsByClassName("age");
    allowance = 3;
    for (let i = 0; i < age.length; i++)
    {
        let guess_age = age[i].innerHTML;
        let random_fighter_age = parseInt(random_fighter.age);
        set_colours("age", allowance, guess_age, random_fighter_age, i);
    }
    

    var weight = document.getElementsByClassName("weight");
    allowance = 2;
    for (let i = 0; i < weight.length; i++)
    {
        let guess_weight = weight_class[weight[i].innerHTML.trim()];
        let random_fighter_weight = weight_class[random_fighter.weight.trim()];
        set_colours("weight", allowance, guess_weight, random_fighter_weight, i);
    }   

    var height = document.getElementsByClassName("height");
    allowance = 3;
    for (let i = 0; i < height.length; i++)
    {
        let arr = height[i].innerHTML.trim().split("'");
        let guess_height = Math.round(parseFloat(arr[0] + "." + arr[1]) * 12);
        let random_fighter_height = parseFloat(random_fighter.height);
        console.log(guess_height, random_fighter_height);
        set_colours("height", allowance, guess_height, random_fighter_height, i);
    }

    var fighter_name = document.getElementsByClassName("name");
    for (let i = 0; i < fighter_name.length; i++)
    {
        if (fighter_name[i].innerHTML.toLowerCase().trim() === random_fighter.name.trim())
        {
            let target = document.querySelectorAll("tr");
            target[i + 1].style.backgroundColor = "rgb(0, 255, 0)";
        }
    }
}

check()