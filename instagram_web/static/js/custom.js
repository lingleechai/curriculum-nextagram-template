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
  })


// }else if($('.follow-btn').text()="Pending"){
//     $.ajax({
//         url: `/users/${e.target.id}/${e.target.name}/unfollow`,
//         method: 'GET',
//         beforeSend: function() {
//           $('.follow-btn')
//             .prop('disabled', true)
//             .text('Loading...')
//         },
//         success: function(response) {
//           $('#followers').text(response.new_follower_count)
//           $('.follow-btn')
//             .prop('disabled', false)
//             .removeClass('btn-default-click')
//             .addClass('btn-default')
//             .text('Pending')
//         }
//       })