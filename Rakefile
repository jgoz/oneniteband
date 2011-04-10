task :default => [ :css, :minjs ]

desc 'Regenerates all sass templates.'
task :css do
  system "compass compile --sass-dir stylesheets --css-dir css"
end

desc 'Minify javascript using web-based uglifyjs.'
task :minjs do
  system "curl --data-urlencode js_code@js/photo.js http://marijnhaverbeke.nl/uglifyjs > js/photo.min.js"
end

desc 'Quantize and compress png images.'
task :png do
  system "pngnq -n 256 -s 1 images/*-o.png"
  system "find images/ -name '*-nq8.png' -print0 | xargs -P1 -0 -n1 pngout"
end
