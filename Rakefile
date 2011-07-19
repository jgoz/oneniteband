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
    next if path =~ /\w+\.\d+\.js/

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
  require 'net/sftp'
  
  BUCKET = 'www.oneniteband.com'
  NOGZIP_EXTS = ['.gif', '.jpg', '.jpeg', '.png', '.ico', '.woff', '.pdf']

  AWS::S3::Base.establish_connection!(
    :access_key_id => ENV['AMAZON_ACCESS_KEY_ID'],
    :secret_access_key => ENV['AMAZON_SECRET_ACCESS_KEY'],
    :use_ssl => true
  )

  versioned_files = get_all_versions().to_a.map do |el|
    dir = File.dirname(el[0])
    ext = File.extname(el[0])
    File.join(dir, "#{File.basename(el[0], ext)}.#{el[1]['ver']}#{ext}")
  end
  deployed = []

  oldwd = Dir.getwd

  Dir.chdir('_site')
  Dir.glob(File.join('**', '*')) do |path|
    next if File.directory? File.expand_path(path)

    maxage = versioned_files.include?(path) ? 315360000 : 259200
    compress = !NOGZIP_EXTS.include?(File.extname(path))

    puts "%s -> %d%s" % [path, maxage, (compress ? ' gzip' : '')]

    file = compress ? get_compressed(path) : File.open(path)

    headers = {
      :access => :public_read,
      'Cache-Control' => "max-age=#{maxage}"
    }

    headers.merge!('Content-Encoding' => 'gzip') if compress

    AWS::S3::S3Object.store(path, file, BUCKET, headers)

    deployed << path
  end

  REMOTE_PATH_ROOT = '/home/public_html/oneniteband.com'

  Net::SFTP.start(ENV['STATIC_HOST'], ENV['STATIC_USER'], :password => ENV['STATIC_PASSWORD']) do |sftp|

    rm_r(sftp, REMOTE_PATH_ROOT)

    Dir.glob(File.join('**', '*')) do |path|

      remote_path = File.join(REMOTE_PATH_ROOT, path)

      if File.directory? File.expand_path(path)
        sftp.mkdir! remote_path
      else
        sftp.upload!(path, remote_path)
      end

      puts "%s -> %s" % [path, remote_path]
    end
  end

  Dir.chdir(oldwd)

  bucket = AWS::S3::Bucket.find(BUCKET)
  all_keys = bucket.objects.map{|obj| obj.key}

  (all_keys - deployed).each do |key|
    puts "x %s" % key
    AWS::S3::S3Object.delete(key, BUCKET)
  end
end

def rm_r(sftp, path)
  sftp.dir.foreach(path) do |entry|
    next if entry.name == '.' or entry.name == '..'

    full_path = File.join(path, entry.name)

    if entry.directory?
      rm_r(sftp, full_path)
      sftp.rmdir! full_path
    else
      sftp.remove! full_path
    end
  end
end

def get_compressed(path)
  require 'stringio'
  require 'zlib'

  strio = StringIO.open('', 'r+')
  gz = Zlib::GzipWriter.new(strio)
  gz.write(File.open(path).read)
  gz.close

  strio.string
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
