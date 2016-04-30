setInterval(function() {
    var myImageElement = document.getElementById('image1');
    myImageElement.src = '/getImage?random=' + Math.random();
    
    // $('#sonar').html("sonar")
}, 500);

document.onkeydown = checkKey;

var directionalVel = 0
var rotationalVel = 0

function checkKey(e) {

    e = e || window.event;

    if (e.keyCode == '38') {
        // up arrow
        directionalVel += 10
        $.get("/move?num=" + directionalVel);
        // alert("test");
    }
    else if (e.keyCode == '40') {
        // down arrow
        directionalVel -= 10
        $.get("/move?num=" + directionalVel);
    }
    else if (e.keyCode == '37') {
       // left arrow
        rotationalVel -= 10
        $.get("/turn?num=" + rotationalVel);
    }
    else if (e.keyCode == '39') {
       // right arrow
        rotationalVel += 10
        $.get("/turn?num=" + rotationalVel);
    }

}


function killall()
{
    $.get("/cleanslateprotocol");
}

function autoEnable()
{
    $.get("/auto?val=true");
}

function autoDisable()
{
    $.get("/auto?val=false");
}