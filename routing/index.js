process.env.UV_THREADPOOL_SIZE = Math.ceil(require('os').cpus().length * 1.5)

var express = require('express'),
    OSRM = require('osrm'),
    path = require('path'),
    sqlite = require('spatialite'),
    fs = require('fs'),
    d3 = require('d3')

var db = new sqlite.Database(':memory:')

var initSatements = [
    "SELECT InitSpatialMetaData()",
    "CREATE TABLE kitas (id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, kita_id integer)",
    "SELECT AddGeometryColumn('kitas', 'the_geom', 4326, 'POINT', 'XY')",
    "SELECT CreateSpatialIndex(`the_geom`, `kitas`)"
], iS = 0;

db.spatialite(function(err) {
    if(err){console.log(err);}
    init();
})

function init(){
    db.run(initSatements[iS], [], function(err, row){
        iS++;
        if(iS < initSatements.length){
            init()
        }else{
            importData()
        }
    })
}

function importData(){
    var stmt = db.prepare("INSERT INTO kitas (kita_id, the_geom) VALUES (?,PointFromText(?, 4326))"),
        kitas = d3.csvParse(fs.readFileSync('./data/kitas.csv','utf8'))

    kitas.forEach((s,i)=>{
        var params = [parseInt(s.id), "POINT("+parseFloat(s.lat)+" "+parseFloat(s.lon)+")"]
        stmt.run(params)
    })

    stmt.finalize()

    console.log('all done');
}

var app = express(),
    osrm_car = new OSRM(path.join(__dirname,"./data/car/berlin-latest.osrm")),
   //osrm_foot = new OSRM(path.join(__dirname,"./data/foot/berlin-latest.osrm")),
    osrm_bicycle = new OSRM(path.join(__dirname,"./data/bicycle/berlin-latest.osrm"))

var jobs = [], jobI = 0, inProgress = false

app.all('/*', function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  next();
});


app.get('/kitas', function(req, res) {
    if (!req.query.lat || !req.query.lon) {
        return res.json({"error":"invalid lat lon query"})
    }

    jobs.push({
        lat:parseFloat(req.query.lat),
        lon:parseFloat(req.query.lon),
        res:res,
        rows:null
    })

    job_id = jobs.length-1

    db.all("SELECT kita_id, Distance(PointFromText(?, 4326), the_geom, 1) AS dist, Y(the_geom) AS lat, X(the_geom) AS lon FROM kitas ORDER BY dist", ["POINT("+req.query.lat+" "+req.query.lon+")"], function(err, rows){
        if(err){
            return res.json(err)
        }
        
        jobs[job_id].rows = rows

        processJobs();
    });
})

function processJobs(){
    if(!inProgress && jobs.length >= 1){
        inProgress = true
        jobI = 0
        processRows()
    }
}

function processRows(){
    if(jobs[0].rows[jobI].dist < 2000){
        multiModalRoute({
            coordinates: [[jobs[0].lon, jobs[0].lat],[jobs[0].rows[jobI].lat, jobs[0].rows[jobI].lon]],
            geometries:'geojson',
            alternateRoute: false
        }, function(r){
            jobs[0].rows[jobI]["routes"] = r
            nextRow()
        })
    }else{
        nextRow()
    }
}

function nextRow(){
    jobI++
    if(jobI<jobs[0].rows.length){
        processRows()
    }else{
        jobs[0].res.json(jobs[0].rows)
        jobs.splice(0,1)
        inProgress = false
        processJobs()
    }
}

// Accepts a query like:
// http://localhost:8888/route?start=13.414307,52.521835&end=13.402290,52.523728&modal=bicycle
app.get('/route', function(req, res) {
    if (!req.query.start || !req.query.end) {
        return res.json({"error":"invalid start and end query"});
    }else if(!req.query.modal){
        return res.json({"error":"invalid modal (multi, car, foot, bicycle)"});
    }
    var coordinates = [];
    var start = req.query.start.split(',');
    coordinates.push([+start[0],+start[1]]);
    var end = req.query.end.split(',');
    coordinates.push([+end[0],+end[1]]);
    var query = {
        modal: req.query.modal,
        coordinates: coordinates,
        //steps: true,
        geometries:'geojson',
        alternateRoute: req.query.alternatives !== 'false'
    };

    if(req.query.modal == 'multi'){
        multiModalRoute(query, function(r){
            return res.json(r)
        })
    }else{
        singleModalRoute(query, function(r){
            return res.json(r)
        })
    }
})

function multiModalRoute(query, callback){
    var r = {car:null,foot:null,bicycle:null}
    osrm_car.route(query, function(err, result) {
        if (err) return res.json({"error":err.message})
        r.car = result

        osrm_foot.route(query, function(err, result) {
            if (err) return res.json({"error":err.message})
            r.foot = result

            osrm_bicycle.route(query, function(err, result) {
                if (err) return res.json({"error":err.message})
                r.bicycle = result
                
                callback(r)
            })
        })
    })
}

function singleModalRoute(query, callback){
    switch(query.modal){
        case 'car':
            osrm_car.route(query, function(err, result) {
                if (err) return res.json({"error":err.message})
                callback(result);
            })
        break;
        case 'foot':
            osrm_foot.route(query, function(err, result) {
                if (err) return res.json({"error":err.message})
                callback(result);
            })
        break;
        case 'bicycle':
            osrm_bicycle.route(query, function(err, result) {
                if (err) return res.json({"error":err.message})
                callback(result);
            })
        break;
    }
}

console.log('Listening on port: ' + 1717);
app.listen(1717);