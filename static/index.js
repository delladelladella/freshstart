function getRadioButtonValue(rbutton){
    for (var i = 0; i < rbutton.length; ++i){ 
        if (rbutton[i].checked)
        return rbutton[i].value;
    }
    return null;
}

function myFunction(){
    //alert("You should move to: " +getRadioButtonValue(document.question["major"]));
}

//Transitions to the next question and changes the button value
function nextAndBack(){
    var degree_questions = document.getElementById("Degree-Choice")
    var location_question = document.getElementById("Location-Choice")
    var next_back_button = document.getElementById("Next-Button")
    var NOTA = document.getElementById("NOTA")
    var submit_button = document.getElementById("Submit-Button")

    if (degree_questions.style.display == "block"){
        degree_questions.style.display = "none"
        NOTA.style.display = "none"
        location_question.style.display = "block"
        next_back_button.value = "Back"
        submit_button.style.display = "inline-block"
    } else{
        location_question.style.display = "none"
        degree_questions.style.display = "block"
        NOTA.style.display = "block"
        next_back_button.value = "Next"
        submit_button.style.display = "none"
    }
}

//sends data to the server and receiving json data in response
//then displaying that data
function getData(){
    //const axios = require('axios').default
    var userMajor = document.querySelector("input[name='Major']:checked").value
    var inTheUS = document.querySelector("input[name='Location']:checked").value
    //axios is a javascript module that allows you to communicate with a server using javascript
    axios.post('/',{// sends user's answers to the server
        Major : userMajor,
        Location : inTheUS
    }).then((response) => {//gets back the response from the server
        data = response.data
        //for each record, create a tag and display them
        var parentDiv = document.getElementById("Location-Response")
        var backButton = document.createElement("button")
        backButton.type = "button"
        backButton.innerText = "Back"
        backButton.onclick = () => window.location.replace("http://localhost:8080")
        backButton.id = "Back-Button"
        for(i=0;i<data.length;i++){
            console.log(data[i])

            var cityChildElement = document.createElement("h3")
            cityChildElement.innerText = data[i].city
            parentDiv.appendChild(cityChildElement)

            var aSalaryChildElement = document.createElement("h4")            
            aSalaryChildElement.innerText = "Average salary (entry level): "+data[i].average_salary
            parentDiv.appendChild(aSalaryChildElement)

            var salaryRChildElement = document.createElement("h4")            
            salaryRChildElement.innerText = "Salary range (entry level): "+data[i].salary_range
            parentDiv.appendChild(salaryRChildElement)
        }
        parentDiv.appendChild(backButton)
        var currentWindow = document.getElementById("Location-Choice")
        currentWindow.style.display = "none"
        var button1 = document.getElementById("Next-Button")
        var button2 = document.getElementById("Submit-Button")
        button1.style.display = "none"
        button2.style.display = "none"
        parentDiv.style.display = "block"
    }).catch(error => console.log(error))
}
