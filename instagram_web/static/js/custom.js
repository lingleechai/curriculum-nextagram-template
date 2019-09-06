$(document).ready(function() {
    $('.follow-btn').on('click', function(e) {
      e.preventDefault()
      if ($('.follow-btn').text() == "Follow"){
          $.ajax({
            url: `/users/${e.target.id}/${e.target.name}/follow`,
            method: 'GET',
            beforeSend: function() {
              $('.follow-btn')
                .prop('disabled', true)
                .text('Loading...')
            },
            success: function(response) {
                if(response.privacy == true){
                    $('#followers').text(response.new_follower_count)
                    $('.follow-btn')
                        .prop('disabled', false)
                        .removeClass('btn-default')
                        .addClass('btn-default-click')
                        .text('Pending')
                }else{
                    $('#followers').text(response.new_follower_count)
                    $('.follow-btn')
                        .prop('disabled', false)
                        .removeClass('btn-default')
                        .addClass('btn-default-click')
                        .text('Unfollow')
                }
            }
          })
      } else{
        $.ajax({
            url: `/users/${e.target.id}/${e.target.name}/unfollow`,
            method: 'GET',
            beforeSend: function() {
              $('.follow-btn')
                .prop('disabled', true)
                .text('Loading...')
            },
            success: function(response) {
              $('#followers').text(response.new_follower_count)
              $('.follow-btn')
                .prop('disabled', false)
                .removeClass('btn-default-click')
                .addClass('btn-default')
                .text('Follow')
            }
          })
      }
    })
    //
    $('.accept-btn').on('click', function(e) {
        e.preventDefault()
            $.ajax({
              url: `/users/${e.target.id}/approval`,
              method: 'GET',
              beforeSend: function() {
                $('.accept-btn')
                  .prop('disabled', true)
              },
              success: function(response) {
                      $('.follow-amount').text(response.new_follower_requests_count)
                      $('#followers').text(response.new_follower_count)
                      $('.accept-btn')
                          .prop('disabled', false)
                          .removeClass('btn-default')
                          .addClass('btn-default-click')
                          .text('Accepted')
                  }
            })
          })
    $('.decline-btn').on('click', function(e) {
        e.preventDefault()
        $.ajax({
        url: `/users/${e.target.id}/decline`,
        method: 'GET',
        beforeSend: function() {
            $('.decline-btn')
            .prop('disabled', true)
        },
        success: function(response) {
                $('.follow-amount').text(response.new_follower_requests_count)
                $('#followers').text(response.new_follower_count)
                $('.decline-btn')
                    .prop('disabled', false)
                    .removeClass('btn-special')
                    .addClass('btn-default-click')
                    .text('Deleted')
            }
        })
    })
  })