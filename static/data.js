//import users from '/static/data.json' assert {type: 'json'};

//console.log(users);


fetch("http://127.0.0.1:8080/confirmation/successful")
.then(function(response){
    return response.json();
})
.then(function(users){
    var handler = PaystackPop.setup({
        key: users["code"],
        email: users["email"],
        amount: users["amount"],
        ref: users["reference"], // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
        metadata: {
        custom_fields: [
            {
                display_name: users['username'],
                variable_name: users['phone'],
                value: users["phone"]
            }
        ]
        },
        callback: function(response){
            alert('success. transaction ref is ' + response.reference);
        },
        onClose: function(){
            alert('window closed');
        }
    });
    handler.openIframe();
})
