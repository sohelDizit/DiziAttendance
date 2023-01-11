    function Toast( id,message) 
    {
        var x = document.getElementById(id);
        x.innerHTML =message;
        x.className = "show";
        setTimeout(function(){ x.className = x.className.replace("show", ""); }, 10000);
    }   
