const inputForm=document.getElementById("search-form");
const inputValue=document.getElementById("search-input");
const loader=document.getElementById("loader");
inputForm.addEventListener("submit",(e)=>{
  e.preventDefault();
//   showLoader();
  handleSearch();
})
async function handleSearch(currentQuery){
    const results_div=document.getElementById("results");
    currentQuery = inputValue.value.trim().toLowerCase();
    inputValue.value="";
    results_div.innerHTML=``;
    showLoader();
    await fetch(`/search?question=${currentQuery}`, {
        method: 'GET',
        headers: {
        'Accept': 'application/json',
    }})
    .then(response => response.json())
    .then(data => {
        if(data.message==="No adequate Match"){
            results_div.innerHTML=`No adequate match`;
        }else{
            for (let res of data){
                const div_elem=document.createElement("div");
                div_elem.classList.add("result-card");
                const desc = res.problem_desc.split(/\s+/).slice(0, 20).join(" ");
                div_elem.innerHTML=`
                    <h2 class="result-title">${res.title}
                      </h2>
                      <div class="result-data">
                        <strong>Acceptance:</strong> ${res.acceptance} &nbsp;&nbsp;
                        <strong>Difficulty:</strong> ${res.difficulty}
                      </div>
                    <p class="result-description">
                      ${desc}....
                      
                      <a href="http://localhost:3000/problems/${res.id}" class="more-button" target="_blank">More</a>
                    </p>
                `;
                results_div.appendChild(div_elem);
            }
        }
    })
    .catch(error => {
      console.error('Error:', error);
      results_div.innerHTML="Sorry an error occured!!!";
    }); 
    hideLoader();
}
function showLoader() {
  loader.classList.remove("hidden");
}

function hideLoader() {
  loader.classList.add("hidden");
}
