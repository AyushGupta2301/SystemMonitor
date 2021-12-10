var http = require('http')
var url = require('url')
var util = require('util')
var strdec = require('string_decoder').StringDecoder
var mongo = require('mongodb')
var mongoclient = mongo.MongoClient
let URI = "mongodb://ayush:ayush2301@localhost:27017"


function store_log(req, res) {
    let decoder = new strdec('utf-8');
    let buffer = "";
    req.on("data", function (chunk) {
        buffer += decoder.write(chunk);
    })
    req.on("end", function () {
        buffer += decoder.end();
        var logobj = JSON.parse(buffer);
        mongoclient.connect(URI, function (err, database) {
            if (err) throw err;
            let dbobj = database.db("LogRecords");
            console.log("connected to database for Storage");
            dbobj.collection("SysLogs").insertOne(logobj,function(err,resp){
                if(err) throw err;
                console.log(resp);
                res.writeHead(200, "OK", { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
                res.write(JSON.stringify(buffer));
                res.end();
            })
        })

    })
}

function store_logpkt(req, res) {
    let decoder = new strdec('utf-8');
    let buffer = "";
    req.on("data", function (chunk) {
        buffer += decoder.write(chunk);
    })
    req.on("end", function () {
        buffer += decoder.end();
        var logobj = JSON.parse(buffer);
        mongoclient.connect(URI, function (err, database) {
            if (err) throw err;
            let dbobj = database.db("LogRecords");
            console.log("connected to database for Storage");
            dbobj.collection("PktLogs").insertOne(logobj,function(err,resp){
                if(err) throw err;
                console.log(resp);
                res.writeHead(200, "OK", { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
                res.write(buffer);
                res.end();
            })
        })

    })
}

//Fetch function is not used right now but I planned to create a Frontend to access the logs
function fetch_log(req, res) {
        res.writeHead(200, "OK", { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
        res.write("fetch Endpoint Hit");
        res.end();
    }

http.createServer(function (req, res) {
    if (req.method == "OPTIONS") {
        //For preflight if created frontend
        res.writeHead(200, "OK", { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*' });
        res.end();
    }
    else if(req.method == "GET") {
        //For checking connectivity
        res.write("Endpoint hit, Request acknowlegded \n");
        res.end();
    }
    else {
        let pathobj = url.parse(req.url, true);
        // store_log, fetch_log are functions defined to access MongoDB server for storage and retrieval
        switch(pathobj.pathname) {
            case "/store": 
                store_log(req,res);
                break;
            case "/fetch":
                fetch_log(req,res);
                break;
            case "/storepkt":
                store_logpkt(req,res);
                break;
        }
    }
}).listen(8081, "192.168.1.10");
