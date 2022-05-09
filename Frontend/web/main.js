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

    


}

function py_video(flg) {
    alert("a")
    //eel.video_feed()()
    eel.toupcamvideo_feed(flg)()
}



eel.expose(updateImageSrc);
function updateImageSrc(val) {
    let elem = document.getElementById('bg');
    elem.src = "data:image/jpeg;base64," + val
}