
sessionStorage.setItem("value",4);
let a = sessionStorage.getItem('value');
function click() {
  a = parseInt(a) + 4;
  sessionStorage.setItem('value', a);
  return sessionStorage.getItem('value');
}


                        sessionStorage
                       window.addEventListener("scroll", function() {
                      
                if (document.documentElement.scrollHeight - document.documentElement.clientHeight == Math.trunc(document.documentElement.scrollTop))
                Func()
                

});
                        function Func(){
                           
                            var val=click();
                            var val_=val-4;
                            $.ajax({
                                type:"GET",
                                url:'/ajax_downolad',
                                data:{
                                    'val':val,
                                    'val_':val_,
                                        },
                                success: function(response){
                                    
                                    if(response.mas!=0){
                                    $("#loadmore").text(val+4)
                                    $('#load_content_ajax').append(response.result);
                                    }
                                    
                                  

                                    

                      },
                      error: function(response) {
                                  console.log('error', response)
                       }
  })
  
  
}
                    