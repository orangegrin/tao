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
  client.hkeys(key, (err, keys) => {
    keys = keys.sort();
    let data = {}
    if (keys && keys.length >= 2) {
      data['status'] = 1;
      curKey = JSON.parse(keys.pop());
      preKey = JSON.parse(keys.pop());
      client.hmget(key, [curKey, preKey], (err, vals) => {
        data['cur'] = JSON.parse(vals[0]);
        data['pre'] = JSON.parse(vals[1]);
        res.send(data);
      });
    } else {
      data['status'] = 2;
      data['err'] = 'No data obtained';
      res.send(data)
    }

  })
});

module.exports = router;
