$(function() {
    console.log(window.innerWidth);
    var check = false;
    (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4)))check = true})(navigator.userAgent||navigator.vendor||window.opera);
    if (window.innerWidth<768) {
        $('#notification-nav-icon').remove();
        $('#mobile-notification-text').html('Notifications<span class="caret"></span>');
        $('#friend-request-nav-icon').remove();
        $('#mobile-friend-text').html('Friend Requests<span class="caret"></span>');
        $('#group-request-nav-icon').remove();
        $('#mobile-group-text').html('Group Requests<span class="caret"></span>');
        $('.non-mobile').remove();
        $('.request_list').removeClass('request_list');
        $('.icon_list').removeClass('icon_list');
    } else {
        $('.dropdown').on('hide.bs.dropdown', function(e) {
            if (!check) { return false; }
        });
    }
    // $(".main-event-feed").css({'max-height': (window.innerHeight-370)+'px', 'overflow': 'auto'});
    $(".main-events-going-to").css({'max-height': (window.innerHeight-480)*3/4+'px', 'overflow': 'auto'});
    $(".main-group-list").css({'max-height': (window.innerHeight-480)/3+'px', 'overflow': 'auto'});
    $(".main-feed").css({'max-height': (window.innerHeight/3 + 40)+'px', 'overflow': 'auto'});
    $("div.main").css({'min-height': (window.innerHeight-165)+'px'});
    $("div.wrapper").css({'min-height': (window.innerHeight-165)+'px'});
    $('a.tooltipped').tooltip();
    
    moment.locale('en', {
        calendar : {
            lastDay : '[Yesterday at] LT',
            sameDay : '[Today at] LT',
            nextDay : '[Tomorrow at] LT',
            lastWeek : '[last] dddd [at] LT',
            nextWeek : 'dddd [at] LT',
            sameElse : 'dddd, MMM Do [at] LT'
        }
    });

    var d = new Date();
    $('#current-date').text(moment(d).format('MMMM Do YYYY, h:mm a'));
    standardizeDatesStarting();
    standardizeDatesHappening();
    var date_array = $('.date-posted')
    for (i=0; i < date_array.length; i++) {
        var date = new Date(date_array[i].innerHTML);
        date_array[i].innerHTML = moment(date).fromNow();
    }

    var update = $('#update').text()

    if (update != "") {
        var start = new Date($('.datepicker').val() + 'T' + $('#id_time_starting').val())
        var end = new Date($('.datepicker').val() + 'T' + $('#id_time_ending').val())
    } else if ($('.datepicker').val() != "") {
        var start = new Date($('.datepicker').val() + ' ' + $('#id_time_starting').val())
        var end = new Date($('.datepicker').val() + ' ' + $('#id_time_ending').val())
    } else {
        var start = d
        var end = d
    }
    try {
        $('.datepicker').datepicker({ dateFormat: 'yy-mm-dd', changeMonth: true, changeYear: true, selectOtherMonths: true, showOtherMonths: true, minDate: start});
        
        if ($('#saved').text() == "") {
            $('.datepicker').val(moment(start).format('YYYY-MM-DD'))
        }

        var coeff = 1000 * 60 * 15;
        var rounded = new Date(Math.round(d.getTime() / coeff) * coeff + coeff) 
        // $('.timepicker').timepicker({ 'timeFormat': 'h:i a', 'scrollDefault': 'now', 'step': 15  , 'minTime': rounded, 'forceRoundTime': true});
        if (!check) {
            $('.timepicker').timeEntry({ampmPrefix: ' '});
        }
        // $('#id_time_starting').val(d.getTime())
        // $('#id_time_starting').val(d.getTime())$('#')

        if (update != "" || $('#form-errors').text()) {
            if ($('#saved').text() == "") {
                $('#id_time_starting').val(moment(start).format('hh:mm A'))
            }
        } else {
            $('#id_time_starting').val(moment(rounded).format('hh:mm A'))
        };
        if (update != "" || $('#form-errors').text()) {
            if ($('#saved').text() == "") {
                $('#id_time_ending').val(moment(end).format('hh:mm A'))
            }
        } else {
            $('#id_time_ending').val(moment(new Date(rounded.getTime() + 1000*60*60)).format('hh:mm A'))
        };
    }
    catch(err) {
    }

    var options = {'width': '625px', 'height': '300px', 'overflow-y': 'auto'};
    try {
        $('a.popup').popup(options);
        $('a.popup-mini').popup({'width': '100px;', 'height': '80px', 'overflow': 'auto'});
    }
    catch(err) {
    }
    try {
        $('#current-timezone').val(jstz.determine().name());
    }
    catch(err) {
    }
    // if (('localStorage' in window) && window['localStorage'] !== null) {
    //     if ('main-event-feed' in localStorage) {
    //         $(".main-event-feed").html(localStorage.getItem('main-event-feed'));
    //     }
    // }
    
});



function standardizeDatesStarting() {
    var span = $(".date-starting")
    for (i=0; i < span.length; i++) {
        var date = new Date(span[i].innerHTML);
        span[i].innerHTML = moment(date).calendar();
    } 
    
}

function standardizeDatesHappening() {
    var span = $("#rawdate")
    var date = new Date(span.html());
    $('#date-happens').html(moment(date).format('MMM Do YYYY'));
    $('#from-time').html(moment(date).format('[From] h:mm a [to]'));
    $('#from-time').html($('#from-time').html() + " " + moment(new Date($('#rawdate-end').html())).format('h:mm a'));
}

function standardizeDatesStartingWithLocation(location) {
    var span = $(location).find('.date-starting')[0]
    console.log(span.innerHTML);
    var date = new Date(span.innerHTML.replace(' ', 'T'));
    span.innerHTML = moment(date).calendar();
}

function standardizeDatesPosted(location) {
    var span = $(location).children('h5').children()[0]
    console.log(span.innerHTML);
    var date = new Date(span.innerHTML.replace(' ', 'T'));
    span.innerHTML = moment(date).fromNow();
}

// $(document).on("pagecontainerbeforechange", function (e, data) {
//     if (typeof data.toPage == "string" && data.options.direction == "back") {
//         $.mobile.pageContainer.pagecontainer( "change", "#pageX", { back: "back" } );
//         console.log('Back out...');
//     }
// });

// $( document ).on( "pagebeforechange" , function ( event, data ) {
//     var stuff = data.options.back;
//     console.log(stuff);
// });


// $(window).unload(function () {
//     if ($(".main-event-feed").length > 0) {
//         console.log("unload");
//         if (('localStorage' in window) && window['localStorage'] !== null) {
//             var form = $(".main-event-feed").html();
//             localStorage.setItem('main-event-feed', form);
//         }
//     }
// });




$('.event-detail').on('click', '.confirm-can-come', function(e) {
    e.preventDefault();
    console.log('coming!');
    prk = $("#"+e.target.id).attr('alt');
    $.ajax({
        type: 'GET',
        url: '/can_come/',
        data: {
            pk: prk
        },
        success: function(data) {
            $("#event-detail-"+prk).html('<br><img style="max-height: 40px; max-width: 40px; float:left" src="' + data[4] + '"><h4 style="float: left;"><strong class="black">&nbsp;' + data[1] + '</strong></h4><h5 class="darkgrey" style="float: right;">Posted <span class="date-posted">' + data[5] + '</span></h5><br style="clear:both;"><h2 class="text-center"><a href="/events/' + prk +'">' + data[0] + '</a></h2><div class="row"><div class="col-md-4"><h4 class="date-starting">' + data[2] + '</h4><h5>' + data[3] + '</h5><h5>' + data[7] + '</h5></div><div class="col-md-8 text-right"><h3>' + data[6] + '</h3></div></div><a class="btn btn-default" alt="' + prk + '"  href="/events/' + prk +'">More details...</a><div class="text-right" style="float:right;"><span class="green stan"><i class="fa fa-check-circle"></i>&nbsp;&nbsp;You\'re going!</span>&nbsp;&nbsp;<a class="btn btn-danger cancel-decision" id="reject-button-' + prk + '" alt="' + prk + '"  href="#"><i class="fa fa-times-circle" alt="' + prk + '" id="' + prk + '"></i>&nbsp;&nbsp;Back out...</a></div></div><br><br>');
            standardizeDatesPosted("#event-detail-"+prk);
            standardizeDatesStartingWithLocation("#event-detail-"+prk);
        }
    });
    
});

$('.event-detail').on('click', '.confirm-cannot-come', function(e) {
    e.preventDefault();
    console.log('won\'t make it...');
    prk = $("#"+e.target.id).attr('alt');
    $.ajax({
        type: 'GET',
        url: '/cannot_come/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#event-detail-"+prk).html('<br><img style="max-height: 40px; max-width: 40px; float:left" src="' + data[4] +'"><h4 style="float: left;"><strong style="color: darkgray">&nbsp;' + data[1] + '</strong></h4><div class="text-right" style="float:right"><span class="red stan"><i class="fa fa-times-circle"></i>&nbsp;&nbsp;You\'re not going...</span><br><br><a class="btn btn-sm btn-success cancel-decision" id="confirm-button-' + prk + '" alt="' + prk + '"  href="#"><i class="fa fa-check-circle" alt="' + prk + '" id="' + prk + '"></i>&nbsp;&nbsp;Cancel</a></div><h2 class="text-center darkgray"><a style="color: #424242" href="/events/' + prk +'">' + data[0] + '</a></h2><h5 style="color: darkgray" class="text-left date-starting">' + data[2] + '</h5><br>');
            // standardizeDatesPosted("#event-detail-"+prk);
            standardizeDatesStartingWithLocation("#event-detail-"+prk);
        }
    });
}); // <a class="btn btn-sm btn-warning cancel-decision" id="confirm-button-' + prk + '" alt="' + prk + '" href="#" style="float:left"><i class="fa fa-check-circle"></i>&nbsp;&nbsp;Well, I can\'t commit now...!</a>


$('.event-detail').on('click', '.cancel-decision', function(e) {
    e.preventDefault();
    console.log('won\'t make it...');
    prk = $("#"+e.target.id).attr('alt');
    $.ajax({
        type: 'GET',
        url: '/cancel_decision/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#event-detail-"+prk).html(
                '<br><img style="max-height: 40px; max-width: 40px; float:left" src="' + data[4] + '"><h4 style="float: left;"><strong class="black">&nbsp;' + data[1] + '</strong></h4><h5 class="darkgrey" style="float: right;">Posted <span class="date-posted">' + data[5] + '</span></h5><div class="row" style="clear:both;"><h2 class="text-center"><a href="/events/' + prk +'">' + data[0] + '</a></h2><div class="col-md-7"><h4 class="date-starting">' + data[2] + '</h4></div><div class="col-md-5 text-right"><h5>' + data[6] + '</h5></div></div><a class="btn btn-default" alt="' + prk + '"  href="/events/' + prk +'">More details...</a><div class="text-right" style="float:right;"><a class="btn btn-success confirm-can-come" alt="' + prk + '" id="confirm-button-' + prk + '" href="#"><i class="fa fa-check-circle" alt="' + prk + '"  alt="' + prk + '" id="' + prk + '"></i>&nbsp;&nbsp;Count me in!</a>&nbsp;<a class="btn btn-danger confirm-cannot-come" alt="' + prk + '" id="reject-button-' + prk + '" href="#"><i class="fa fa-times-circle" alt="' + prk + '" id="' + prk + '"></i>&nbsp;&nbsp;Can\'t make it!</a></div></div><br><br>'
                );  
            standardizeDatesPosted("#event-detail-"+prk); 
            standardizeDatesStartingWithLocation("#event-detail-"+prk);
        }
    });
});

                        
$('.event-detail-buttons').on('click', '.confirm-can-come', function(e) {
    e.preventDefault();
    console.log('coming!');
    prk = $("#"+e.target.id).attr('alt');
    $.ajax({
        type: 'GET',
        url: '/can_come/',
        data: {
            pk: prk
        },
        success: function(data) {
            $(".event-detail-buttons").html('<span class="green stan"><i class="fa fa-check-circle"></i>&nbsp;&nbsp;You\'re going!</span>&nbsp;&nbsp;<a class="btn btn-danger cancel-decision" id="reject-button-' + prk + '" alt="' + prk + '"  href="#"><i class="fa fa-times-circle" alt="' + prk + '" id="' + prk + '"></i>&nbsp;&nbsp;Back out...</a>');
        }
    });
    
});

$('.event-detail-buttons').on('click', '.confirm-cannot-come', function(e) {
    e.preventDefault();
    console.log('won\'t make it...');
    prk = $("#"+e.target.id).attr('alt');
    $.ajax({
        type: 'GET',
        url: '/cannot_come/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $(".event-detail-buttons").html('<span class="red stan"><i class="fa fa-times-circle"></i>&nbsp;&nbsp;You\'re not going...</span>&nbsp;&nbsp;<a class="btn btn-success cancel-decision" id="confirm-button-' + prk + '" alt="' + prk + '"  href="#"><i class="fa fa-check-circle" alt="' + prk + '" id="' + prk + '"></i>&nbsp;&nbsp;Cancel</a>');

        }
    });
}); // <a class="btn btn-sm btn-warning cancel-decision" id="confirm-button-' + prk + '" alt="' + prk + '" href="#" style="float:left"><i class="fa fa-check-circle"></i>&nbsp;&nbsp;Well, I can\'t commit now...!</a>


$('.event-detail-buttons').on('click', '.cancel-decision', function(e) {
    e.preventDefault();
    console.log('won\'t make it...');
    prk = $("#"+e.target.id).attr('alt');
    $.ajax({
        type: 'GET',
        url: '/cancel_decision/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $(".event-detail-buttons").html('<a class="btn btn-success confirm-can-come" alt="' + prk + '" id="confirm-button-' + prk + '" href="#"><i class="fa fa-check-circle" alt="' + prk + '"  alt="' + prk + '" id="' + prk + '"></i>&nbsp;&nbsp;Count me in!</a>&nbsp;<a class="btn btn-danger confirm-cannot-come" alt="' + prk + '" id="reject-button-' + prk + '" href="#"><i class="fa fa-times-circle" alt="' + prk + '" id="' + prk + '"></i>&nbsp;&nbsp;Can\'t make it!</a>'
                );  
        }
    });
});

                        
    


$('.friend_request_section').on('click', '.request-add-button', function(e) {
    e.preventDefault();
    console.log('requested');
    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/request_friendship/',
        data: {
            pk: prk
        },
        success: function(data) {
            $("#friend_request_section-"+prk).html('');
            $("#friend_request_section-"+prk).html('<a class="btn btn-default">Requested as a friend</a>&nbsp;<a id="cancel-request-' + prk + '" class="btn btn-warning cancel-request" href = "#" alt=' + prk + '>Cancel request</a>');
        }

    });
});

$('.friend_request_section').on('click', '.cancel-request', function(e) {
    e.preventDefault();
    console.log('requested');
    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/cancel_request/',
        data: {
            pk: prk
        },
        success: function(data) {
            $("#friend_request_section-"+prk).html('');
            $("#friend_request_section-"+prk).html('<a id="request-add-button-'+ prk +'" class="btn btn-primary request-add-button" href = "#" alt='+ prk +'>Add as a friend</a>');
        }

    });
});

$('.friend_request_section').on('click', '.delete-friend-button', function(e) {
    e.preventDefault();
    console.log('delete friendship');
    var prk = $("#"+e.target.id).attr('alt')
    var confirm = window.confirm("You're about to delete " + $("#"+e.target.id).attr('placeholder') + " as a friend. Are you sure you want to do that?")
    if (confirm) {
        $.ajax({
            type: 'GET',
            url: '/delete_friendship/',
            data: {
                pk: prk,
            },
            success: function(data) {
                $("#friend_request_section-"+prk).html('');
                $("#friend_request_section-"+prk).html('<h3 class="btn btn-default"> Your friendship with ' + data[0] + ' has been deleted.</h3>');
                setTimeout(function(){ location.reload(); }, 1400);
            }

        });
    }
});


$('.friend_request_section').on('click', '.detail-add-button', function(e) {
    e.preventDefault();
    console.log('added');
    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/accept_request/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#friend_request_section-"+prk).html('');
            $("#friend_request_section-"+prk).html('<h4 class="green">You are now friends with ' + data[0] + '!</h4>');
            if (data[1] == 0) {
                $("#friend_request_bubble").html('');
            } else {
                $("#friend_request_noti").text(data[1]);
            }
        }

    });
});


$('.friend_request_section').on('click', '.detail-reject-button', function(e) {
    e.preventDefault();
    console.log('rejected...');
    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/reject_request/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#friend_request_section-"+prk).html('');
            $("#friend_request_section-"+prk).html('<h4 class="red">You rejected ' + data[0] + '\'s request...</h4>');
            if (data[1] == 0) {
                $("#friend_request_bubble").html('');
            } else {
                $("#friend_request_noti").text(data[1]);
            }
        }

    });
});


$('.add-menu').on('click', '.add-button', function(e) {
    e.preventDefault();
    console.log('added');
    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/accept_request/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#notif-friend-li-"+prk).html('<a href="/people/' + prk + '/" class="added green">' + data[0] + ' added</a>');
            $("#li-"+prk).html('<a href="/people/' + prk + '/" class="added green">' + data[0] + ' added</a>');
            if (data[1] == 0) {
                $("#friend_request_bubble").html('');
            } else {
                $("#friend_request_noti").text(data[1]);
            }
        }

    });
});

$('.add-menu').on('click', '.reject-button', function(e) {
    e.preventDefault();
    console.log('rejected...');
    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/reject_request/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#notif-friend-li-"+prk).html('<a class="rejected red">' + data[0] + ' rejected...</a>');
            $("#li-"+prk).html('<a class="rejected red">' + data[0] + ' rejected...</a>');
            if (data[1] == 0) {
                $("#friend_request_bubble").html('');
            } else {
                $("#friend_request_noti").text(data[1]);
            }
        }

    });
});


$('.group-add-menu').on('click', '.add-button', function(e) {
    e.preventDefault();
    console.log('added');
    console.log(e.target);
    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/user_accepts_invitation/',
        data: {
            group_pk: prk,
        },
        success: function(data) {
            $("#notif-group-div-"+prk).html('<a href="/groups/' + prk + '/" class="added green">' + data[0] + ' added</a>');
            $("#group-li-"+prk).html('<a href="/groups/' + prk + '/" class="added green">' + data[0] + ' added</a>');
            if (data[2] == 0) {
                $("#group_request_bubble").html('');
            } else {
                $("#group_request_noti").text(data[2]);
            }
        }

    });
});

$('.group-add-menu').on('click', '.reject-button', function(e) {
    e.preventDefault();
    console.log('rejected...');
    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/reject_invitation_from_group/',
        data: {
            group_pk: prk,
            person_pk: $('#profile-pk').text(),
        },
        success: function(data) {
            $("#notif-group-div-"+prk).html('<a href="/groups/' + prk + '/" class="rejected red">' + data[0] + ' rejected...</a>');
            $("#group-li-"+prk).html('<a href="/groups/' + prk + '/" class="rejected red">' + data[0] + ' rejected...</a>');
            if (data[2] == 0) {
                $("#group_request_bubble").html('');
            } else {
                $("#group_request_noti").text(data[2]);
            }
        }

    });
});


$('.notification-menu').on('click', '.clear-button', function(e) {
    e.preventDefault()
    var prk = $("#"+e.target.id).attr('alt')
    console.log(prk);
    $.ajax({
        type: 'GET',
        url: '/clear_notification/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#notif-row-"+prk).removeClass('unread');
            $("#notif-"+prk).remove('');
                if (data[0] == 0) {
                    $("#notification_request_bubble").html('');
                    $("#notifs").html('<li><a class="navbar-li">No notifications!</a></li>');
                    $("#notif-row-"+prk).removeClass('unread');
                    $("#notif-clear-button-"+prk).remove();
                } else {
                    $("#notification_request_count").text(data[0]);
                }
                var href = e.target.href
                if (href) {
                    window.location = href
                }
        }
    });
});







$('#group-detail').on('click', '.request_membership_in_group', function(e) {
    e.preventDefault();
    console.log('user requesting group');
    var prk = $('#group_pk').attr('alt')
    $.ajax({
        type: 'GET',
        url: '/request_membership_in_group/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#group_request_section-"+prk).html('');
            $("#group_request_section-"+prk).html('<span class="btn btn-default">' + data[0] + ' requested</span>&nbsp;<a id="cancel-request-' + prk + '" class="btn btn-warning cancel_request_membership_in_group" href = "#" alt=' + prk + '>Cancel request</a>');
        }
    });
});


$('#group-detail').on('click', '.cancel_request_membership_in_group', function(e) {
    e.preventDefault();
    console.log('user cancelling request to group');
    var prk = $('#group_pk').attr('alt')
    $.ajax({
        type: 'GET',
        url: '/cancel_request_membership_in_group/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#group_request_section-"+prk).html('');
            $("#group_request_section-"+prk).html('<a id="request-add-button-' + prk + '" class="btn btn-primary request_membership_in_group" href = "#" alt="' + prk + '">Request to join ' + data[0] + '</a>');
        }
    });

});


$('#group-detail').on('click', '.accept_invitation_from_group', function(e) {
    e.preventDefault();
    console.log('accept to join group');
    var prk = $('#group_pk').attr('alt')
    $.ajax({
        type: 'GET',
        url: '/user_accepts_invitation/',
        data: {
            group_pk: prk,
            person_pk: $('#user_pk').attr('alt'),
        },
        success: function(data) {
            $("#group_request_section-"+prk).html('');
            $("#group_request_section-"+prk).html('<h3 class="green">You\'re now a member of ' + data[0] + '!</h3>');
        }
    });
});


$('#group-detail').on('click', '.reject_invitation_from_group', function(e) {
    e.preventDefault();
    console.log('reject group invitation');
    var person_pk = $('#'+e.target.id).attr('alt');
    var group_pk = $('#group_pk').attr('alt');
    $.ajax({
        type: 'GET',
        url: '/reject_invitation_from_group/',
        data: {
            group_pk: group_pk,
            person_pk: person_pk,
        },
        success: function(data) {
            $("#group_request_section-"+group_pk).html('');
            $("#group_request_section-"+group_pk).html('<h4 class="red"> You declined joining '+ data[0]+'...</h4>');
        }
    });
});


$('#adminship').on('click', '.accept_request_from_user', function(e) {
    e.preventDefault();
    console.log('accept user into this group');
    var prk = $('#'+e.target.id).attr('alt');
    $.ajax({
        type: 'GET',
        url: '/group_approves_request/',
        data: {
            group_pk: $('#group_pk').attr('alt'),
            person_pk: prk,
        },
        success: function(data) {
            $("#accept-request-"+prk).html('');
            $("#accept-request-"+prk).html('<span class="green">Accepted!</span>');
        }
    });
});


$('#adminship').on('click', '.reject_request_from_user', function(e) {
    e.preventDefault();
    console.log('reject user from joining group');
    var prk = $('#'+e.target.id).attr('alt');
    $.ajax({
        type: 'GET',
        url: '/reject_invitation_from_group/',
        data: {
            group_pk: $('#group_pk').attr('alt'),
            person_pk: prk,
        },
        success: function(data) {
            $("#accept-request-"+prk).html('');
            $("#accept-request-"+prk).html('<span class="red">Rejected...</span>');
        }
    });

});


$('#membership').on('click', '.leave_group', function(e) {
    e.preventDefault();
    console.log('leave a group');
    var confirm = window.confirm("You're about to leave " + e.target.id + ". Are you okay with that?")
    if(confirm) {
        var prk = $('#group_pk').attr('alt')
        $.ajax({
            type: 'GET',
            url: '/leave_group/',
            data: {
                pk: prk,
            },
            success: function(data) {
                $("#membership").html('');
                $("#adminship").html('');
                $("#membership").html('<h3 class="red">You left ' + data[0] + '...</h3>');
                setTimeout(function(){ location.reload(); }, 1400);
            }
        });
    }
});


$('.delete-button').on("click", function(e) {
    e.preventDefault();
    var confirm = window.confirm("You're about to delete " + e.target.id + ". Are you okay with that?")
    if(confirm) {
        window.location = e.target.href
    }
});

$('.reply-link').on('click', function(event) {
    event.preventDefault();
    if ($('#reply-pk').val() !== $(this).attr('alt')) {
        $('#reply-pk').val($(this).attr('alt'));
        $(".event-comment").css({'background': ''});
        $('#'+$(this).attr('alt')).parent().css({'background': 'rgba(39, 163, 156, 0.3)'});
        console.log($('#reply-pk').val());
        console.log('#'+$(this).attr('alt')+"author");
        $('#replying-to').text(" -- Replying to "+$('#'+$(this).attr('alt')+"author").text());
    } else {
        $('#reply-pk').val("");
        $(".event-comment").css({'background': ''});
        $('#replying-to').text("");
    }
    $('#comment_body').focus();
});



 $('#sharing').on('click', '#share-event', function(e) {
        e.preventDefault();
        console.log('Share!');
        var prk = $(this).attr('alt');
        $.ajax({
            type: 'GET',
            url: '/share_event/',
            data: {
                pk: prk,
            },
            success: function(data) {
                if (data[1]) {
                    $("#sharing").html('<h4 class="green">You shared ' + data[0] + ' to your feed.</h4>&nbsp;&nbsp;<a class="btn btn-danger" href="#" alt="' + prk + '" id="share-event">Undo</a>');
                } else {
                    $("#sharing").html('<a class="btn btn-success" href="#" alt="' + prk + '" id="share-event">Share this event to your feed!</a>');
                }
            }
        });
    });


