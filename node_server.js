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
var sortJsonArray = require('sort-json-array');
var util = require('util');
var moment = require('moment');
var error_file = fs.createWriteStream(__dirname + '/error.log', {flags : 'a'});

console.log_error = function(d) { //
  var time = moment();
  var time_format = time.format('YYYY-MM-DD HH:mm:ss Z');
  error_file.write(time_format + "\n" + util.format(d) + '\n');
};

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
  try
  {
    var coll = mongo.collection('challenges');
    coll.find().toArray(function(err, challenges){
      if(err) console.log("Could not fetch challenge Details");
      else res.render('home', {challenges : challenges});
    });
  }
  catch(e)
  {
    console.log_error(e);
    res.render('error', {error_msg : "Error loading the challenges."});
  }
});

/*
function insert_keywords(_id)
{
  var coll = mongo.collection('challenges');
  var ret = "abc";
  coll.findOne({"_id" : _id}, function(err, challenge){
    if(err) console.log(err);
    else {
      request({method : "POST", url : "http://127.0.0.1:5000/keywords", json : {'content' : challenge["content"] , 'title' : challenge["title"]} }, function(err, response, body)
      {
        if(err) console.log(err);
        else
        {
          var keywords = body.split(",,")
          ret = keywords;
          var coll1 = mongo.collection(_id);
          var s = 5 * keywords.length;
          for (var i in keywords)
          {
            coll1.insertOne({keyword : keywords[i] , score : s}, function(err, res){
              if(err)
              {
                console.log_error(err);
                res.render('error', {error_msg : "Error loading the keywords."});
              }
            });
            s = s-5;
          }

        }
      });
    }
  });
  return ret;
}


app.post("/keywords", function(req,res){
  try
  {
    var _id = req.body.challenge;
    var coll = mongo.collection(_id);
    coll.find().sort({score:-1}).toArray(function(err, keywords){
      if(err)
      {
        console.log_error(err);
        res.render('error', {error_msg : "Error loading the challenges."});
      }

    });
    res.send("Done");
  }
  catch(e)
  {

  }
});
*/

app.post("/keywords", function(req, res) {
  try
  {
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
            res.render('keywords', {challenge_title : challenge["title"] , keywords : top_keywords, other_keywords : other_keywords, challenge_url :challenge["url"], html : challenge["html"]});
          }
        });
      }
    });
  }
  catch(e)
  {
    console.log_error(e);
    res.render('error', {error_msg : "Error loading the Keywords."})
  }
});




app.post('/finetune', function(req, res){
  try
  {
  var keywords = req.body.keywords;
  var challenge_title = req.body.challenge_title;
  //console.log(keywords);
  if(typeof(keywords)=="string" || keywords.length < 2)
  {
    res.render('error', {error_msg : "Please select two or more Keywords."});
  }
  res.render('finetune1', {keywords : keywords , challenge_title : challenge_title } );
  }
  catch(e)
  {
    console.log_error(e);
    res.render('error', {error_msg : "Error loading the Keywords."})
  }

});

app.post('/final', function(req, res){
  try
  {
    var keywords = req.body.keywords_list;
    var challenge_title = req.body.challenge_title;
    var engine = req.body.engine;
    var time_limit = parseInt(req.body.time_slider);
    if(engine==undefined)
    {
        engine = 'off';
    }
    request( {method : 'POST', url : "http://127.0.0.1:5000/final", json : {'keywords' : keywords, 'time_limit' : time_limit, 'engine' : engine} }, function(err, response, body){
      try
      {
        ret = fs.readFileSync('temp/'+body+'.json');


        ret_json = JSON.parse(ret);
        ret_json_sorted = ret_json.sort(function(a,b){
          return parseInt(b['score']) - parseInt(a['score'])
        });
        fs.unlinkSync('temp/'+body+'.json');
        //console.log(body);
        //console.log(ret_json);
        //console.log(ret_json_sorted);
        res.render('final', {results : ret_json_sorted, challenge_title : challenge_title });
      }
      catch(e)
      {
        console.log_error(e);
        res.render('error', {error_msg : "Error loading the results."});
      }
    });
  }
  catch(e)
  {
    console.log_error(e);
    res.render('error', {error_msg : "Error loading the results."});
  }

});


/*app.post('/final', function(req, res){
  try
  {
    var keywords = req.body.keywords;
    var challenge_title = req.body.challenge_title;
    var keyword_scores = {};
    var body = req.body;
    var time_limit = parseInt(req.body.time_slider);
    for (var i in keywords)
    {
      var z = keywords[i]+"_val"
      keyword_scores[keywords[i]] = parseInt(body[z]);
    }
    request( {method : 'POST', url : "http://127.0.0.1:5000/final", json : {'keyword_scores' : keyword_scores, 'time_limit' : time_limit} }, function(err, response, body){
      try
      {
        ret = fs.readFileSync('temp/'+body+'.json');


        ret_json = JSON.parse(ret);
        ret_json_sorted = ret_json.sort(function(a,b){
          return parseInt(b['score']) - parseInt(a['score'])
        });
        fs.unlinkSync('temp/'+body+'.json');
        //console.log(ret_json);
        //console.log(ret_json_sorted);
        res.render('final', {results : ret_json_sorted, challenge_title : challenge_title });
      }
      catch(e)
      {
        console.log_error(e);
        res.render('error', {error_msg : "Error loading the results."});
      }
    });
  }
  catch(e)
  {
    console.log_error(e);
    res.render('error', {error_msg : "Error loading the results."});
  }

});*/


/*
app.get('/refresh', function(req,res){
  try
 {
  request.get({url:"http://127.0.0.1:5000/refresh"}, function(err, response, body){
    if(err)
    {
      console.log_error(err);
      res.render('error', {error_msg : "Error loading the challenges."});
    }
    var coll = mongo.collection("challenges");
    coll.find({}).toArray(function(err,challenges){

      for (var i in challenges)
      {
        var _id = challenges[i]['_id'];
        console.log(_id);
        request({method : "POST", url : "http://127.0.0.1:5000/keywords", json : {'content' : challenges[i]["content"] , 'title' : challenges[i]["title"]} }, function(err, response, body)
        {
          if(err)
          {
            console.log_error(err);
            res.render('error', {error_msg : "Error loading the challenges."});
          }
          else
          {
            var keywords = body.split(",,")
            var coll1 = mongo.collection(String(_id));
            var s = 5 * keywords.length;
            for (var i in keywords)
            {
              coll1.insertOne({keyword : keywords[i] , score : s}, function(err, res){
                if(err)
                {
                  console.log_error(err);
                  res.render('error', {error_msg : "Error loading the keywords."});
                }
              });
              s = s-5;
            }
          }
        });

      }


    });
    res.redirect('/');
  });
  }
  catch(e)
  {
    console.log_error(e);
    res.render('error', {error_msg : ""});
  }

});
*/



app.get('/refresh', function(req,res){
  try
 {
  request.get({url:"http://127.0.0.1:5000/refresh"}, function(err, response, body){
    if(err)
    {
      console.log_error(err);
      res.render('error', {error_msg : "Error loading the challenges."});
    }

    res.redirect('/');
  });
  }
  catch(e)
  {
    console.log_error(e);
    res.render('error', {error_msg : ""});
  }

});

app.get('*', function(req, res){
  if (req.accepts('html')) {
    res.render('error',{error_msg : "The Page you are requesting for is not available."})
  }
});


mongo.connect(mongoUrl, function(){
  console.log('Connected to mongo at: ' + mongoUrl);
  app.listen(port, function(){
    console.log('Server is listening on port: '+port);
  });
});
