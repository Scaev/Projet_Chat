function form_post(){

var datastring=$form.serialize();
var id__conversation_courante=$conversation.id()
$.ajax({
    url:"/ajax_url/",
    type:'POST',
    data: datastring, id_conversation_courante
        success: function(response){
            result=JSON.parse(response){
                if (result.error){
                    alert(result.error_text);               
                }
                else{
                    //traiter les données
                }
            }
        }
});
}

$("#submit_message").submit(form_post());
