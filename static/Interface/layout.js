document.addEventListener('DOMContentLoaded', ()=> {
    
    fetch_data()

    function fetch_data(){
        fetch(`/layout/${user_id}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            }
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then(data => {
              
              console.log(data);
              const profileImageTag=document.querySelector("#profileImageTag")
              profileImageTag.src = baseUrl + data.profile_picture
            })
            .catch(error => {
              // Handle errors
              console.error('There was a problem with the fetch operation:', error);
            });
    }   
});