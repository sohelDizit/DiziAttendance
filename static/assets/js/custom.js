$(document).ready(function()
 {
  $("button#add_guest").click(function()
  {
    var html='';
    var currentDate=GetCurrerntDate();
    var gustNumber= parseInt($("#numberofGust").val());
    if(gustNumber>0)
    {
        $(".Guest_details").show();
        for (let i = 1; i <= gustNumber; i++) 
        {
            html +='<tr> <td class="tddate">'+currentDate+'</td> <td class="tdname"><input id="text'+i+'" name="text'+i+'" type="text"/></td><td></td>  <td class="tdcheck"><input id="check'+i+'" name="check'+i+'" type="checkbox"/></td> </tr>';
        }
        $('tbody#tblgust').empty();
        $('tbody#tblgust').append(html);
    }
    else
    {
        $(".Guest_details").hide();
    }
 });


$("#numberofGust").blur(function()
{
    var maxvalue= $(this).attr("maxvalue");
    var currentvalue= parseInt($(this).val());
    if(isNaN(currentvalue))
    {
        $(this).val(1);
    }
    else if(maxvalue<currentvalue)
    {
        $(this).val(maxvalue);
    }
    else if (currentvalue<=0)
    {
        $(this).val(1);
    }
});


function GetCurrerntDate()
{
    var d = new Date();
    const options = { month: "short" };

    var month = new Intl.DateTimeFormat("en-US", options).format(d);
    var day =(d.getDate()<10 ? '0' : '') + d.getDate();
    var year= d.getFullYear();
    var hour= (d.getHours()<10 ? '0' : '') +d.getHours();
    var mini= (d.getMinutes()<10 ? '0' : '') +d.getMinutes();
    var sec= (d.getSeconds()<10 ? '0' : '') +d.getSeconds();
    var output =   month+' '+day + ' ' +year+", "+hour + ":" + mini ;
    return output;
}

});