var md = require('markdown')

exports.convert = function(str) {
  return md.parse(str)
}
