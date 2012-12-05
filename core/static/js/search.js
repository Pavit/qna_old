$("#search").autocomplete({
  maxLength: 7,
  source: function(request, response) {
    var searchtext = request.term;
    $.ajax({
      url: "/search/?searchtext=" + searchtext,
      type: "GET",
      success: function(data) {
        var extrastuff = [{
          question: "<b>View all search results</b>",
          url: "/search_results/?searchtext=" + searchtext
        },
        {
          question: "Submit Question",
          url: "/submit/"
        }];
        data.slice(0,5);
        data.splice(6, 0, extrastuff[0]);
        data.splice(7, 0, extrastuff[1]);
        response($.map(data, function(item) {
          
          return {
            label: item.question,
            value: item.url
          }
        }));
      },
      data: request.term,
      dataType: "json"
    });
  },
  select: function(event, ui) {

    console.log(ui.item);
    $('.previous_question').fadeOut(300);
    $('#current_question').delay(100).fadeOut(300);
    if (ui.item.label == "View all search results") {
      $("#search_results").html('&nbsp').load(ui.item.value);
        $(this).val('');
  return false;
    }
    else{
      if(ui.item.label == "Submit Question") {
        window.open(ui.item.value);
          $(this).val('');
  return false;
      }
      else{
    $('#current_question').html('&nbsp;').load(ui.item.value);
    $('#current_question').delay(100).fadeIn(300);
    $('.previous_question').delay(400).fadeIn(300);
      $(this).val('');
  return false;
  };
  };
  $(this).val('');
  return false;
  }
});
