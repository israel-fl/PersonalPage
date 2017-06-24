$( document ).ready(function() {
  var $sticky = $('.sticky');
  var $stickyrStopper = $('.sticky-stopper');
  if (!!$sticky.offset()) { // make sure ".sticky" element exists

    var generalSidebarHeight = $sticky.innerHeight();
    var stickyTop = $sticky.offset().top;
    var stickOffset = 0;
    var stickyStopperPosition = $stickyrStopper.offset().top;
    var stopPoint = stickyStopperPosition - generalSidebarHeight - stickOffset;
    var diff = stopPoint + stickOffset;

    $(window).scroll(function(){ // scroll event
      var windowTop = $(window).scrollTop(); // returns number

      if (stopPoint < windowTop) {
          $sticky.css({ position: 'absolute', top: diff });
      } else if (stickyTop < windowTop+stickOffset) {
          $sticky.css({ position: 'fixed', top: stickOffset });
      } else {
          $sticky.css({position: 'absolute', top: 'initial'});
      }
    });

  }
});

$('#comment-form').submit(function( event ) {
    var title = $('#title');
    var comment = $('#comment');

    var titleVal = $('#title').val();
    var commentVal = $('#comment').val();

    var error = $("#message");
    var missing = false;

    // Remove the class so that it can be re-added in case of errors
    title.removeClass("shake");
    comment.removeClass("shake");

    if (titleVal == '') {
        error.html("Title cannot be empty");
        title.addClass('shake');
        title.css('border-color', 'red');
        missing = true;
    }
    if (commentVal == '') {
        error.html("Comment cannot be empty");
        comment.addClass('shake');
        comment.css('border-color', 'red');
        missing = true;
    }
    console.log("stopping");
    if (missing) {
        $("#show-errors").show();
        return false;
    } else {
        return true;
    }
});

window.twttr = (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0],
    t = window.twttr || {};
    if (d.getElementById(id)) return t;
    js = d.createElement(s);
    js.id = id;
    js.src = "https://platform.twitter.com/widgets.js";
    fjs.parentNode.insertBefore(js, fjs);

    t._e = [];
    t.ready = function(f) {
    t._e.push(f);
};

    return t;
}(document, "script", "twitter-wjs"));


(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.9";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
