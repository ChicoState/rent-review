// function hideMenu(){
//     let menu = document.getElementById('sidebarMenu');
//     document.onclick = function(e){
//     if(!menu.contains(e.target) && e.target.className != "header"){
//         menu.style.display = 'none';
//     }
//     };
//   };

    $('.openSidebarMenu').click(function() { //button click class name is myDiv
    e.stopPropagation();
   })
  
   function hideMenu(){
    let menu = document.getElementById('sidebarMenu');
    let openMenuButton = document.getElementById("openSidebarMenu");
    document.onclick = function(e){
            if(!menu.contains(e.target) && e.target.className != "header"){
                document.getElementById("sidebarMenu").style.transform = "translateX(-250px)";
                openMenuButton.checked = false;
            }
            if(openMenuButton.contains(e.target)){
                if(!openMenuButton.checked){
                    document.getElementById("sidebarMenu").style.transform = "translateX(0px)";
                    openMenuButton.checked = true;
                }else{
                    document.getElementById("sidebarMenu").style.transform = "translateX(-250px)";
                    openMenuButton.checked = false;
                }
            }
            }; 
    }
  