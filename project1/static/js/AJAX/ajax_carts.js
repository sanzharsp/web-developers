
   
     function Ajax_count_update(slug){
        let inp = document.querySelector(`.qty${slug}`)
        function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                    }
                }
            }
            return cookieValue;
        }
const csrftoken = getCookie('csrftoken');
        
        $.ajax({
    type:"POST",
     url:`/change-qty/${slug}/`,
        data:{
                'slug':slug,
                'qty':inp.value,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(response){
                if (response.success){
                    var el = document.getElementById('ajax_messages')
                    let resul = document.createElement('div')
                    resul.classList.add('alert')
                    resul.classList.add('alert-success')
                    resul.setAttribute("id","ajax_messages")
                    resul.innerHTML = `
                        <li style="color: black;">${response.success}</li>
                        `
         
                    el.replaceWith(resul);
                    
                    let counts_product=parseInt(inp.value)
                    let trims=parseFloat(response.product)
                    $(`#praice_ajax${slug}`).text(parseFloat(counts_product*trims)+" тенге")
                   if(!counts_product){
                    $(`#praice_ajax${slug}`).text(trims+" тенге")
                   }
                    
                }
                if (response.errors){
                    var el = document.getElementById('ajax_messages')
                    let resul = document.createElement('div')
                    resul.classList.add('alert')
                    resul.classList.add('alert-danger')
                    resul.setAttribute("id","ajax_messages")
                    resul.innerHTML = `
                        <li style="color: black;">${response.errors}</li>
                        `
         
                    el.replaceWith(resul);
                }
              
                $("#final_price").text(response.final_price)
            },
     
            error: function(response) {
                                    console.log('error', response)
                                    console.log(response.errors)
                         }
    })
   
    
     }