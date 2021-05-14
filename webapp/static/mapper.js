$( document ).ready(function() {
    var agency = {{ agency | tojson }};
    console.log(agency);
});