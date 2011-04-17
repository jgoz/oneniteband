task :default => [ :css, :minjs, :versions ]

desc 'Regenerates all sass templates.'
task :css do
  system "compass compile --sass-dir _stylesheets --css-dir css --output-style compressed"

  update_versions
end

desc 'Minify javascript using web-based uglifyjs.'
task :minjs do
  min_dir = 'js'
  unless File.exists? min_dir then Dir.mkdir(min_dir) end

  Dir.glob(File.join('_js', '*.js')) do |path|
    key = path[1..-1]
    file = File.basename(path, ".js") + "." + get_version('min', key).to_s + ".js"
    out_path = File.join(min_dir, file)

    system "curl --data-urlencode js_code@#{path} http://marijnhaverbeke.nl/uglifyjs > #{out_path}"
  end
end

desc 'Add version numbers to versioned files'
task :versions do
  update_versions
end

desc 'Quantize and compress png images.'
task :png do
  system "pngnq -n 256 -s 1 images/*-o.png"
  system "find images/ -name '*-nq8.png' -print0 | xargs -P1 -0 -n1 pngout"
end

def get_versions(on)
  require "yaml"

  YAML::load_file("_versions.yml").delete_if{|file, opts| opts['gen'] and opts['gen'] != on}
end

def get_version(on, path)
  get_versions(on)[path]['ver']
end

def update_versions()
  require "ftools"

  get_versions('copy').each do |file, opts|
    ver = opts['ver']
    dir = File.dirname(file)
    ext = File.extname(file)
    pre = ext == '.js' ? '_' : ''

    unless File.exists? dir then Dir.mkdir(dir) end
    File.copy(pre + file, File.join(dir, File.basename(file, ext) + '.' + ver.to_s + ext))
  end
end
