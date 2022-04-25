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
          b="""<div class="wrap">
          <div class="cmt-box">"""
          v="""</div> </div>"""
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
                                                      <button class="btn1 reply set{id}" style="padding:2%;margin-left:2%;color:red;" id="submit_otmena" onclick="Comment_Form_ajaxed('{id}','{parent_id}')"  data-id="{id}" data-parent={parent_id}>Ответить</button>
                                                          <form action="" method="POST" class="comment-form form-group" id="form-{id}" style="display:none;">
 
        <textarea type="text" class="form-control" id="textarea-{id}" name="comment-text"></textarea><br>
  
        <p><input type="button" value="Отправить" onclick="Comments_textarea_post('{parent_id}','{id}')"></p>
    </br>
    </form>
                                                    </div>
                                                    
                                                  </div>

                                           {v}
                                           <div id={id}>
                                            </div>
                                          
    """.format(c=b,v=v, id=comment['id'],author=comment['author'],timestamp=comment['timestamp'],text=comment['text'],parent_id=comment['parent_id'],is_chaild=comment['is_child'])
     
      if comment.get('children'):
        i+=comments_filter(comment['children'])
    
    return mark_safe(res.format(i))




def comments_filter_children(comments_list):
  
    
    res="""<ul> 
    {}
    </ul>"""
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
          b="""<div class="wrap">
          <div class="cmt-box">"""
          v="""</div> </div>"""
        i=""" 
        {c}
        <div id={id}>
        


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
                                                      <button class="btn1 reply set{id}" style="padding:2%;margin-left:2%;color:red;" id="submit_otmena" onclick="Comment_Form_ajaxed('{id}','{parent_id}')"  data-id="{id}" data-parent={parent_id}>Ответить</button>
                                                          <form action="" method="POST" class="comment-form form-group" id="form-{id}" style="display:none;">
 
        <textarea type="text" class="form-control" name="comment-text"></textarea><br>
  
        <p><input type="button" value="Отправить" onclick="Comments_textarea_post('{parent_id}','{id}')"></p>
    </br>
    </form>
                                                    </div>
                                                    
                                                  </div>
                                                  
                                            </div>
                                            {c}
                                            
    """.format(c=b,v=v,id=comment['id'],author=comment['author'],timestamp=comment['timestamp'],text=comment['text'],parent_id=comment['parent_id'],is_chaild=comment['is_child'])
      if comment.get('children'):
        i=comments_filter(comment['children'])
    return mark_safe(res.format(i))



