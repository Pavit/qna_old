$("#search").autocomplete({
  source: function(request, response) {
    $.ajax({
      url: "{% url search %}?searchtext=" + request.term,
      type: "GET",
      success: function(data) {
        console.log(data);
        response($.map(data, function(item) {
          return {
            label: item.fields.question,
            value: item.pk
          }
        }));
      },
      data: request.term,
      dataType: "json"
    });
  },
  select: function(event, ui) {
    console.log(ui);
    var url = "/current_question/" + ui.item.value;
    $('.previous_question').fadeOut(300);
    $('#current_question').fadeOut(300);
    $('#current_question').html('&nbsp;').load(url);
    $('#current_question').fadeIn(300);
    $('.previous_question').fadeIn(300);

  }
});