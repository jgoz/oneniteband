require "yaml"

module Jekyll
  class VersionedTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super

      @path = text.strip

      site_root = File.join(File.dirname(__FILE__), "..")
      @versions = YAML::load_file(File.join(site_root, "_versions.yml"))
    end

    def render(context)
      version = @versions[@path] or 1
      ext = File.extname(@path)

      File.basename(@path, ext) + "." + version.to_s + ext
    end
  end
end

Liquid::Template.register_tag('versioned', Jekyll::VersionedTag)
