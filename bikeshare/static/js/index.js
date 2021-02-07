console.log("for index.html");

d3.json("/api/pricing").then(function(data) {
    console.log(data);
})
