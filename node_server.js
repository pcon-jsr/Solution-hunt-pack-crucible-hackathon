var express = require('express');
var app = express();
var path=require('path');
var fs=require('fs');
var expressSession = require('express-session');
var mongoUrl = 'mongodb://localhost:27017';
var MongoStore = require('connect-mongo')(expressSession);
var mongo = require('./mongo');
var port = 1337;
var bodyParser=require('body-parser');
var router=require('router');
var request = require('request');

app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());
app.use(router());
app.use(express.static(__dirname+'/css'));
app.use(express.static(__dirname+'/dist'));
app.set('view engine', 'pug');
app.set('views', './views');

app.get('/', function(req, res){
  var coll = mongo.collection('challenges');
  coll.find().toArray(function(err, user){
    if(err) console.log("Could not fetch challenge Details");
    else res.render('home', {challenges : user});
  });
});

app.post("/keywords", function(req, res) {
  var _id = req.body.challenge;
  var coll = mongo.collection('challenges');
  coll.findOne({"_id" : _id}, function(err, challenge){
    if(err) console.log(err);
    else {
      request({method : "POST", url : "http://127.0.0.1:5000/keywords", json : {'content' : challenge["content"] , 'title' : challenge["title"]} }, function(err, response, body)
      {
        if(err) console.log(err);
        else
        {
          var keywords = body.split("||")
          var top_keywords = keywords[0].split(",,")
          var other_keywords = keywords[1].split(",,")
          res.render('keywords', {challenge_title : challenge["title"] , keywords : top_keywords, other_keywords : other_keywords});
        }
      });
    }
  });
});

app.post('/finetune', function(req, res){
  var keywords = req.body.keywords;
  var challenge_title = req.body.challenge_title;
  res.render('finetune', {keywords : keywords , challenge_title : challenge_title } );
});

app.post('/final', function(req, res){
  console.log(req.body);
  var keywords = req.body.keywords;
  var keyword_scores = {};
  var body = req.body;
  for (var i in keywords)
  {
    var z = keywords[i]+"_val"
    keyword_scores[keywords[i]] = parseInt(body[z]);
    console.log(z);
    console.log(body[z]);
  }
  res.send(keyword_scores);
});

app.get('/refresh', function(req,res){
  request.get({url:"http://127.0.0.1:5000/refresh"}, function(err, response, body){
    if(err) console.log(err);
    res.redirect('/');
  });

});

mongo.connect(mongoUrl, function(){
  console.log('Connected to mongo at: ' + mongoUrl);
  app.listen(port, function(){
    console.log('Server is listening on port: '+port);
  });
});
