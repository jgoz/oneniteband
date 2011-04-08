task :default => [ :stylesheets, :modjs ]

desc 'Regenerates all sass templates.'
task :stylesheets do
  system "compass compile --sass-dir stylesheets --css-dir css"
end

desc 'Quantize and compress png images.'
task :png do
  system "pngnq -n 256 -s 1 images/*-o.png"
  system "find images/ -name '*-nq8.png' -print0 | xargs -P1 -0 -n1 pngout"
end

desc 'Minify modified head.js and append to modernizr. Muahahahaaaaa.'
task :modjs do
  system "curl --data-urlencode js_code@js/head.mod.js http://marijnhaverbeke.nl/uglifyjs | cat - js/libs/modernizr.min.js > js/head.mod.min.js"
end
