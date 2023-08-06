$(function () {

  $(".js-create-host").click(function () {
    $.ajax({
      url: '/ace/host/create/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-host").modal("show");
      },
      success: function (data) {
        $("#modal-host .modal-content").html(data.html_form);
      }
    });
  });

});


