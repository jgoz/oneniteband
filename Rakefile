def get_version(path)
  require "yaml"

  YAML::load_file("_versions.yml")[path] or 1
end

task :default => [ :css, :minjs ]

desc 'Regenerates all sass templates.'
task :css do
  system "compass compile --sass-dir stylesheets --css-dir css --output-style compressed"
end

desc 'Minify javascript using web-based uglifyjs.'
task :minjs do
  min_dir = File.join('js', 'min')
  unless File.exists? min_dir then Dir.mkdir(min_dir) end

  Dir.glob(File.join('js', '*.js')) do |path|
    file = File.basename(path, ".js") + "." + get_version(path).to_s + ".js"
    out_path = File.join(min_dir, file)

    system "curl --data-urlencode js_code@#{path} http://marijnhaverbeke.nl/uglifyjs > #{out_path}"
  end
end

desc 'Quantize and compress png images.'
task :png do
  system "pngnq -n 256 -s 1 images/*-o.png"
  system "find images/ -name '*-nq8.png' -print0 | xargs -P1 -0 -n1 pngout"
end
