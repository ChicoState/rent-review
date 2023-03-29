function hideMenu(){
    let menu = document.getElementById('sidebarMenu');
    
    let menuActivationButton = document.getElementsByClassName('openSidebarMenu');
    document.onclick = function(e){
    if(!menu.contains(e.target) && !menuActivationButton.contains(e.target)){
        menu.style.display = 'none';
    }
    };
  };