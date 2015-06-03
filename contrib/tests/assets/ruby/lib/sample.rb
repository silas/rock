require 'kramdown'

module Sample
  def self.convert(text)
    Kramdown::Document.new(text, { :auto_ids => false }).to_html
  end
end
