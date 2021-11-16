var http = require('http')
var url = require('url')
var util = require('util')
var strdec = require('string_decoder').StringDecoder
var mongo = require('mongodb')
var mongoclient = mongo.MongoClient
let URI = "mongodb+srv://admin:1357@cluster0.qbbwc.mongodb.net/Parking?retryWrites=true&w=majority"

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
            // console.log("log recorded");
        })

    })
        // res.writeHead(200, "OK", { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
        // res.write(JSON.stringify(buffer));
        // res.end();
}


function fetch_log(req, res) {
    let decoder = new strdec('utf-8');
    let buffer = "";
    req.on("data", function (chunk) {
        buffer += decoder.write(chunk);
    })
    req.on("end", function () {
        buffer += decoder.end();
        var carobj = JSON.parse(buffer);
        mongoclient.connect(URI, function (err, database) {
            if (err) throw err;
            let dbobj = database.db("Parking");
            console.log("connected to database for deletion");
            var query = {carreg : carobj.carreg}
            dbobj.collection("Cars").deleteOne(query,function(err,resp){
                if(err) throw err;
                console.log(resp);
            })
            logobj = carobj;
            logobj.reqtype = "Exit";
            dbobj.collection("log").insertOne(logobj,function(err,resp){
                if(err) throw err;
                console.log("log recorded");
            })
        })
        res.writeHead(200, "OK", { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
        res.write(JSON.stringify(buffer));
        res.end();
    })
}

http.createServer(function (req, res) {
    if (req.method == "OPTIONS") {
        res.writeHead(200, "OK", { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*', 'Access-Control-Allow-Methods': '*' });
        res.end();
    }
    else {
        let pathobj = url.parse(req.url, true);
        switch(pathobj.pathname) {
            case "/store":
                store_log(req,res);
                break;
            case "/fetch":
                fetch_log(req,res);
                break;
        }
    }
}).listen(8081, "localhost");
