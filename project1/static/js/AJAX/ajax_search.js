$(function() {var val = document.getElementById('search-ajax');
val.oninput = function() {
$.ajax({
    type:"GET",
                        url:"search/",
                        data:{
                            'val':val.value
                        },
                        success: function(response){
                            let list = document.getElementById('character');
                            let len =(response.mas).length
                           
                            for (i=0; i<len; i++){
                            let option = document.createElement('option');
                            option.value = response.mas[i];
                            list.appendChild(option);
                            if (list.options.length>len){
                                option.remove()
                            }
                            
                            }
                            if (len>30){
                              return
                          }
                          
                           
                      
                        },
                        error: function(response) {
                                    console.log('error', response)
                         }
  })
};
});