from django.template import Library
from django.utils.html import mark_safe



register=Library()

@register.filter
def comments_filter(comments_list):
  
    
    res="""
    <ul>
    
    {}
  
    </ul>
    """
    i=''
    b=''
    v=''
    pk=0
    try:
      pk=comments_list[0]['pk']
    except:
      pass
    
    for comment in comments_list:
    
      if (comment['object_id_models']==pk):
     

        if comment['is_child']==True:
          b='<div class="wrap"><div class="cmt-box">'
          v='</div></div>'
        

        i+=""" 

        {c}


                                                  <div class="cmt-box">
                                                    <div class="cmt-avatar-item cmt-decorate-item">
                                                      
                                                    </div>
                                                    <div class="cmt-body-item">
                                                      <div class="cmt-top-item pb_10">
                                                        <div class="cmt-name-item"><b>{author}</b></div>
                                                        <div class="cmt-mark-item">

                                                          <div class="cmt-date-item ml_15">{timestamp}</div>
                                                        </div>

                                                      </div>
                                                      <div class="cmt-description-item{id}">
                                                       {text}
                                                      </div>
                                                    </div>
                                                  </div>
                                                  
                                                
<button class="btn1 reply set{id}" style="padding:2%;margin-left:2%;color:red;" id="submit_otmena" data-id="{id}" data-parent={parent_id}>Ответить</button>
        
    <form action="" method="POST" class="comment-form form-group" id="form-{id}" style="display:none;">
 
        <textarea type="text" class="form-control" name="comment-text"></textarea><br>
        <input type="submit" class="btn btn-primary submit-reply estamps-none" name=text data-id="{id}" data-submit-reply="{parent_id}" value="Отправить">
    </form>

    {v}




                  
    """.format(c=b,v=v, id=comment['id'],author=comment['author'],timestamp=comment['timestamp'],text=comment['text'],parent_id=comment['parent_id'],is_chaild=comment['is_child'])
     
      if comment.get('children'):
        i+=comments_filter(comment['children'])
    
    return mark_safe(res.format(i))

