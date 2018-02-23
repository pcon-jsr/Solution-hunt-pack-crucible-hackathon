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

app.use(bodyParser());
app.use(router());
app.use(express.static(__dirname+'/css'));
app.set('view engine', 'pug');
app.set('views', './views');

app.get('/', function(req, res){
  var coll = mongo.collection('challenges');
  coll.find().toArray(function(err, user){
    if(err) console.log("Could not fetch challenge Details");
    else res.render('home', {challenges : user});
  });
});

app.get('/refresh', function(req,res){
  request.get({url:"http://127.0.0.1:5000/refresh"}, function(err, response, body){
    if(err) console.log(err);
    res.redirect('/');
  });

});

app.get('/refresh', function(req, res){
  res.send("in refresh")

});





mongo.connect(mongoUrl, function(){
  console.log('Connected to mongo at: ' + mongoUrl);
  app.listen(port, function(){
    console.log('Server is listening on port: '+port);
  });
});
