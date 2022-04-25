$(document).ready(() => {
    /*------- button with class register -------*/
    let reg_btn:string = $('.container .register')
    
    /*------- button with class sign in --------*/
    let sig_btn:string = $('.container .signin')
    
    /*------- back button ----------------------*/
    let back_btn:string = $('.container .back')
    
  
    
  
    reg_btn.click(function(e){
      e.preventDefault()
      $(this).siblings('.reg').css({
        'transform':'translateY(40%) scale(5)',
        'border-radius':'0',
        'width':'100%',
        'height':'100%'
      }).end();
      
    
      reg_btn.siblings('.container h3:nth-of-type(1)').css({
        'top':'40%',
        'z-index':'8',
      }).end().end();   
    });
    
     sig_btn.on('click',function(e){
      e.preventDefault();
      $(this).siblings('.sig').css({
        'transform':'translateY(40%) scale(5)',
        'border-radius':'0',
        'width':'100%',
        'height':'100%'
      }).end();
       
   
      sig_btn.siblings('.container h3:nth-of-type(2)').css({
        'top':'40%',
        'z-index':'8',
      }).end().end(); 
      
    });
  });
  