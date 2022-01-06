
async function sendRequest(url) {
    console.log("BEFORE REQUEST");
    response = await fetch(`${url}admin/encode/`)
    console.log(response);
    if(response.status !== 200) {
        alert("Neuspesno!")
    }
    else {
        alert("Uspesno!")
    }

}