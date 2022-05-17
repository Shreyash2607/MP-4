$(document).ready(function(){

    

    $("#cmd").click(function(){
        var doc = newjsPDF();
        

        doc.save("sample.pdf");
    });
});

function demoFromHTML() {
    var specialElementHandler = {
        "#editor":function(element,renderer){
            return true;
        }
    };

    var indentor = document.getElementById('select-indenter').value
    var load =  document.getElementById('select-load').value
    var caliberation = document.getElementById('caliberation').value
    var hbvalue = document.getElementById('select-hb').value
    var lowerRange = document.getElementById('range-from').value
    var higherRange = document.getElementById('range-to').value
    var filename = document.getElementById('file-name').value
    var jobname = document.getElementById('job-description').value
    var custname = document.getElementById('cust-name').value
    var custadd = document.getElementById('cust-address').value
    var res = document.getElementById('result').value
    var testedby = document.getElementById('tested-by').value
    var witnessedby = document.getElementById('witnessed-by').value
    var aprovedby = document.getElementById('aproved-by').value
    
    var doc = new jsPDF();
    //document.getElementById("indentor").innerHTML = 3;
    doc.setFontSize(20);
    doc.setFont("times");
    doc.text(40, 20, 'Job Name : ' + jobname);
    doc.text(40, 80, 'Tested By ' +testedby);
    doc.text(40, 100, 'Aprooved By : ' + aprovedby);
    doc.text(40, 120, 'Witnessed By : ' + witnessedby);
    doc.text(40, 140, 'Customer Name : ' + custname);
    doc.text(40, 160, 'Customer Address : ' + custadd);
    doc.text(40, 180, 'HB Value : ' + hbvalue);
    doc.text(40, 200, 'Diamete of Indentor : ' + indentor);
    doc.text(40, 220, 'Calculated HB Value : ' + res);
    doc.fromHTML($("#target").html(),15,15,{
        "width":170,
        "elementHandlers":specialElementHandler
    });

    doc.save('Test.pdf');
}