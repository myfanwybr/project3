
//app.use("/static", express.static('./static/'));


d3.json("/api/pricing").then(function(data) {
    
    var data=data
    console.log(data)
    data.forEach(function(aliens){
        var row=tbody.append("tr")
    
        //select objects using . Entries
        Object.entries(aliens).forEach(function([key, value]){
            var cell=row.append("td")
            cell.text(value)
        })
    })
})

var tbody= d3.select("tbody")

