require "yaml"
require "ftools"

module Jekyll
  class VersionedFile < StaticFile
    def initialize(site, base, dir, name, ver)
      super(site, base, dir, name)

      @ver = ver
    end

    alias src_destination destination

    def destination(dest)
      ext = File.extname(@name)
      File.join(dest, @dir, "#{File.basename(@name, ext)}.#{@ver}#{ext}")
    end

    def write(dest)
      dest_path = destination(dest)
      src_path = src_destination(dest)

      File.delete(src_path) if File.exist? src_path

      return false if File.exist? dest_path and !modified?
      @@mtimes[path] = mtime

      FileUtils.mkdir_p(File.dirname(dest_path))
      FileUtils.cp(path, dest_path)

      true
    end
  end

  class VersionedFilesGenerator < Generator
    safe true
    
    def generate(site)
      versions = YAML::load_file(File.join(site.source, "_versions.yml"))

      versions.each do |file, opts|
        site.exclude << File.basename(file)
      end

      versions.each do |file, opts|
        dir = File.dirname(file)
        ver = opts['ver']

        site.static_files << VersionedFile.new(site, site.source, dir, File.basename(file), ver)
      end
    end
  end

  class VersionedTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super

      @path = text.strip

      site_root = File.join(File.dirname(__FILE__), "..")
      @versions = YAML::load_file(File.join(site_root, "_versions.yml"))
    end

    def render(context)
      version = @versions[@path]['ver'] or 1
      ext = File.extname(@path)

      File.basename(@path, ext) + "." + version.to_s + ext
    end
  end
end

Liquid::Template.register_tag('versioned', Jekyll::VersionedTag)
