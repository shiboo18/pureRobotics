setInterval(function() {
    var myImageElement = document.getElementById('image1');
    myImageElement.src = '/getImage?random=' + Math.random();
}, 500);