d3.json("/api/weather").then(function(data)
{
    
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

