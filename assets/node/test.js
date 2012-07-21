var assert = require('assert')
  , sample = require('./sample')

assert.equal('<h1>Test</h1>', sample.convert('# Test'))
