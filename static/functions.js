window.onload = function(){
    var size = document.getElementsByTagName('font-size')[0];
    if (localStorage.getItem("fntSz")) {
        document.body.style.setAttribute('font-size', localStorage.getItem("fntSz")+'px');
    }
    else {
        document.body.style.setAttribute('font-size', '12px');
    }
}