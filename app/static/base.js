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
            var final = one + data.listByDeptId[i] + two + "c" + three + data.listByDept[i] + four;
            listText+=final;
        }
        $(listText).appendTo("#courseList");
        $("#courseList").show(300);
    });
}

function showSection(getcourseIdin){
    $("#sectionListModal").empty();
    var md = "";
    $.getJSON($SCRIPT_ROOT + '/_load_section', {
        getcourseId: getcourseIdin
    }, function (data) {
        var crn= data.listOfSectionsCRNOut;
        var prf= data.listOfSectionsProfOut;
        var c = data.courseNumOut;
        var cc = data.courseCredOut;
           var se = '<div class="modal fade" id="c" tabindex="-1" role="dialog" aria-labelledby="" aria-hidden="true">' +
                        '<div class="modal-dialog" role="document">' +
                            '<div class="modal-content">'+
                                '<div class="modal-header">' +
                                    '<button type="button" class="close" data-dismiss="modal" aria-hidden="true"><span aria-hidden="true">&times;</span></button>' +
                                    '<h4 class="modal-title" id="myModalLabel">'+data.courseName+ '</h4>' +
                                '</div>'+
                                '<div class="modal-body">'+
                                    '<h3>'+'CRNs: '+crn+
                                          ' Profs: '+prf+'</h3>'+
                                '</div>'+
                                '<div class="modal-footer">'+
                                    '<button type="button" class="btn btn-default" data-dismiss="modal">Back</button>'+
                                    '<button type="button" class="btn btn-primary">Add to Cart</button>'+
                                '</div>'+
                            '</div>'+
                        '</div>'+
                    '</div>';

    $(se).appendTo("#sectionListModal");
        $('#c').modal('show');
    });
}



