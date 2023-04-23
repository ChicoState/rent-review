function toggleStarRating(rating, input_id) {
    var input_e = document.getElementById(input_id);
    input_e.value = rating;
    const input_div = String(input_id) + '_div';
    var spans = document.getElementById(input_div).getElementsByTagName("li");
    var uncheck_all = false;
    var span_rating = spans[(spans.length-rating)].getElementsByTagName("i")[0];
    if(span_rating.classList.contains("checked") ){
        if(rating === spans.length){
            uncheck_all = true;
            input_e.value = 0;
        }
        else if(spans[(spans.length-(rating+1))].getElementsByTagName("i")[0].classList.length === 2){
            uncheck_all = true;
            input_e.value = 0;
        }
    }
    for(var a = spans.length -1; a >= (0); a--) {
        var is = spans[a].getElementsByTagName("i")[0];
        is.classList.remove("checked");
    }
    if(!uncheck_all){
        for(var a = spans.length -1; a >= (spans.length-rating); a--) {
            spans[a].getElementsByTagName("i")[0].classList.add("checked");
        }
    }
  }
  
  function hasClass(element, className) {
    return (' ' + element.className + ' ').indexOf(' ' + className+ ' ') > -1;
}