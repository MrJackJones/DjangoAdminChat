$(function ($) {
    function updateItem() {
    jQuery('.refresh').trigger('click');
    }

    $(function() {
        setInterval(updateItem, 2000);
    });

    window.onload=function () {
    let elms_id = document.querySelectorAll("[id^='chat']");

    for(let i = 0; i < elms_id.length; i++)
      elms_id[i].scrollTop = elms_id[i].scrollHeight;
    };
    
    $('.model-chat').on('click', '.add-comment', function (e) {
        e.preventDefault();

        let self = $(this);
        let chat = self.parents('.main-chat');
        let chatId = chat.data('id');
        let url = './add_comment/' + chatId;
        let message = self.parent().find('.message').val().trim();

        if (!message) {
            alert('Comment is required!');
            return
        }

        self.prop('disabled', true);

        $.post(url, {
            message: message,
        }, function (data) {
            if (data.status !== true) {
                alert('Error on add message');
                return;
            }
            $('.message').val('');
            let objDiv = document.getElementsByClassName("chat-"+chatId);
            objDiv.scrollTop = objDiv.scrollHeight;
        }).always(function () {
            self.prop('disabled', false);
        });
    });

    $('.refresh').on('click', function () {
        let self = $(this);
        let chat = self.parents('.main-chat');
        let chatId = chat.data('id');
        let url = './update_data/' + chatId;
            $.get(url, function (data) {
                if (data.status === true) {
                    let result = data.data;
                    let html = '';
                    $.each(result, function(key, value) {
                        if (value.from_admin) {
                            html += '<div class="container darker">';
                        } else {
                            html += '<div class="container">';
                        }
                        html += '<p>';
                        html += value.message;
                        html += '</p>';
                        html += '<span class="time-right">';
                        html += value.created_at;
                        html += '</span><br>';
                        html += '<span class="time-right">';
                        html += value.name;
                        if (value.is_read) {
                            html += ' &#10003;';
                        }
                        html += '</span>';
                        html += '</div>';
                    });

                    $(".chat-"+chatId).html(html);
                    let objDiv_new = document.getElementsByClassName("chat-"+chatId);
                    for(let i = 0; i < objDiv_new.length; i++)
                        objDiv_new[i].scrollTop = objDiv_new[i].scrollHeight;
                }
            });
    });
});

function include(filename)
{
    let head = document.getElementsByTagName('head')[0];
    let script = document.createElement('script');
    script.src = filename;
    script.type = 'text/javascript';
    head.appendChild(script)
}

include('http://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js');
