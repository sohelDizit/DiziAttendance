    function Toast( id,message) 
    {
        debugger;
        var x = document.getElementById(id);
        x.innerHTML =message;
        x.className = "show";
        setTimeout(function(){ x.className = x.className.replace("show", ""); }, 7000);
    }   


    function ToastWithoutHide( id,message,color) 
    {
        debugger;
        var x = document.getElementById(id);
        if(color!=null)
        {
            x.style.color =color;
        }
        

        x.innerHTML =message;
        x.className = "show";
        // setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
    }   