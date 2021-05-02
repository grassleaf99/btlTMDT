var updateBtns = document.getElementsByClassName("myjs-update-cart")
for(var i = 0; i < updateBtns.length; i++)
{
    updateBtns[i].addEventListener('click', function(){
        var itemId = this.dataset.item
        var action = this.dataset.action
        console.log('itemId: ', itemId, '. Action: ', action)

        console.log('User: ', user)
        updateCart(itemId, action)
        /*
            // nhung dong trong comment nay dung de kiem tra co ton tai user ko (tuc user da dang nhap chua)
            if(user === 'AnonymousUser')
            {
                console.log('Not logged in')
            }
            else
            {
                console.log('User is logged in, sending data...')
            }
        */
    })
}

function updateCart(itemId, action)
{
    console.log('Sending data...')
    // gui du lieu den view
    var url = '/updateItem/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'itemId': itemId, 'action': action})
    })

    .then((response) =>{
        return response.json();
    })

    .then((data) =>{
        console.log('data: ', data)
    })
}