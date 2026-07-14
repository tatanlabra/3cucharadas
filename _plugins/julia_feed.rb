# frozen_string_literal: true

# jekyll-polyglot narrows site.posts to the active language. This generator
# reads the source posts so the root-level JuliaBloggers feed can stay English.
module JuliaFeed
  class Generator < Jekyll::Generator
    safe true
    priority :lowest

    def generate(site)
      return unless site.active_lang == site.default_lang

      collection = site.collections.fetch("posts")
      site.data["julia_feed_posts"] = post_paths(collection).filter_map do |path|
        document = Jekyll::Document.new(path, :site => site, :collection => collection)
        document.read
        next unless eligible?(document)

        document.data["layout"] = "none"
        rendered_content = document.renderer.run
        url = absolute_url(site, localized_path(site, document))

        {
          "title" => document.data.fetch("title"),
          "url" => url,
          "date" => document.date,
          "description" => document.data.fetch("description", ""),
          "content" => absolutize_urls(rendered_content, site),
        }
      end.sort_by { |post| post.fetch("date") }.reverse
    end

    private

    def post_paths(collection)
      Dir.glob(File.join(collection.directory, "**", "*")).select do |path|
        File.file?(path) && %w[.md .markdown .mkdown].include?(File.extname(path))
      end
    end

    def eligible?(document)
      document.data["lang"] == "en" &&
        document.data["author"] == "clabra" &&
        Array(document.data["tags"]).map { |tag| tag.to_s.downcase }.include?("julia")
    end

    def localized_path(site, document)
      path = document.url
      lang = document.data.fetch("lang", site.default_lang)
      return path if lang == site.default_lang || path.start_with?("/#{lang}/")

      "/#{lang}#{path.start_with?("/") ? path : "/#{path}"}"
    end

    def absolute_url(site, path)
      root = "#{site.config.fetch("url")}#{site.config.fetch("baseurl", "")}".sub(%r{/$}, "")
      "#{root}/#{path.sub(%r{^/}, "")}"
    end

    def absolutize_urls(content, site)
      root = "#{site.config.fetch("url")}#{site.config.fetch("baseurl", "")}".sub(%r{/$}, "")
      content
        .gsub('href="/', "href=\"#{root}/")
        .gsub('src="/', "src=\"#{root}/")
        .gsub('srcset="/', "srcset=\"#{root}/")
        .gsub("]]>", "]]]]><![CDATA[>")
    end
  end
end
