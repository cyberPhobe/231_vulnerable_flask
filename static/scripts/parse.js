function parseOut(outputS) {
    var out = document.getElementById("shellOut");
    var shell = document.getElementById("shell");
    if (outputS !== "empty"){
        outputS = outputS.replace('b&#39;', '');
        outputS = outputS.replace('&#39;', '');
        out.innerText = outputS;
        out.style.display = 'block';
        shell.style.display = 'block';
        console.log(outputS);
    }
    else{
        out.style.display = 'none';
        shell.style.display = 'none';
    }
}

function parseOut2(outputS) {
    var out = document.getElementById("llehsOut");
    var shell = document.getElementById("llehs");
    if (outputS !== "empty"){
        outputS = outputS.replace('b&#39;', '');
        outputS = outputS.replace('&#39;', '');
        out.innerText = outputS;
        out.style.display = 'block';
        shell.style.display = 'block';
        console.log(outputS);
    }
    else{
        out.style.display = 'block';
        shell.style.display = 'block';
    }
}