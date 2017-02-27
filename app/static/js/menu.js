
$(document).ready(function()
{
  $('.child_menu li').click(function ()
    {
        var idDiv = $(this).attr('rel');
        if(typeof(idDiv) == "undefined")
            return ;
       var pages = $(".menu-view-money");
       for(var i = 0 ; i < pages.length ;i++)
        {
          if(pages[i].id != idDiv )
            $(pages[i]).attr('style', "display:none");
          else
            $(pages[i]).attr('style', "display:inline");
        }

        var menu = $(".child_menu li");
        for(var i = 0 ; i < menu.length ;i++)
         {
           if(menu[i] != this )
           {
              $(menu[i]).attr('style', "cursor:pointer");
              $(menu[i]).attr('class', "");
           }
           else
           {
             $(this).attr('style', "cursor:pointer");
             $(this).attr('class', "active");
           }

         }

    });
     $('#_home').click();

});
