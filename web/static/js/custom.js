$(function() {
    console.log(window.innerWidth);
    
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
        return false;
    });
    }
    // $(".main-event-feed").css({'max-height': (window.innerHeight-370)+'px', 'overflow': 'auto'});
    $(".main-events-going-to").css({'max-height': (window.innerHeight-480)*2/3+'px', 'overflow': 'auto'});
    $(".main-group-list").css({'max-height': (window.innerHeight-480)/4+'px', 'overflow': 'auto'});
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

    if ($('.datepicker').val() != "") {
        var start = new Date($('.datepicker').val() + 'T' + $('#id_time_starting').val())
        var end = new Date($('.datepicker').val() + 'T' + $('#id_time_ending').val())
    } else {
        var start = d
        var end = d
    }
    try {
        $('.datepicker').datepicker({ dateFormat: 'yy-mm-dd', changeMonth: true, changeYear: true, selectOtherMonths: true, showOtherMonths: true});
        if ($('.datepicker').val().indexOf('-') != 4) {
            $('.datepicker').val(moment(start).format('YYYY-MM-DD'))
        }
        $('.timepicker').timepicker({ 'timeFormat': 'h:i a', 'scrollDefault': 'now', 'step': 15  });
        if ($('#id_time_starting').val().indexOf('am') <= -1 && $('#id_time_starting').val().indexOf('pm') <= -1) {
            $('#id_time_starting').val(moment(start).format('hh:mm a'))
        };
        if ($('#id_time_ending').val().indexOf('am') <= -1 && $('#id_time_ending').val().indexOf('pm')  <= -1) {
            $('#id_time_ending').val(moment(end).format('hh:mm a'))
        };
    }
    catch(err) {
    }


    var options = {'width': '625px', 'height': '300px', 'overflow-y': 'auto'};
    try {
        $('a.popup').popup(options);
        $('a.popup-mini').popup({'width': '100px;', 'height': '75px', 'overflow': 'auto'});
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
            standardizeDatesPosted("#event-detail-"+prk);
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
            $("#friend_request_section-"+prk).html('<a class="btn btn-default">' + data[0] + ' requested as a friend</a>&nbsp;<a id="cancel-request-' + prk + '" class="btn btn-warning cancel-request" href = "#" alt=' + prk + '>Cancel request</a>');
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
            $("#friend_request_section-"+prk).html('<a id="request-add-button-'+ prk +'" class="btn btn-primary request-add-button" href = "#" alt='+ prk +'>Add '+data[0]+' as a friend</a>');
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


