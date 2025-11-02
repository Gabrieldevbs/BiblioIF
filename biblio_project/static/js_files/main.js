const element = document.querySelector('#cpf')
const zip_code = document.querySelector("#zip_code")
const buy_price = document.querySelector("#buy_price")

function limit(element){

    switch(element){
        case cpf:
            if(element.value.length > 14){
                const new_element = element.value.slice(0,14)
                element.value = new_element
            }
            break;

        case zip_code:
            if(element.value.length > 10){
                const new_element = element.value.slice(0,10)
                element.value = new_element
            }
            break;
    }
}

function format(element){
    if (element == zip_code){
        switch(element.value.length){
            case 8:
                const new_element = element.value.slice(0,2) + "." + element.value.slice(2,5) + '-' + element.value.slice(5,8)
                element.value = new_element
                break;
        
            case 9:
                const new_element2 = element.replace(".").replace("-")
                element.value = new_element2
                break;
        }
    } else {
        switch(element.value.length){
            case 11:
                const new_cpf = element.value.slice(0,3) + '.' + element.value.slice(3,6) + '.' + element.value.slice(6, 9) + '-' + element.value.slice(9,11)
                element.value = new_cpf
                break;

            case 13:
                const new_cpf2 = element.value.replaceAll(".", "").replace("-", '')
                element.value = new_cpf2
                break;
        }
    }
}

function delete_letters(element){
    accept_numbers = ["0","1","2","3","4","5","6","7","8","9"]
    last_char = element.value.slice(-1)
    if(!accept_numbers.includes(last_char)){
        const new_element = element.value.slice(0,-1)
        element.value = new_element
    }
}

// -------------------------------------------------------------------

cpf.addEventListener("input", () => limit(cpf))
cpf.addEventListener("input", () => format(cpf))
cpf.addEventListener("input", () => delete_letters(cpf))

// -------------------------------------------------------------------

zip_code.addEventListener("input", () => delete_letters(zip_code))
zip_code.addEventListener("input", () => format(zip_code))
zip_code.addEventListener("input", () => limit(zip_code))

console.log(buy_price.value)