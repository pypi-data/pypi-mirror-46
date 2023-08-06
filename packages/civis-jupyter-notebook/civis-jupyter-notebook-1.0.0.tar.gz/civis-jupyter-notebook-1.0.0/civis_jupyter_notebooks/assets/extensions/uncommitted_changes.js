define(['jquery'], function($) {
  var uncommitted_changes = function() {
    var settings = {
      url: '/git/uncommitted_changes',
      type: 'GET',
      contentType: 'applicaton/json',
      success: function(data) {
        if (data.hasOwnProperty('dirty') && data.dirty) {
          $("#uncommitted_changes").css('display', 'inline-block');
          $("#no_changes").css('display', 'none');
        } else {
          $("#no_changes").css('display', 'inline-block');
          $("#uncommitted_changes").css('display', 'none');
        }

        window.setTimeout(uncommitted_changes, 3000);
      },
      error: function() {
        $("#no_changes").css('display', 'none');
        $("#uncommitted_changes").css('display', 'none');
      }
    }

    $.ajax(settings)
  }

  var _on_click = function() {
    $("#terminal > button").click();
  }

  function _on_load() {
    var uncommittedChangesBox = '<div id="uncommitted_changes" title="Open terminal to commit" class="notification_widget btn btn-xs navbar-btn" style="display: none"><i class="fa fa-circle"></i><span> Uncommitted Changes </span></div>';
    $("#notification_trusted").before(uncommittedChangesBox);
    $("#uncommitted_changes").on("click", _on_click);

    var noChangesBox = '<div id="no_changes" class="navbar-btn btn btn-xs" style="display: none"><span> Nothing to Commit </span></div>';
    $("#uncommitted_changes").before(noChangesBox);

    uncommitted_changes();
  }

  return {load_ipython_extension: _on_load };
})
