// function getUsers(){
//     fetch('http://localhost:5000/jsonify_users')
//         .then(res =>  res.json())
//         .then(data => {
//             console.log(data)
//             const users = document.getElementById("users");
//             for(let i=0; i < data.users.length; i++) {
//                 let row = document.createElement("tr")

//                 let name= document.createElement("td")
//                 name.innerHTML = `${data.users[i].last_name}, ${data.users[i].first_name}`
//                 row.appendChild(name)

//                 let email=document.createElement("td")
//                 email.innerHTML=data.users[i].email
//                 row.appendChild(email)

//                 users.appendChild(row)
//             } //endfor
//         })  //end .then (data
// }
// getUsers();

/*########################################################
##################   LIKE FORM/BUTTON   ##################
########################################################*/ 
let like_form = document.getElementsByClassName('like_form');
let like_count = document.getElementsByClassName('like_count');
for(let i = 0; i < like_form.length; i++){
    like_form[i].onsubmit = function(e){
        e.preventDefault();
        console.log("clicked form")
        var form = new FormData(like_form[i])
        fetch("/like/form", { method :'POST', body : form})
            .then( response => response.json() )
            .then( data => {
                console.log(data)
                if (data['stars']){
                    console.log(data)
                    console.log(data['stars'])
                    console.log(data['num'])
                    const stars = document.getElementById("stars")
                    stars.innerHTML = `💜 ${data['stars']}` 
                    like_count[i].value = `💜 ${data['num']}`
                }
            })
        }
}


/*########################################################
##################     MESSAGE UPDATE   ##################
########################################################*/ 
const message_update_a = document.getElementsByClassName('message_update_a');
let messsage_update_form = document.getElementsByClassName('messsage_update_form');

for(const i of message_update_a){
    i.onclick = function(e){
        e.preventDefault();

        let message = i.parentNode
        let content = message.firstElementChild
        let form_show = message.nextElementSibling

        message.setAttribute('style', 'display:none')
        form_show.setAttribute('style', 'display:inline')

for(let j of messsage_update_form){
    j.onsubmit = function(e){
        e.preventDefault();
        var form = new FormData(j)
        console.log(form)
        fetch("/message/update", { method :'POST', body : form})
            .then( response => response.json() )
            .then( data => { console.log(data) 
            message.setAttribute('style', 'display:block')
            form_show.setAttribute('style', 'display:none')
            console.log(data.message)
            content.innerHTML = data.message
            }) //endfetch

        } //end j.onsubmit
    } //end for j message_update_form

    } // end a tag click
}//end for a tag


/*########################################################
##################     REPLY UPDATE   ##################
########################################################*/ 
const reply_update_a = document.getElementsByClassName('reply_update_a');
let reply_update_form = document.getElementsByClassName('reply_update_form');

for(const i of reply_update_a){
    i.onclick = function(e){
        e.preventDefault();

        console.log('clickity click')

        let reply = i.parentNode
        console.log(reply)
        let content = reply.firstElementChild
        console.log(content)
        let form_show = reply.nextElementSibling
        console.log(form_show)

        reply.setAttribute('style', 'display:none')
        form_show.setAttribute('style', 'display:inline')

for(let j of reply_update_form){
    j.onsubmit = function(e){
        e.preventDefault();
        var form = new FormData(j)
        console.log(form)
        fetch("/reply/update", { method :'POST', body : form})
            .then( response => response.json() )
            .then( data => { console.log(data) 
            reply.setAttribute('style', 'display:block')
            console.log("#####")
            console.log(reply)
            form_show.setAttribute('style', 'display:none')
            console.log(data.message)
            content.innerHTML = data.message
            }) //endfetch

        } //end on submit
    } //end for j

    } //end onclick
}//end for reply_update





