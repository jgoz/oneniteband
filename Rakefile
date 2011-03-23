task :default => [ :stylesheets ]

desc 'Regenerates all sass templates.'
task :stylesheets do
  system "compass compile --sass-dir stylesheets --css-dir css"
end

desc 'Quantize and compress png images.'
task :png do
  system "pngnq -n 256 -s 1 images/*-o.png"
  system "find images/ -name '*-nq8.png' -print0 | xargs -P1 -0 -n1 pngout"
end
