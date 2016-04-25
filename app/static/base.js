/**
 * Created by yanmingwang on 4/24/16.
 */
var slideoutinner = $( "#slideoutinner" );
var search = $("#searchView");
var list = $("#listView");

$("#menu-toggle").click(function(e) {
    e.preventDefault();
    if($("#wrapper").hasClass("toggled")){
         $("#wrapper").removeClass("toggled");
    }else{
         $("#wrapper").addClass("toggled");
    }
});

// Bind the link to toggle the slide.
$( "#slideoutTab" ).click(function( e ){
    // Prevent the default event.
    e.preventDefault();
    // Toggle the slide based on its current
    // visibility.
    if (slideoutinner.is( ":visible" )){
        // Hide - slide up.
        console.log("hide");
        slideoutinner.slideUp( 300 );
    } else {
        console.log("show");
        // Show - slide down.
        slideoutinner.slideDown( 300 );
    }
});

$( "#tab" ).click(function( e ){
    // Prevent the default event.
    e.preventDefault();
    // Toggle the slide based on its current
    // visibility.
    if (list.is( ":visible" )){
        list.hide(500);
        search.show(300);
    }else{
        search.hide(300);
        list.show(500);
    }
});

$(document).on("click", function(event){
    if($("#wrapper").hasClass("toggled")) {
        if($("#menu-toggle") !== event.target && !$("#menu-toggle").has(event.target).length){
            if (event.target.id !== "sidebar-wrapper") {
                $("#wrapper").removeClass("toggled");
            }
        }
    }
    if(slideoutinner.is( ":visible" )) {
        var $trigger = $("#slideoutTab");
        var $triggerT = $("#slideoutinner");
        if ("slideoutTab" !== event.target.id && !$trigger.has(event.target).length) {
            if ($triggerT !== event.target && !$triggerT.has(event.target).length) {
                slideoutinner.slideUp(300);
            }
        }
    }
});

function getJs(detpId) {
    var listText = "";
    $("#courseList").empty();
    $("#courseList").hide();
    $.getJSON($SCRIPT_ROOT + '/_load_list', {
        deptIdIn: detpId
    }, function (data) {
        for(var i =0; i<data.listByDept.length;i++){
            var one = '<li><button class="btn bc btn-block" type="button" data-toggle="modal" onclick="showSection(';
            var two = ')"data-target="#c';
            var three = '">';
            var four = '</button></li>';
            var final = one + data.listByDeptId[i] + two + data.listByDeptId[i] +three + data.listByDept[i] + four;
            listText+=final;
        }
        $(listText).appendTo("#courseList");
        $("#courseList").show(300);
    });
}

function showSection(getcourseId){
    $("#sectionListModal").empty();
    var md = "";
    $.getJSON($SCRIPT_ROOT + '/_load_section', {
        getcourseId: courseId
    }, function (data) {


    });
}



