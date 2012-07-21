require 'sample'

require 'test/unit'

class TestSample < Test::Unit::TestCase
  def test_sample
    assert_equal "<h1>Test</h1>\n", Sample.convert('# Test')
  end
end
