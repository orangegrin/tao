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
    let data = {}
    if (vals && vals.length >= 2) {
      data['status'] = 1;
      data['cur'] = JSON.parse(vals.pop());
      data['pre'] = JSON.parse(vals.pop());
    } else {
      data['status'] = 2;
      data['err'] = 'No data obtained';
    }
    res.send(data)
  })
});

module.exports = router;
