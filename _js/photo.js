(function($, window, document) {
  var _selectors = {
    o: "#overlay",
    v: "#photo-viewer",
    n: "a.next",
    p: "a.prev",
    c: "a.close",
    h: "invisible"
  };

  function buildViewerDom() {
    $("body").prepend("<div id='overlay'><div id='photo-viewer'><h3>Title</h3><img src='' alt='' title='Click to close'><a class='next'>Next</a><a class='prev'>Previous</a><a class='close'>Close</a></div></div>");
  }

  function toggleNextAndPrev($link) {
    $(_selectors.n, _selectors.v).toggleClass(_selectors.h, $link.next("a").size() === 0);
    $(_selectors.p, _selectors.v).toggleClass(_selectors.h, $link.prev("a").size() === 0);
  }

  function redirectToPhoto() {
    window.location = $(this).attr("src");
  }

  function loadPhoto($link) {
    var $viewer = $(_selectors.v),
        viewHeight = window.innerHeight || document.documentElement.clientHeight;

    $("h3", $viewer).html($("img", $link).attr("alt"));
    $("img", $viewer).css("max-height", viewHeight - 110);
    $("img", $viewer).attr("src", $link.attr("href"));
    $viewer.data("link", $link);

    toggleNextAndPrev($link);
  }

  function showViewer() {
    loadPhoto($(this));
    $(_selectors.o).show();

    return false;
  }

  function hideViewer() {
    $(_selectors.o).hide();
  }

  function changePhoto($link) {
    if ($link.size() > 0) {
      loadPhoto($link);
    }
  }

  function nextPhoto() {
    changePhoto($(_selectors.v).data("link").next("a"));
  }

  function prevPhoto() {
    changePhoto($(_selectors.v).data("link").prev("a"));
  }

  function init($pane) {
    buildViewerDom();

    var $viewer = $(_selectors.v),
        isMobile = $("html").hasClass("lt-640");

    $("img", $viewer).click(isMobile ? redirectToPhoto : hideViewer);
    $(_selectors.c, $viewer).click(hideViewer);
    $(_selectors.n, $viewer).click(nextPhoto);
    $(_selectors.p, $viewer).click(prevPhoto);
    $("a", $pane).click(showViewer);

    if (isMobile) {
      $(_selectors.o).css("padding-top", $pane.offset().top - 20);
    }
  }

  $(function() {
    init($(".photo-pane"));
  });
})(jQuery, window, document);
