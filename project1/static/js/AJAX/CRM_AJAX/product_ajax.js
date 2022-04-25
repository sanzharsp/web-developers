function CRM_Product_create_set(val) {                                        
$.ajax({
  type:"GET",
                      url:'/ajaxcrm',
                      data:{
                          'val':val
                      },
                      success: function(response){
                        
                         
                          $('#ajax').text(response.mas)
                          
                          
                          var  select = document.getElementById('ajax');
                        for (i=0; i<(response.mas).length; i++){
                            var opt = document.createElement('option');
                            opt.value = response.mas[i];
                            opt.innerHTML = response.mas_name[i];
                            select.appendChild(opt);
                        }
                        
                      },
                      error: function(response) {
                                  console.log('error', response)
                       }
  })
  
  
}