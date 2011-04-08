/**
  Head JS    The only script in your <HEAD>
  Copyright  Tero Piirainen (tipiirai)
  License    MIT / http://bit.ly/mit-license
  Version    0.9
  
  http://headjs.com
*/
(function(doc) {

  var html = doc.documentElement,
      conf = { screens: [320, 480, 640, 985, 1024, 1220] },
      klass = [];

  function each(arr, fn) {  
    for (var i = 0; i < arr.length; i++) {
      fn.call(arr, arr[i], i);
    }
  }

  // screen resolution: w-100, lt-480, lt-1024 ...
  function screenSize() {
    var w = window.outerWidth || html.clientWidth;

    // remove earlier widths
    html.className = html.className.replace(/ (w|lt|gt)-\d+/g, "");

    // add new ones
    klass.push("w-" + Math.round(w / 100) * 100);

    each(conf.screens, function(width) {
      if (w <= width) { klass.push("lt-" + width); } 
      if (w > width) { klass.push("gt-" + width); } 
    });

    html.className += ' ' + klass.join(' ');
    klass = [];
  }

  screenSize();    
  window.onresize = screenSize;
})(document);

