var express = require('express');
var router = express.Router();
var redis = require("redis"),
  client = redis.createClient();

/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/stats', function (req, res, next) {
  let key = req.query.key;
  client.hvals(key, (err, vals) => {
    let results = {}
    results['cur'] = JSON.parse(vals.pop());
    results['pre'] = JSON.parse(vals.pop());
    res.send(results)
  })
});

module.exports = router;
