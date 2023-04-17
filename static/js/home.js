$(function() {

    window.addEventListener('click', function(event) {
      if (event.target.className == 'ui-corner-all') {
        var autoCompleteValue = $(event.target).text();
        document.getElementById("searchBar").value = autoCompleteValue;
        document.getElementById("cityForm").requestSubmit();
        console.log(event.target.id + 'was clicked');
      }
    });
  });


