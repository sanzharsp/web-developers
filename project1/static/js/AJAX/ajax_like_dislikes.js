
function Like_dislike_ajax(val) {
    const post_id = val;
    const Like_Unlike_Text=$(`#id_str${post_id}`).text()
    const trim = $.trim(Like_Unlike_Text)
                $.ajax({
                type:"POST",
                url:`/Product/${val}/like`,
                    data:{
                        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                        'post_id':post_id,
                    },
                    success: function(response){
                        
                        if(trim === 'Unlike'){
                            $(`.class_str${post_id}`).text('Like')
                           
                        }
                        if (trim === 'Like'){
                            $(`.class_str${post_id}`).text('Unlike')
                           
                        }
                      
                        $(`.likes${post_id}`).text(response.post_like)
                    },
                    error: function(response) {
                                console.log('error', response)
                     }
                });
    }
                
                    



