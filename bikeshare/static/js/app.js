
app.use("/static", express.static('./static/'));


d3.json("/api/prices").then(function(data) {
    console.log(data)
})