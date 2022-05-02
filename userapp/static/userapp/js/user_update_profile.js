// ENABLE NOTIFICATIONS
$('#notification_toggle').on('change', function() {
  var listHeight = $('.judgments-settings .list').outerHeight();
  var headerHeight = $('.judgments-settings .settings-legend').outerHeight();

  if ($(this).is(':checked')) {
    $('.judgments-settings').removeClass('disabled').stop().animate({ height: listHeight + headerHeight + 1 }, 500);
  } else {
    $('.judgments-settings').addClass('disabled').stop().animate({ height: 0 }, 500);
  }
});