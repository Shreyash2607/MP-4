const menuButton = document.getElementsByClassName('menu-button')[0];
const menu = document.getElementById('menu');

menuButton.addEventListener("click", function () {
    menu.classList.toggle("show");
    menuButton.classList.toggle("show");
});

const menuItems = document.getElementsByClassName("menu-item");
console.log('items', menuItems)

for (item of menuItems) {
    console.log('item', item)
    item.addEventListener("click", function (e) {

        const clickedMenuItem = e.target.closest('.menu-item')
        console.log('Clicked Menu Item', clickedMenuItem)
        document.getElementById('current-menu').innerHTML = clickedMenuItem.getAttribute('title');

        //if menu-item clicked is already selected : Do nothing
        // if (clickedMenuItem.contains('selected')) return;

        // Remove selected from all other menu items
        Array.from(menuItems).forEach(mitem => {
            mitem.classList.remove('selected')
        });

        //add selected to current menu Item
        clickedMenuItem.classList.add('selected');

        //Hide Divs all target divs
        const menuTargets = document.getElementsByClassName(`menu-target`);
        Array.from(menuTargets).forEach(menuTaget => menuTaget.classList.add('hide'));

        //Display target div for current menu item
        const itemVal = clickedMenuItem.getAttribute('menu-item');
        const showTargets = document.getElementsByClassName(`menu${itemVal}`);
        console.log('Item Target', showTargets)
        Array.from(showTargets).forEach(classItme => classItme.classList.remove('hide'));

    });
}
// Simulate Click on Home to load Test Panel
document.querySelector('[menu-item="0"]').click();

document.getElementById("button-video").addEventListener("click", ()=>{eel.start_video()}, false);

async function getResults(event) {
    console.log('Result')
    event.preventDefault()
    var indentor = document.getElementById('select-indenter').value
    console.log(indentor)
    var load =  document.getElementById('select-load').value
    console.log(load)
    var caliberation = document.getElementById('caliberation').value
    console.log(caliberation)
    var hbvalue = document.getElementById('select-hb').value
    console.log(hbvalue)
    var lowerRange = document.getElementById('range-from').value
    var higherRange = document.getElementById('range-to').value
    var output = ' '    

    // // single(caliberation,output,diameter_of_indenter,applied_load,HB_value,method,lower,upper)

    var res = await eel.getResults(caliberation,output,indentor,load,hbvalue,lowerRange,higherRange)()
    // console.log(res)
    // var res = await eel.getR()()
    document.getElementById('result').value = res
}

async function saveSingleResult(event){
    event.preventDefault()
    var indentor = document.getElementById('select-indenter').value
    console.log(indentor)
    var load =  document.getElementById('select-load').value
    console.log(load)
    var caliberation = document.getElementById('caliberation').value
    console.log(caliberation)
    var hbvalue = document.getElementById('select-hb').value
    console.log(hbvalue)
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


    console.log("RECORD")

    await eel.saveRecord(caliberation,indentor,load,hbvalue,lowerRange,higherRange,filename,jobname,custname,custadd,res,testedby,witnessedby,aprovedby)()

}

var list = []

async function saveInfo(){
    
  alert('record added')
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
  var logoimgsrc = './images/qsonlogo.png';

  var authDetails = {
    "filename":filename, 
    "jobname":jobname ,
    "customer-name":custname,
    "customer-address": custadd,
    "tested-by":testedby,
    "witnessed-by":witnessedby,
    "aprooved-by":aprovedby,}
  var doc = { "calculated-hb":res,
            "given-hb":hbvalue,
            "diameter-of-indentor":indentor,
            "caliberation-value":caliberation,
            "load":load,
            "lowerRange":lowerRange,
            "higherRange":higherRange,

        };
  list.push(doc);
  console.log(doc);

  await eel.saveBatchRecord(authDetails,list)()
}


async function constructTable(selector) {

    var list =  await eel.getData()()
    console.log(list)
             
    // Getting the all column names
    var cols = Headers(list, selector); 

    // Traversing the JSON data
    for (var i = 0; i < list.length; i++) {
        var row = $('<tr/>');  
        for (var colIndex = 0; colIndex < cols.length; colIndex++)
        {
            var val = list[i][cols[colIndex]];
             
            // If there is any key, which is matching
            // with the column name
            if (val == null) val = ""; 
                row.append($('<td/>').html(val));
        }
         
        // Adding each row to the table
        $(selector).append(row);
    }
}
 
function Headers(list, selector) {
    var columns = [];
    var header = $('<tr/>');
     
    for (var i = 0; i < list.length; i++) {
        var row = list[i];
         
        for (var k in row) {
            if ($.inArray(k, columns) == -1) {
                columns.push(k);
                 
                // Creating the header
                header.append($('<th/>').html(k));
            }
        }
    }
     
    // Appending the header to the table
    $(selector).append(header);
        return columns;
}      

function py_video(flg) {
    //alert("a")
    //eel.video_feed()()
    eel.toupcamvideo_feed(flg)()
}



eel.expose(updateImageSrc);
function updateImageSrc(val) {
    let elem = document.getElementById('bg');
    elem.src = "data:image/jpeg;base64," + val
}

function printData()
{
   var divToPrint=document.getElementById("table");
   newWin= window.open("");
   newWin.document.write(divToPrint.outerHTML);
   newWin.print();
   newWin.close();
}

