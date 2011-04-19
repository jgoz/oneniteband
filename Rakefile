task :default => [ :css, :minjs ]

desc 'Regenerates all sass templates.'
task :css do
  system "compass compile --sass-dir _stylesheets --css-dir css --output-style compressed"
end

desc 'Minify javascript using web-based uglifyjs.'
task :minjs do
  min_dir = 'js'
  unless File.exists? min_dir then Dir.mkdir(min_dir) end

  Dir.glob(File.join('js', '*.js')) do |path|
    key = path
    file = File.basename(path, ".js") + "." + get_version('min', key).to_s + ".js"
    out_path = File.join(min_dir, file)

    system "curl --data-urlencode js_code@#{path} http://marijnhaverbeke.nl/uglifyjs > #{out_path}"
  end
end

desc 'Quantize and compress png images.'
task :png do
  system "pngnq -n 256 -s 1 images/*-o.png"
  system "find images/ -name '*-nq8.png' -print0 | xargs -P1 -0 -n1 pngout"
end

desc 'Deploy files to S3'
task :deploy => [:css, :minjs] do
  require 'aws/s3'
  
  BUCKET = 'oneniteband.com'

  AWS::S3::Base.establish_connection!(
    :access_key_id => ENV['AMAZON_ACCESS_KEY_ID'],
    :secret_access_key => ENV['AMAZON_SECRET_ACCESS_KEY']
  )

  versioned_files = get_all_versions().keys
  deployed = []

  oldwd = Dir.getwd
  Dir.chdir('_site')
  Dir.glob(File.join('**', '*')) do |path|
    next if File.directory? File.expand_path(path)

    maxage = versioned_files.include?(path) ? 315360000 : 259200

    puts "%s -> %d" % [path, maxage]

    AWS::S3::S3Object.store(
      path, File.open(path), BUCKET,
      :access => :public_read,
      'Cache-Control' => "max-age=#{maxage}"
    )

    deployed << path
  end
  Dir.chdir(oldwd)

  bucket = AWS::S3::Bucket.find(BUCKET)
  all_keys = bucket.objects.map{|obj| obj.key}

  (all_keys - deployed).each do |key|
    puts "x %s" % key
    AWS::S3::S3Object.delete(key, BUCKET)
  end
end

def get_version(on, path)
  get_versions(on)[path]['ver']
end

def get_versions(on)
  get_all_versions().delete_if{|file, opts| opts['gen'] and opts['gen'] != on}
end

def get_all_versions()
  require "yaml"

  YAML::load_file("_versions.yml")
end
