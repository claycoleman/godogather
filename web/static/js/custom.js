$(function() {
    $(".main-event-feed").css({'max-height': (window.innerHeight-280)+'px', 'overflow': 'scroll'});
    $(".main-feed").css({'max-height': (window.innerHeight/2)+'px', 'overflow': 'scroll'});
    $('a.tooltipped').tooltip();
    var date_str = $('#current-date').text();
    var d = new Date(date_str);
    $('#current-date').text(moment(d).format('MMMM Do YYYY, h:mm a'));
    var date_array = $('.date-posted')
    for (i=0; i < date_array.length; i++) {
        var date = new Date(date_array[i].innerHTML);
        date_array[i].innerHTML = moment(date).fromNow();
    }
    $('.datepicker').datepicker({ dateFormat: 'yy-mm-dd', changeMonth: true, changeYear: true, selectOtherMonths: true, showOtherMonths: true});
    $('.timepicker').timepicker({ 'timeFormat': 'h:i a', 'scrollDefault': 'now', 'step': 5  });
    // if (('localStorage' in window) && window['localStorage'] !== null) {
    //     if ('main-event-feed' in localStorage) {
    //         $(".main-event-feed").html(localStorage.getItem('main-event-feed'));
    //     }
    // }
    
});


function standardizeDates(location) {
    var span = $(location).children('h5').children()[0]

    console.log(span);
    var date = new Date(span.innerHTML);
    console.log(date);
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
            $("#event-detail-"+prk).html('<br><img style="max-height: 40px; max-width: 40px; float:left" src="' + data[4] + '"><h4 style="float: left;"><strong class="black">&nbsp;' + data[1] + '</strong></h4><h5 class="darkgrey" style="float: right;">Posted <span class="date-posted">' + data[5] + '</span></h5><br style="clear:both;"><h2 class="text-center"><a href="/event_detail/' + prk +'">' + data[0] + '</a></h2><div class="row"><div class="col-sm-4"><h4>' + data[2] + '</h4><h5>' + data[3] + '</h5><h5>' + data[7] + '</h5></div><div class="col-sm-8 text-right"><h3>' + data[6] + '</h3></div></div><a class="btn btn-default" alt="' + prk + '"  href="/event_detail/' + prk +'">More details...</a><div class="text-right" style="float:right;"><span class="green stan"><i class="fa fa-check-circle"></i>&nbsp;&nbsp;You\'re going!</span>&nbsp;&nbsp;<a class="btn btn-danger cancel-decision" id="reject-button-' + prk + '" alt="' + prk + '"  href="#"><i class="fa fa-times-circle"></i>&nbsp;&nbsp;Back out...</a></div></div><br><br>');
            standardizeDates("#event-detail-"+prk);
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
            $("#event-detail-"+prk).html('<br><img style="max-height: 40px; max-width: 40px; float:left" src="' + data[4] +'"><h4 style="float: left;"><strong style="color: darkgray">&nbsp;' + data[1] + '</strong></h4><div class="text-right" style="float:right"><span class="red stan"><i class="fa fa-times-circle"></i>&nbsp;&nbsp;You\'re not going...</span><br><br><a class="btn btn-sm btn-success cancel-decision" id="confirm-button-' + prk + '" alt="' + prk + '"  href="#"><i class="fa fa-check-circle"></i>&nbsp;&nbsp;Cancel</a></div><h2 class="text-center darkgray"><a style="color: #424242" href="/event_detail/' + prk +'">' + data[0] + '</a></h2><h5 style="color: darkgray" class="text-left">' + data[2] + '</h5><br>');
            standardizeDates("#event-detail-"+prk);

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
                '<br><img style="max-height: 40px; max-width: 40px; float:left" src="' + data[4] + '"><h4 style="float: left;"><strong class="black">&nbsp;' + data[1] + '</strong></h4><h5 class="darkgrey" style="float: right;">Posted <span class="date-posted">' + data[5] + '</span></h5><div class="row" style="clear:both;"><h2 class="text-center"><a href="/event_detail/' + prk +'">' + data[0] + '</a></h2><div class="col-sm-7"><h4>' + data[2] + '</h4></div><div class="col-sm-5 text-right"><h5>' + data[6] + '</h5></div></div><a class="btn btn-default" alt="' + prk + '"  href="/event_detail/' + prk +'">More details...</a><div class="text-right" style="float:right;"><a class="btn btn-success confirm-can-come" alt="' + prk + '" id="confirm-button-' + prk + '" href="#"><i class="fa fa-check-circle"></i>&nbsp;&nbsp;Count me in!</a>&nbsp;<a class="btn btn-danger confirm-cannot-come" alt="' + prk + '" id="reject-button-' + prk + '" href="#"><i class="fa fa-times-circle"></i>&nbsp;&nbsp;Can\'t make it!</a></div></div><br><br>'
                );  
            standardizeDates("#event-detail-"+prk); 
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
            $("#friend_request_section-"+prk).html('<a class="btn btn-default">' + data[0] + ' requested</a>&nbsp;<a id="cancel-request-' + prk + '" class="btn btn-warning cancel-request" href = "#" alt=' + prk + '>Cancel request</a>');
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
    $.ajax({
        type: 'GET',
        url: '/delete_friendship/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#friend_request_section-"+prk).html('');
            $("#friend_request_section-"+prk).html('<h3 class="btn btn-default"> Your friendship with ' + data[0] + ' has been deleted.</h3>');
        }

    });
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
    console.log(e.target);
    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/accept_request/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#li-"+prk).html('<a class="added">' + data[0] + ' added</a>');
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
            $("#li-"+prk).html('<a class="rejected">' + data[0] + ' rejected...</a>');
            if (data[1] == 0) {
                $("#friend_request_bubble").html('');
            } else {
                $("#friend_request_noti").text(data[1]);
            }
        }

    });
});


$('#group-detail').on('click', '.request_membership_in_group', function(e) {
    e.preventDefault();
    console.log('user requesting group');
    var prk = $("#"+e.target.id).attr('alt')
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
    var prk = $("#"+e.target.id).attr('alt')
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
    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/group_invitation_accepted/',
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

    var prk = $("#"+e.target.id).attr('alt')
    $.ajax({
        type: 'GET',
        url: '/reject_invitation_from_group/',
        data: {
            pk: prk,
        },
        success: function(data) {
            $("#group_request_section-"+prk).html('');
            $("#group_request_section-"+prk).html('<a id="request-add-button-' + prk + '" class="btn btn-primary request_membership_in_group" href = "#" alt="' + prk + '">Request to join ' + data[0] + '</a>');
        }
    });
});


$('#group-detail').on('click', '.accept_request_from_user', function(e) {
    e.preventDefault();
    console.log('accept user into group');
});


$('#group-detail').on('click', '.reject_request_from_user', function(e) {
    e.preventDefault();
    console.log('reject user from joining group');
});


$('#group-detail').on('click', '.leave_group', function(e) {
    e.preventDefault();
    console.log('leave a group');
    var prk = $("#"+e.target.id).attr('alt')
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
        }
    });
});





$('.dropdown').on('hide.bs.dropdown', function(e) {
    return false;
});